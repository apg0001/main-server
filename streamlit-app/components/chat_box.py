import streamlit as st

from api.chat import send_chat_message


def render_chat_box():
    st.subheader("AI 채팅")

    if not st.session_state["chat_messages"]:
        st.info("질문을 입력하면 AI 응답이 표시됩니다.")

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("예: 하이닉스 관련 기사 흐름 요약해줘")

    if prompt:
        st.session_state["chat_messages"].append({"role": "user", "content": prompt})

        selected_keyword = st.session_state.get("selected_keyword_name")

        with st.chat_message("assistant"):
            with st.spinner("응답 생성 중..."):
                try:
                    answer = send_chat_message(
                        message=prompt,
                        keyword=selected_keyword,
                    )
                except Exception as e:
                    answer = (
                        f"채팅 요청 실패: {e}\n\n"
                        "AI 서버 URL(AI_BASE_URL)이나 /chat-messages 요청 스펙을 확인해줘."
                    )
                st.write(answer)

        st.session_state["chat_messages"].append(
            {"role": "assistant", "content": answer}
        )