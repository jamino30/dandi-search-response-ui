import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

from rest.clients.dandi import DandiClient
from rest.clients.openai import OpenaiClient


dandi_client = DandiClient()
openai_client = OpenaiClient()

# extract dandisets metadata
all_metadata = dandi_client.get_all_dandisets_metadata()
all_metadata_formatted: list[dict] = dandi_client.collect_relevant_metadata(metadata_list=all_metadata)
print("START: Number of items:", len(all_metadata_formatted))


# blacklist specific dandiset ids
dandiset_blacklist = [
    "000545/draft",
    "000470/draft",
    "000411/draft",
    "000529/draft",
    "000299/draft",
    "000029/0.230317.1553",
    "000029/0.231017.2004"
    "000027/0.210831.2033",
    "000126/0.210813.0327",
    "000544/0.230514.1148",
    "000482/draft",
    "000068/draft",
]

filtered_all_metadata_formatted = []
for i, dandiset in enumerate(all_metadata_formatted):
    if not any(item in dandiset["dandiset_id"] for item in dandiset_blacklist):
        filtered_all_metadata_formatted.append(dandiset)
    else:
        print(f"REMOVED -- {dandiset['dandiset_id']}: {dandiset['title']}")

num_not_removed = len(dandiset_blacklist) - (len(all_metadata_formatted) - len(filtered_all_metadata_formatted))
if num_not_removed:
    print(f"NOTE: {num_not_removed} blacklisted dandisets not removed.")

# overwrite qdrant_points.json
emb = openai_client.get_embeddings(
    metadata_list=filtered_all_metadata_formatted,
    save_to_file=True
)
print("END: Number of emb items:", len(emb))