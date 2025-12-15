import os
import qdrant_client
from typing import List, Dict

class QdrantService:
    def __init__(self, collection_name: str):
        self.client = qdrant_client.QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = collection_name

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Performs a similarity search in Qdrant.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )
        results = []
        for hit in search_result:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            })
        return results