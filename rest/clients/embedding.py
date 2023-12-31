from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from typing import List
from pathlib import Path

import uuid
import json

from .dandi import DandiClient


class EmbeddingClient:
    def __init__(self):
        self.dandi_client = DandiClient()
        self.embeddings_client = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en")

    def get_embedding_simple(self, text: str) -> list:
        """Get embedding for a single text"""
        print("get_embedding_simple reached.")
        try:
            emb = self.embeddings_client.embed_query(text=text)
        except Exception as e:
            print(f"exception occurred: {e}")
        print(emb)
        return emb


    def get_embeddings(self, metadata_list: List[dict], max_num_sets: int = None, save_to_file: bool = False) -> List:
        """Get embeddings for all metadata fields, organizes them as list of objects similar to Qdrant points"""
        if not max_num_sets:
            max_num_sets = len(metadata_list)
        query_list = [self.dandi_client.stringify_relevant_metadata(m) for m in metadata_list[:max_num_sets]]
        embeddings = self.embeddings_client.embed_documents(texts=query_list)
        # Prepare Qdrant Points
        qdrant_points = [
            {
                "id": str(uuid.uuid4()),
                "vector": emb,
                "payload": metadata_list[i],
            } for i, emb in enumerate(embeddings)
        ]
        if save_to_file and len(qdrant_points) > 0:
            with open(str(Path.cwd().parent / "data" / "qdrant_points_emb.json"), "w") as f:
                json.dump(qdrant_points, f)
        return qdrant_points

