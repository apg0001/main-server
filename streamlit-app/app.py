import os

import streamlit as st
from dotenv import load_dotenv

from components.article_list import render_article_list
from components.chat_box import render_chat_box
from components.sidebar import LOGIN_DISABLED, render_sidebar
from components.summary_cards import render_summary_cards
from utils.session import init_state

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "AI Agent 기반 기사 모니터링")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📰",
    layout="wide",
)

init_state()


def render_header():
    st.title(APP_TITLE)
    st.caption("메인서버 + AI서버 연동 Streamlit 화면")

    if not LOGIN_DISABLED and not st.session_state.get("is_logged_in"):
        st.warning("왼쪽 사이드바에서 로그인하세요.")
        return

    selected_keyword = st.session_state.get("selected_keyword_name")
    if selected_keyword:
        st.info(f"현재 선택된 키워드: {selected_keyword}")
    else:
        st.warning("왼쪽 사이드바에서 키워드를 선택하세요.")


def main():
    render_sidebar()
    render_header()

    if not st.session_state.get("is_logged_in"):
        st.stop()

    left, right = st.columns([3, 2])

    with left:
        st.markdown("## 무엇을 도와드릴까요?")
        render_chat_box()

    with right:
        render_summary_cards()

    st.markdown("---")
    render_article_list()


if __name__ == "__main__":
    main()