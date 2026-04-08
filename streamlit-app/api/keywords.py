import os

from dotenv import load_dotenv

from api.client import api_delete, api_get, api_patch, api_post
from api.crawl_runs import create_crawl_run

load_dotenv()
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ko")


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

    try:
        result = api_get("/keywords", params=params)
    except Exception as e:
        error_text = str(e)
        if "404" in error_text or "Not Found" in error_text:
            return [], {"page": page, "size": size, "total": 0}
        raise

    items = result.get("items", []) if isinstance(result, dict) else []
    page_info = result.get("page_info") if isinstance(result, dict) else None
    return items, page_info