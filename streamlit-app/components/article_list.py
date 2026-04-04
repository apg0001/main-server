import streamlit as st

from api.articles import get_article_detail, get_articles


def render_article_list():
    st.subheader("기사 목록")

    keyword_id = st.session_state.get("selected_keyword_id")
    articles = get_articles(keyword_id=keyword_id, page=1, size=10)
    st.session_state["articles"] = articles

    if not articles:
        st.info("표시할 기사가 없습니다.")
        return

    for article in articles:
        article_id = article.get("id")
        title = article.get("title", "제목 없음")
        source = article.get("source", "출처 없음")
        published_at = article.get("publishedAt") or article.get("published_at", "")
        summary = article.get("summary", "")
        url = article.get("url", "")

        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(f"{source} | {published_at}")

            if summary:
                st.write(summary)

            col1, col2 = st.columns([1, 1])

            if col1.button("상세 보기", key=f"detail_{article_id}"):
                try:
                    detail = get_article_detail(article_id)
                    st.session_state[f"article_detail_{article_id}"] = detail
                except Exception as e:
                    st.error(f"상세 조회 실패: {e}")

            if url:
                col2.link_button("원문 링크", url)

            detail_data = st.session_state.get(f"article_detail_{article_id}")
            if detail_data:
                st.markdown("---")
                st.write(detail_data)