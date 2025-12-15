import os
import cohere
import qdrant_client
import requests
from bs4 import BeautifulSoup
from data_ingestion.chunking import chunk_text
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

# Load environment variables from .env file
load_dotenv()

# Initialize clients
co = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client_instance = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# --- Configuration ---
SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-native-book-seven.vercel.app/sitemap.xml") # Default value for local testing
QDRANT_COLLECTION_NAME = "ai-native-book"

def get_urls_from_sitemap(sitemap_url: str):
    """
    Fetches a sitemap and extracts all URLs.
    """
    urls = []
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Handle both regular sitemap and sitemap index
        content = response.content.decode('utf-8')
        if '<sitemapindex>' in content:
            # This is a sitemap index, parse it differently
            root = ET.fromstring(content)
            for sitemap in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                urls.extend(get_urls_from_sitemap(sitemap.text))
        else:
            # This is a regular sitemap
            root = ET.fromstring(content)
            for url_element in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                urls.append(url_element.text)
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
    except ET.ParseError as e:
        print(f"Error parsing sitemap: {e}")
    return urls

def scrape_page(url: str):
    """
    Scrapes a single page and extracts the main content and title.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        title = soup.find("title").get_text() if soup.find("title") else "No Title"

        # Try to find main content containers (Docusaurus-specific selectors)
        main_content = (
            soup.find("main") or
            soup.find("article") or
            soup.find("div", class_="container") or
            soup.find("div", class_="main-wrapper") or
            soup.find("div", {"role": "main"}) or
            soup.body
        )

        if main_content:
            # Extract text with proper separation
            text = main_content.get_text(separator="\n", strip=True)

            # Clean up excess whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            clean_text = "\n".join(lines)
            return title, clean_text

        return title, ""
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return "No Title", ""

def ingest_data():
    """
    Crawls the Docusaurus site, chunks the content, generates embeddings,
    and stores them in Qdrant.
    """
    print("Starting data ingestion...")

    # Ensure the Qdrant collection exists
    try:
        qdrant_client_instance.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
        # Clear existing collection
        qdrant_client_instance.delete_collection(QDRANT_COLLECTION_NAME)
        print(f"Existing collection '{QDRANT_COLLECTION_NAME}' deleted.")
    except Exception:
        print(f"Collection '{QDRANT_COLLECTION_NAME}' does not exist yet, will be created.")

    # Recreate collection with proper dimensions for embed-english-v3.0
    qdrant_client_instance.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=qdrant_client.models.VectorParams(size=1024, distance=qdrant_client.models.Distance.COSINE),
    )
    print(f"Collection '{QDRANT_COLLECTION_NAME}' created/recreated.")

    urls_to_scrape = get_urls_from_sitemap(SITEMAP_URL)
    if not urls_to_scrape:
        print("No URLs found in sitemap. Exiting.")
        return

    print(f"Found {len(urls_to_scrape)} URLs to process:")
    for url in urls_to_scrape:
        print(f"  - {url}")

    documents_to_embed = []
    point_id = 0
    for url in urls_to_scrape:
        print(f"Scraping {url}...")
        page_title, page_content = scrape_page(url)
        if page_content:
            chunks = chunk_text(page_content)
            for idx, chunk in enumerate(chunks):
                documents_to_embed.append({
                    "id": point_id,
                    "text": chunk,
                    "payload": {
                        "url": url,
                        "page_title": page_title,
                        "chunk_index": idx,
                        "content": chunk
                    }
                })
                point_id += 1
        else:
            print(f"  No content extracted from {url}")

    print(f"Generated {len(documents_to_embed)} documents/chunks for embedding.")

    if not documents_to_embed:
        print("No documents to ingest. Exiting.")
        return

    # Generate embeddings in batches to avoid rate limits
    BATCH_SIZE = 100
    total_points = len(documents_to_embed)

    for i in range(0, total_points, BATCH_SIZE):
        batch = documents_to_embed[i:i + BATCH_SIZE]
        texts = [doc["text"] for doc in batch]

        print(f"Processing batch {i // BATCH_SIZE + 1}/{(total_points - 1) // BATCH_SIZE + 1}...")

        # Generate embeddings
        embeddings = co.embed(texts=texts, model="embed-english-v3.0").embeddings

        # Store in Qdrant
        points = [
            qdrant_client.models.PointStruct(
                id=doc["id"],
                vector=embeddings[j],
                payload=doc["payload"],
            )
            for j, doc in enumerate(batch)
        ]

        qdrant_client_instance.upload_points(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points,
            wait=True
        )

    print("Data ingestion complete.")

def main():
    ingest_data()

if __name__ == "__main__":
    main()