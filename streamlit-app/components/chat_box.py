import streamlit as st

from api.chat import send_chat_message


def render_chat_box():
    st.subheader("채팅")

    if not st.session_state["chat_messages"]:
        st.info("질문을 입력하면 AI 응답이 표시됩니다.")

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("예: 하이닉스 관련 검색 현황 알려줘")

    if prompt:
        st.session_state["chat_messages"].append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("assistant"):
            with st.spinner("응답 생성 중..."):
                try:
                    answer = send_chat_message(
                        message=prompt,
                        keyword_id=st.session_state.get("selected_keyword_id"),
                    )
                except Exception as e:
                    answer = f"채팅 요청 실패: {e}"

                st.write(answer)

        st.session_state["chat_messages"].append(
            {"role": "assistant", "content": answer}
        )