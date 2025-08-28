from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
)
from typing import List, Dict, Any
from codesage_core.components.vector_store.base_vector_store import BaseVectorStore
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        vector_size: int = 384,
    ):
        self.endpoint = os.getenv("VECTOR_STORE_QDRANT_ENDPOINT")
        if not self.endpoint:
            raise ValueError("Qdrant endpoint is not set in environment variables.")
        
        self.port = os.getenv("VECTOR_STORE_QDRANT_PORT")
        if not self.port:
            raise ValueError("Qdrant port is not set in environment variables.")
        
        self.collection_name = os.getenv("VECTOR_STORE_QDRANT_COLLECTION_NAME")
        if not self.collection_name:
            raise ValueError("Qdrant collection name is not set in environment variables.")
        
        self.api_key = os.getenv("VECTOR_STORE_QDRANT_API_KEY")
        if not self.api_key:
            raise ValueError("Qdrant API key is not set in environment variables.")
        
        self.vector_size = vector_size
        self.client = QdrantClient(url=self.endpoint, port=self.port, api_key=self.api_key, )

        self._init_collection()

    def _init_collection(self):
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )

    def upsert(self, chunks: List[Dict[str, Any]]) -> None:
        if not chunks:
            return

        # Assume all chunks have the same repo_url (if present)
        repo_url = chunks[0].get("metadata", {}).get("repo_url", None)
        if repo_url:
            # Delete all points with the same repo_url in payload.metadata
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.repo_url",
                            match=MatchValue(value=repo_url)
                        )
                    ]
                )
            )

        points = []
        for item in chunks:
            points.append(
                PointStruct(
                    id=item.get("id", str(uuid.uuid4())),
                    vector=item["embedding"],
                    payload={
                        "project_name": item.get("project_name", ""),
                        "metadata": item.get("metadata", {}),
                        "llm_summary": item.get("llm_summary", ""),
                        "raw_code": item.get("raw_code", ""),
                    }
                )
            )
        self.client.upsert(collection_name=self.collection_name, points=points)

    def query(self, query_vector: List[float], project_name: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="project_name",
                        match=MatchValue(value=project_name)  # Match all projects
                    )
                ]
            ),
            limit=top_k
        )
        return [
            {
                "id": hit.id,
                "score": hit.score,
                "metadata": hit.payload
            }
            for hit in search_result
        ]

    def delete_collection(self) -> None:
        self.client.delete_collection(collection_name=self.collection_name)
