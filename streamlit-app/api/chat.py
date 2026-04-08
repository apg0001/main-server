from api.client import api_post
import streamlit as st


def send_chat_message(message: str, article_id: int | None = None):
    payload = {
        "message": message,
        "article_id": article_id,
        "conversation_id": st.session_state.get("conversation_id", ""),
    }

    result = api_post("/ai/chat", payload)

    if isinstance(result, dict):
        conversation_id = result.get("conversation_id")
        if conversation_id:
            st.session_state["conversation_id"] = conversation_id

        return result.get("answer", "응답이 없습니다.")

    return "응답 형식을 해석하지 못했습니다."