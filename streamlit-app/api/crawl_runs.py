import os

from dotenv import load_dotenv

from api.client import api_delete, api_get, api_patch, api_post

load_dotenv()
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ko")

from api.client import api_get, api_post


def create_crawl_run(keyword_ids: list[int] | None = None, force: bool = False):
    payload = {
        "keyword_ids": keyword_ids or [],
        "force": force,
    }
    return api_post("/crawl-runs", payload)


def get_crawl_runs(page=1, size=20, status=None, keyword_id=None):
    params = {
        "page": page,
        "size": size,
    }
    if status:
        params["status"] = status
    if keyword_id is not None:
        params["keyword_id"] = keyword_id

    return api_get("/crawl-runs", params=params)

def get_keywords(page=1, size=100, is_active=None, language=None, q=None):
    params = {
        "page": page,
        "size": size,
    }
    if is_active is not None:
        params["is_active"] = is_active
    if language:
        params["language"] = language
    if q:
        params["q"] = q

    result = api_get("/keywords", params=params)

    items = result.get("items", []) if isinstance(result, dict) else []
    page_info = result.get("page_info") if isinstance(result, dict) else None
    return items, page_info


def create_keyword(keyword: str, language: str = DEFAULT_LANGUAGE):
    payload = {
        "keyword": keyword,
        "language": language,
    }
    return api_post("/keywords", payload)


def batch_create_keywords(keywords: list[str], language: str = DEFAULT_LANGUAGE):
    payload = {
        "keywords": keywords,
        "language": language,
    }
    return api_post("/keywords/batch", payload)


def update_keyword_active(keyword_id: int, is_active: bool):
    payload = {"is_active": is_active}
    return api_patch(f"/keywords/{keyword_id}", payload)


def delete_keyword(keyword_id: int):
    return api_delete(f"/keywords/{keyword_id}")