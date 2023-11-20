from dandi.dandiapi import DandiAPIClient
from .clients.qdrant import QdrantClient

# Number of similar results to fetch (adjust based on model)
TOP_K = 6

dandi_client = DandiAPIClient()


def scan_for_relevant_dandisets(query: str, model: str, qdrant_client, openai_client, llama2_client):
    query = query.strip()

    # Get semantic search results
    def get_similar_results(query: str, qdrant_client: QdrantClient, openai_client, llama2_client):
        similar_results = qdrant_client.query_from_user_input(
            text=query, 
            collection_name=model, 
            top_k=TOP_K,
            openai_client=openai_client,
            llama2_client=llama2_client
        )
        return similar_results

    similar_results = get_similar_results(query, qdrant_client, openai_client, llama2_client)
    print("Results found.")
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

    results = {
        "ids": dandiset_ids if dandiset_ids else None, 
        "scores": list(scores) if scores else None, 
        "names": dandiset_names if dandiset_names else None
    }
    return results


# Dandi search algorithm to address scientific/quantitative queries
class DandiSearch:
    def __init__(self):
        pass