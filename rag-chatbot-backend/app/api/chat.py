from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse, Source
from app.services.qdrant_service import QdrantService
import cohere
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Initialize Qdrant service
QDRANT_COLLECTION_NAME = "ai-native-book" # This should be consistent with ingestion
qdrant_service = QdrantService(collection_name=QDRANT_COLLECTION_NAME)

# Initialize OpenAI client for agent (using non-OpenAI model endpoint as configured)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY environment variable not set. Using Cohere for responses instead.")

openai_client = OpenAI(
    api_key=openai_api_key or "sk-dummy",  # Use dummy key if not set, but will fail gracefully in usage
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # This allows using non-OpenAI endpoints
) if openai_api_key else None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate embedding for the query using embed-english-v3.0
        query_embedding = co.embed(texts=[request.query], model="embed-english-v3.0", input_type="search_query").embeddings[0]

        # Perform similarity search in Qdrant
        retrieved_chunks_with_payload = qdrant_service.search(query_vector=query_embedding)

        if not retrieved_chunks_with_payload:
            # If no content is found, return "I don't know"
            return ChatResponse(
                answer="I don't know. The requested information is not available in the book content.",
                sources=[]
            )

        retrieved_texts = []
        sources_list = []
        for payload_data in retrieved_chunks_with_payload:
            payload = payload_data['payload']
            retrieved_texts.append(payload['content'])
            sources_list.append(Source(
                url=payload['url'],
                page_title=payload['page_title'],
                chunk_index=payload['chunk_index'],
                content=payload['content']
            ))

        # Build the context from retrieved information
        context = "\n\n".join(retrieved_texts)

        if openai_client:
            # Use OpenAI API to generate response (this allows non-OpenAI model endpoints as configured)
            # Create a strict RAG prompt that forces the agent to only use provided context
            system_prompt = """You are an AI assistant that strictly answers questions based only on the provided context from the book.
            If the information is not available in the provided context, respond with 'I don't know'.
            Do not make up information or use general knowledge. Only answer based on the specific context provided."""

            user_prompt = f"""
            Context:
            {context}

            Question: {request.query}

            Answer: """

            response = openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),  # This can be configured with custom models
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            answer = response.choices[0].message.content.strip()
        else:
            # Fallback to Cohere if OpenAI API key is not set
            system_prompt = f"""You are an AI assistant that strictly answers questions based only on the provided context from the book.
            If the information is not available in the provided context, respond with 'I don't know'.
            Do not make up information or use general knowledge. Only answer based on the specific context provided."""

            user_prompt = f"""
            Context:
            {context}

            Question: {request.query}

            Answer: """

            # Generate answer using Cohere
            response = co.generate(
                prompt=f"{system_prompt}\n\n{user_prompt}",
                model="command-r",  # Using Cohere Command-R model
                temperature=0.3,
                max_tokens=500
            )
            answer = response.generations[0].text.strip()

        return ChatResponse(answer=answer, sources=sources_list)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))