import streamlit as st

from api.articles import (
    delete_article_feedback,
    get_article_detail,
    get_article_importance,
    get_articles,
    upsert_article_feedback,
)


def render_article_list():
    st.subheader("기사 목록")

    keyword_id = st.session_state.get("selected_keyword_id")

    try:
        articles, page_info = get_articles(keyword_id=keyword_id, page=1, size=10)
        st.session_state["articles"] = articles
        st.session_state["article_page_info"] = page_info
    except Exception as e:
        st.error(f"기사 목록 조회 실패: {e}")
        return

    if not articles:
        st.info("표시할 기사가 없습니다.")
        return

    for article in articles:
        article_id = article.get("id")
        title = article.get("title", "제목 없음")
        source = article.get("source", "출처 없음")
        published_at = article.get("published_at", "")
        summary = article.get("summary", "")
        url = article.get("url", "")
        importance = article.get("importance")
        is_liked = article.get("is_liked", False)
        has_feedback = article.get("has_feedback", False)

        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(f"{source} | {published_at}")

            if importance is not None:
                st.write(f"중요도: {importance}")

            if summary:
                st.write(summary)

            col1, col2, col3, col4, col5 = st.columns(5)

            if col1.button("상세", key=f"detail_{article_id}"):
                try:
                    st.session_state[f"article_detail_{article_id}"] = get_article_detail(article_id)
                except Exception as e:
                    st.error(f"상세 조회 실패: {e}")

            if col2.button("중요도", key=f"importance_{article_id}"):
                try:
                    st.session_state[f"article_importance_{article_id}"] = get_article_importance(article_id)
                except Exception as e:
                    st.error(f"중요도 조회 실패: {e}")

            if col3.button("좋아요", key=f"like_{article_id}"):
                try:
                    upsert_article_feedback(article_id, "LIKE")
                    st.rerun()
                except Exception as e:
                    st.error(f"피드백 저장 실패: {e}")

            if col4.button("싫어요", key=f"dislike_{article_id}"):
                try:
                    upsert_article_feedback(article_id, "DISLIKE")
                    st.rerun()
                except Exception as e:
                    st.error(f"피드백 저장 실패: {e}")

            if has_feedback and col5.button("피드백 삭제", key=f"delete_feedback_{article_id}"):
                try:
                    delete_article_feedback(article_id)
                    st.rerun()
                except Exception as e:
                    st.error(f"피드백 삭제 실패: {e}")

            if url:
                st.link_button("원문 링크", url)

            detail_data = st.session_state.get(f"article_detail_{article_id}")
            if detail_data:
                st.markdown("##### 기사 상세")
                st.json(detail_data)

            importance_data = st.session_state.get(f"article_importance_{article_id}")
            if importance_data:
                st.markdown("##### 중요도 상세")
                st.json(importance_data)

            if has_feedback:
                st.caption(f"내 피드백 있음 / 좋아요 여부: {is_liked}")