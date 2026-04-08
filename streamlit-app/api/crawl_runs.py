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