from api.client import api_get


def get_articles(keyword_id=None, page=1, size=10):
    params = {
        "page": page,
        "size": size,
    }

    if keyword_id:
        params["keywordId"] = keyword_id

    result = api_get("/articles", params=params)

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        if "items" in result:
            return result["items"]
        if "articles" in result:
            return result["articles"]
        if "content" in result:
            return result["content"]

    return []


def get_article_detail(article_id: int):
    return api_get(f"/articles/{article_id}")


def get_importance_list(keyword_id=None):
    params = {}
    if keyword_id:
        params["keywordId"] = keyword_id

    result = api_get("/importance", params=params)

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        if "items" in result:
            return result["items"]
        if "importance" in result:
            return result["importance"]

    return []