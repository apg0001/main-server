from api.client import api_post


def send_chat_message(message: str, keyword_id=None):
    payload = {
        "message": message,
    }

    if keyword_id:
        payload["keyword_id"] = keyword_id

    # 실제 AI 서버 연동 스펙에 따라 수정 가능
    result = api_post("/chat-messages", payload)

    if isinstance(result, dict):
        return (
            result.get("answer")
            or result.get("response")
            or result.get("message")
            or result.get("content")
            or "응답이 없습니다."
        )

    if isinstance(result, str):
        return result

    return "응답 형식을 해석하지 못했습니다."