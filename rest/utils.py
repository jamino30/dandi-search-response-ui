import uuid

def generate_object_key(user_query: str, max_length=1024):
    unique_id = str(uuid.uuid4())
    type = ".json"
    remaining = max_length - len(type) - len(unique_id)

    formatted_query = "_".join(user_query.strip().lower().split())
    if len(formatted_query) > remaining:
        formatted_query = formatted_query[:remaining]
        if len(formatted_query) > 0 and formatted_query[-1] == "_":
            formatted_query = formatted_query[:-1]

    object_key = f"{formatted_query}_{unique_id}{type}"
    return object_key