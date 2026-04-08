from api.client import api_post


def send_chat_message(
    chat_id: int,
    message: str,
    article_id: int | None = None,
    conversation_id: str = "",
):
    payload = {
        "message": message,
        "article_ids": [article_id] if article_id is not None else [],
        "conversation_id": conversation_id,
    }

    return api_post(f"/chats/{chat_id}/messages", payload)