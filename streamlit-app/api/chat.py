from api.client import ai_post


def send_chat_message(message: str, keyword: str | None = None):
    
    payload = {
        "query": message,
        "response_mode": "blocking",
        "user": "streamlit-user",
    }

    if keyword:
        payload["inputs"] = {"keyword": keyword}
    else:
        payload["inputs"] = {}

    result = ai_post("/chat-messages", payload, with_auth=True)

    if isinstance(result, dict):
        return (
            result.get("answer")
            or result.get("message")
            or result.get("content")
            or result.get("text")
            or "응답이 없습니다."
        )

    if isinstance(result, str):
        return result

    return "응답 형식을 해석하지 못했습니다."