from dandi.dandiapi import DandiAPIClient
from .clients.qdrant import QdrantClient

# Number of similar results to fetch (adjust based on model)
TOP_K = 6

# Semantic "simple" search vs keyword-based "keyword" search (adjust based on model)
# METHOD = "simple"

dandi_client = DandiAPIClient()


# change to true if testing locally; set to false for deployment
TESTING = True

def scan_for_relevant_dandisets(query: str, model: str, qdrant_client: QdrantClient):
    query = query.strip()

    # Get semantic search results
    def get_similar_results(query: str, qdrant_client: QdrantClient):
        similar_results = qdrant_client.query_from_user_input(
            text=query, 
            collection_name=model, 
            top_k=TOP_K,
            testing=TESTING
        )
        return similar_results

    similar_results = get_similar_results(query, qdrant_client)
    similar_results, scores = zip(*similar_results)

    dandiset_ids = []
    dandiset_names = []
    for dandiset_result in similar_results:
        id = dandiset_result.split(":")[-1]
        dandiset_ids.append(id)

        # show dandiset name
        dandiset_id, dandiset_version = id.split("/")
        dandiset = dandi_client.get_dandiset(dandiset_id, dandiset_version)
        name = dandiset.get_metadata().name.strip()
        dandiset_names.append(name)

    return {"ids": dandiset_ids, "scores": list(scores), "names": dandiset_names}