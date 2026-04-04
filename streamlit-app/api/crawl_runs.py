from api.client import api_get, api_post


def create_crawl_run(keyword_id=None):
    payload = {}
    if keyword_id:
        payload["keywordId"] = keyword_id
    return api_post("/crawl-runs", payload)


def get_crawl_runs(page=1, size=10):
    result = api_get("/crawl-runs", params={"page": page, "size": size})

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        if "items" in result:
            return result["items"]
        if "content" in result:
            return result["content"]
        if "runs" in result:
            return result["runs"]

    return []


def get_crawl_run_detail(run_id: int):
    return api_get(f"/crawl-runs/{run_id}")