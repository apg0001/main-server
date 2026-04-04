import streamlit as st

from api.keywords import create_keyword, delete_keyword, get_keywords
from utils.session import reset_chat, set_selected_keyword


def render_sidebar():
    st.sidebar.title("키워드 관리")

    keywords = get_keywords()

    st.sidebar.subheader("키워드 리스트")

    if not keywords:
        st.sidebar.info("등록된 키워드가 없습니다.")

    for kw in keywords:
        keyword_id = kw.get("id")
        keyword_name = kw.get("name", "이름 없음")

        col1, col2 = st.sidebar.columns([4, 1])

        if col1.button(keyword_name, key=f"kw_{keyword_id}", use_container_width=True):
            set_selected_keyword(keyword_id, keyword_name)
            reset_chat()
            st.rerun()

        if col2.button("X", key=f"del_{keyword_id}", use_container_width=True):
            try:
                delete_keyword(keyword_id)
                if st.session_state.get("selected_keyword_id") == keyword_id:
                    st.session_state["selected_keyword_id"] = None
                    st.session_state["selected_keyword_name"] = None
                    reset_chat()
                st.sidebar.success("삭제되었습니다.")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"삭제 실패: {e}")

    st.sidebar.divider()

    new_keyword = st.sidebar.text_input("새 키워드", placeholder="예: 하이닉스")

    if st.sidebar.button("키워드 추가", use_container_width=True):
        if not new_keyword.strip():
            st.sidebar.warning("키워드를 입력해주세요.")
        else:
            try:
                create_keyword(new_keyword.strip())
                st.sidebar.success("키워드가 추가되었습니다.")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"추가 실패: {e}")

    st.sidebar.divider()

    selected_name = st.session_state.get("selected_keyword_name")
    if selected_name:
        st.sidebar.caption(f"현재 선택: {selected_name}")
    else:
        st.sidebar.caption("선택된 키워드 없음")