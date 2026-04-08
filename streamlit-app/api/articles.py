from api.client import api_get, api_post, api_delete


def get_articles(keyword_id=None, page=1, size=10, q=None, sort="published_at_desc"):
    params = {
        "page": page,
        "size": size,
        "sort": sort,
    }

    if keyword_id:
        params["keyword_id"] = keyword_id
    if q:
        params["q"] = q

    try:
        result = api_get("/articles", params=params)
    except Exception as e:
        error_text = str(e)
        if "404" in error_text or "Not Found" in error_text:
            return [], {"page": page, "size": size, "total": 0}
        raise

    items = result.get("items", []) if isinstance(result, dict) else []
    page_info = result.get("page_info") if isinstance(result, dict) else None
    return items, page_info


def get_article_detail(article_id: int):
    return api_get(f"/articles/{article_id}")


def get_article_importance(article_id: int):
    return api_get(f"/articles/{article_id}/importance")


def get_article_feedback(article_id: int):
    return api_get(f"/articles/{article_id}/feedback")


def upsert_article_feedback(article_id: int, action: str):
    return api_post(f"/articles/{article_id}/feedback", {"action": action})


def delete_article_feedback(article_id: int):
    return api_delete(f"/articles/{article_id}/feedback")