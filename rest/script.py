import json

from dandi.dandiapi import DandiAPIClient
from pathlib import Path

from .clients.qdrant import QdrantClient
from .clients.openai import OpenaiClient

# Number of similar results to fetch (adjust based on model)
TOP_K = 6

# Semantic "simple" search vs keyword-based "keyword" search (adjust based on model)
METHOD = "simple"

def scan_for_relevant_dandisets(query: str):
    # strip user query
    query = query.strip()

    # Populate Qdrant
    def populate_qdrant():
        with open(str(Path.cwd() / "data/qdrant_points.json"), "r") as file:
            emb = json.load(file)
        qdrant_client = QdrantClient(host="https://906c3b3f-d3ff-4497-905f-2d7089487cf9.us-east4-0.gcp.cloud.qdrant.io")
        qdrant_client.create_collection(collection_name="dandi_collection")
        qdrant_client.add_points_to_collection(collection_name="dandi_collection", embeddings_objects=emb)
        return qdrant_client


    # Get semantic search results
    def get_similar_results(query: str, qdrant_client: QdrantClient):
        similar_results = qdrant_client.query_from_user_input(text=query, collection_name="dandi_collection", top_k=TOP_K)
        return similar_results

    def get_keyword_results(query: str, openai_client: OpenaiClient, qdrant_client: QdrantClient):
        keywords = openai_client.keywords_extraction(user_input=query)
        similar_results = get_similar_results(query="".join(keywords), qdrant_client=qdrant_client)
        return similar_results

    qdrant_client = populate_qdrant()
    if METHOD == "simple":
        similar_results = get_similar_results(query, qdrant_client)
    else:
        openai_client = OpenaiClient()
        similar_results = get_keyword_results(query, openai_client, qdrant_client)
    similar_results = [id for id, _ in similar_results]

    dandiset_ids = []
    dandiset_names = []
    for dandiset_result in similar_results:
        id = dandiset_result.split(":")[-1]
        dandiset_ids.append(id)
        # dandiset_archive_link = f"https://dandiarchive.org/dandiset/{dandiset_path}"
        
        # show dandiset name
        dandi_client = DandiAPIClient()
        dandiset_id, dandiset_version = id.split("/")
        dandiset = dandi_client.get_dandiset(dandiset_id, dandiset_version)
        name = dandiset.get_metadata().name.strip()
        dandiset_names.append(name)

    return {"ids": dandiset_ids, "names": dandiset_names}