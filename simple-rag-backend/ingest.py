#!/usr/bin/env python3
"""
Simplified ingestion script to populate the Qdrant vector database.
"""
import os
import cohere
import qdrant_client
import requests
from bs4 import BeautifulSoup
from chunking import chunk_text
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY", "YOUR_COHERE_API_KEY_HERE"))

# Qdrant configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

if QDRANT_API_KEY:
    qdrant_client_instance = qdrant_client.QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY
    )
else:
    qdrant_client_instance = qdrant_client.QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT
    )

VECTOR_SIZE = 1024  # Cohere embeddings size for embed-english-v3.0


def get_urls_from_sitemap(sitemap_url: str):
    """
    Fetches a sitemap and extracts all URLs.
    """
    urls = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(sitemap_url, headers=headers)
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
        logger.error(f"Error fetching sitemap: {e}")
    except ET.ParseError as e:
        logger.error(f"Error parsing sitemap: {e}")
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

        # Try to get the title
        title_elem = soup.find("title")
        title = title_elem.get_text().strip() if title_elem else "No Title"

        # Try to find main content containers (common selectors)
        main_content = (
            soup.find("main") or
            soup.find("article") or
            soup.find("div", class_="container") or
            soup.find("div", class_="main-content") or
            soup.find("div", {"role": "main"}) or
            soup.find("div", {"id": "content"}) or
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
        logger.error(f"Error scraping {url}: {e}")
        return "No Title", ""
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {e}")
        return "No Title", ""


def setup_collection():
    """
    Ensures the Qdrant collection exists with the proper schema.
    """
    try:
        # Check if collection exists
        collections = qdrant_client_instance.get_collections()
        collection_exists = any(collection.name == COLLECTION_NAME for collection in collections.collections)

        if collection_exists:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists. Clearing existing data...")
            # Delete the existing collection
            qdrant_client_instance.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted existing collection '{COLLECTION_NAME}'")

        # Create collection with proper dimensions for embed-english-v3.0
        qdrant_client_instance.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qdrant_client.models.VectorParams(
                size=VECTOR_SIZE, 
                distance=qdrant_client.models.Distance.COSINE
            ),
        )
        
        # Create payload indexes for common metadata fields
        try:
            qdrant_client_instance.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="page_title",
                field_schema=qdrant_client.models.PayloadSchemaType.KEYWORD
            )
        except Exception as e:
            logger.warning(f"Could not create payload index for page_title: {e}")
            
        try:
            qdrant_client_instance.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="url",
                field_schema=qdrant_client.models.PayloadSchemaType.TEXT
            )
        except Exception as e:
            logger.warning(f"Could not create payload index for url: {e}")

        logger.info(f"Collection '{COLLECTION_NAME}' created with {VECTOR_SIZE}-dimensional vectors")
        
    except Exception as e:
        logger.error(f"Error setting up collection: {e}")
        raise


def ingest_data(sitemap_url: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Crawls the site from the sitemap, chunks the content, generates embeddings,
    and stores them in Qdrant.
    """
    logger.info("Starting data ingestion...")

    # Setup the collection
    setup_collection()

    # Get URLs from sitemap
    urls_to_scrape = get_urls_from_sitemap(sitemap_url)
    if not urls_to_scrape:
        logger.warning("No URLs found in sitemap. Exiting.")
        return

    logger.info(f"Found {len(urls_to_scrape)} URLs to process:")
    for url in urls_to_scrape:
        logger.info(f"  - {url}")

    # Process each URL and collect documents to embed
    documents_to_embed = []
    point_id = 0
    
    for url in urls_to_scrape:
        logger.info(f"Scraping {url}...")
        page_title, page_content = scrape_page(url)
        
        if page_content:
            chunks = chunk_text(page_content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            for idx, chunk in enumerate(chunks):
                documents_to_embed.append({
                    "id": str(point_id),  # Use string IDs
                    "text": chunk,
                    "payload": {
                        "url": url,
                        "page_title": page_title,
                        "chunk_index": idx,
                        "content": chunk,
                        "created_at": str(datetime.now())
                    }
                })
                point_id += 1
        else:
            logger.warning(f"  No content extracted from {url}")

    logger.info(f"Generated {len(documents_to_embed)} documents/chunks for embedding.")

    if not documents_to_embed:
        logger.warning("No documents to ingest. Exiting.")
        return

    # Generate embeddings and store in batches to avoid rate limits
    BATCH_SIZE = 50  # Reduced batch size to avoid rate limits
    total_points = len(documents_to_embed)

    logger.info(f"Processing {total_points} documents in batches of {BATCH_SIZE}...")

    for i in range(0, total_points, BATCH_SIZE):
        batch = documents_to_embed[i:i + BATCH_SIZE]
        texts = [doc["text"] for doc in batch]

        logger.info(f"Processing batch {i // BATCH_SIZE + 1}/{(total_points - 1) // BATCH_SIZE + 1}...")

        try:
            # Generate embeddings
            embeddings_response = cohere_client.embed(
                texts=texts, 
                model="embed-english-v3.0",
                input_type="search_document"
            )
            embeddings = embeddings_response.embeddings

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
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True
            )

            logger.info(f"Uploaded batch {i // BATCH_SIZE + 1} successfully")
            
        except Exception as e:
            logger.error(f"Error processing batch {i // BATCH_SIZE + 1}: {e}")
            raise

    logger.info("Data ingestion complete.")


if __name__ == "__main__":
    from datetime import datetime
    
    SITEMAP_URL = os.getenv("SITEMAP_URL", "https://ai-native-book-seven.vercel.app/sitemap.xml")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    print("Starting sitemap ingestion process...")
    print(f"Sitemap URL: {SITEMAP_URL}")
    print(f"Qdrant Collection: {COLLECTION_NAME}")
    print(f"Chunk Size: {CHUNK_SIZE}, Chunk Overlap: {CHUNK_OVERLAP}")
    print("-" * 50)

    try:
        ingest_data(SITEMAP_URL, CHUNK_SIZE, CHUNK_OVERLAP)
        print("\nIngestion completed successfully!")
    except Exception as e:
        print(f"\nError during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)