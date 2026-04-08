import streamlit as st
from api.chat_rooms import create_chat, get_chat_detail, get_chat_list


def render_chat_list():
    st.subheader("채팅방")

    if "selected_chat_id" not in st.session_state:
        st.session_state["selected_chat_id"] = None

    if "chat_conversation_id" not in st.session_state:
        st.session_state["chat_conversation_id"] = ""

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    # 🔹 채팅방 생성
    with st.expander("새 채팅방 만들기", expanded=False):
        new_title = st.text_input("채팅방 제목", key="new_chat_title")

        if st.button("채팅방 생성", use_container_width=True):
            try:
                if not new_title.strip():
                    st.warning("채팅방 제목을 입력하세요.")
                else:
                    result = create_chat(title=new_title.strip())

                    data = result.get("data", {})
                    chat_id = data.get("id")

                    st.session_state["selected_chat_id"] = chat_id
                    st.session_state["chat_conversation_id"] = ""
                    st.session_state["chat_messages"] = []

                    st.success("채팅방 생성 완료")
                    st.rerun()

            except Exception as e:
                st.error(f"생성 실패: {e}")

    st.markdown("---")

    # 🔹 채팅방 목록
    try:
        result = get_chat_list(page=1, size=20)

        data = result.get("data", {})
        items = data.get("items", [])

        if not items:
            st.info("채팅방이 없습니다.")
            return

        for chat in items:
            chat_id = chat.get("id")
            title = chat.get("title", f"채팅 {chat_id}")

            is_selected = st.session_state.get("selected_chat_id") == chat_id
            label = f"✅ {title}" if is_selected else title

            if st.button(label, key=f"chat_{chat_id}", use_container_width=True):
                detail = get_chat_detail(chat_id)
                detail_data = detail.get("data", {})

                st.session_state["selected_chat_id"] = chat_id
                st.session_state["chat_conversation_id"] = (
                    detail_data.get("external_conversation_id") or ""
                )
                st.session_state["chat_messages"] = []

                st.rerun()

    except Exception as e:
        st.error(f"채팅 목록 불러오기 실패: {e}")