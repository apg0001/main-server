from api.client import api_delete, api_get, api_patch, api_post


def get_keywords():
    result = api_get("/keywords")

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        if "items" in result:
            return result["items"]
        if "keywords" in result:
            return result["keywords"]

    return []


def create_keyword(name: str):
    payload = {"name": name}
    return api_post("/keywords", payload)


def update_keyword(keyword_id: int, payload: dict):
    return api_patch(f"/keywords/{keyword_id}", payload)


def delete_keyword(keyword_id: int):
    return api_delete(f"/keywords/{keyword_id}")