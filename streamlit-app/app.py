import os

import streamlit as st
from dotenv import load_dotenv

from components.article_list import render_article_list
from components.chat_box import render_chat_box
from components.sidebar import render_sidebar
from components.summary_cards import render_summary_cards
from utils.session import init_state

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "AI 기반 기사 모니터링")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📰",
    layout="wide",
)

init_state()


def render_header():
    st.title(APP_TITLE)
    st.caption("키워드 기반 기사 조회 및 AI 채팅 대시보드")

    selected_keyword = st.session_state.get("selected_keyword_name")
    if selected_keyword:
        st.info(f"현재 선택된 키워드: {selected_keyword}")
    else:
        st.warning("왼쪽 사이드바에서 키워드를 선택하세요.")


def main():
    render_sidebar()
    render_header()

    top_col1, top_col2 = st.columns([3, 2])

    with top_col1:
        st.markdown("## 무엇을 도와드릴까요?")
        render_chat_box()

    with top_col2:
        render_summary_cards()

    st.markdown("---")
    render_article_list()


if __name__ == "__main__":
    main()