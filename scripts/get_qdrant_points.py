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


# blacklist specific dandiset ids (ignore version for now)
dandiset_blacklist = [
    "000545",
    "000470",
    "000411",
    "000529",
    "000299",
    "000029",
    "000027",
    "000126",
    "000544",
    "000482",
    "000068",
]

filtered_all_metadata_formatted = []
for i, dandiset in enumerate(all_metadata_formatted):
    if not any(item in str(dandiset["dandiset_id"]).split(":")[-1] for item in dandiset_blacklist):
        filtered_all_metadata_formatted.append(dandiset)
    else:
        print(f"REMOVED -- {dandiset['dandiset_id']}: {dandiset['title']}")

num_not_removed = len(dandiset_blacklist) - (len(all_metadata_formatted) - len(filtered_all_metadata_formatted))
if num_not_removed:
    print(f"NOTE: {num_not_removed} blacklisted dandisets not removed.")

# overwrite qdrant_points.json
update_file = True
if update_file:
    emb = openai_client.get_embeddings(
        metadata_list=filtered_all_metadata_formatted,
        save_to_file=True
    )
    print("END: Number of emb items:", len(emb))