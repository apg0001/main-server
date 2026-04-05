from api.client import ai_chat_post
import streamlit as st


def send_chat_message(message: str, article_id: int | None = None):
    user = st.session_state.get("user") or {}
    user_id = user.get("id")

    if not user_id:
        raise ValueError("로그인 사용자 정보가 없습니다.")

    inputs = {
        "user_id": user_id,
    }

    if article_id is not None:
        inputs["article_id"] = article_id

    payload = {
        "inputs": inputs,
        "query": message,
        "conversation_id": st.session_state.get("conversation_id", ""),
        "response_mode": "blocking",
        "user": str(user_id),
    }

    result = ai_chat_post("/chat-messages", payload)

    if isinstance(result, dict):
        conversation_id = result.get("conversation_id")
        if conversation_id:
            st.session_state["conversation_id"] = conversation_id

        return result.get("answer", "응답이 없습니다.")

    return "응답 형식을 해석하지 못했습니다."