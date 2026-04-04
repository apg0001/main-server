import streamlit as st

from api.articles import get_importance_list
from api.crawl_runs import get_crawl_runs


def render_summary_cards():
    selected_keyword = st.session_state.get("selected_keyword_name")
    keyword_id = st.session_state.get("selected_keyword_id")
    articles = st.session_state.get("articles", [])

    importance_items = []
    crawl_runs = []

    try:
        importance_items = get_importance_list(keyword_id=keyword_id)
    except Exception:
        pass

    try:
        crawl_runs = get_crawl_runs(page=1, size=5)
    except Exception:
        pass

    st.session_state["importance_items"] = importance_items
    st.session_state["crawl_runs"] = crawl_runs

    article_count = len(articles)
    importance_count = len(importance_items)
    crawl_count = len(crawl_runs)

    col1, col2, col3 = st.columns(3)

    col1.metric("선택 키워드", selected_keyword if selected_keyword else "-")
    col2.metric("기사 수", article_count)
    col3.metric("중요도 결과 수", importance_count)

    st.markdown("### 최근 실행 이력")
    if crawl_runs:
        for run in crawl_runs[:3]:
            run_id = run.get("id", "-")
            status = run.get("status", "UNKNOWN")
            created_at = run.get("createdAt") or run.get("created_at", "")
            st.write(f"- 실행 #{run_id} | 상태: {status} | 생성시각: {created_at}")
    else:
        st.caption("실행 이력이 없습니다.")

    st.markdown("### 중요도 상위 항목")
    if importance_items:
        for item in importance_items[:3]:
            title = item.get("title", "제목 없음")
            score = item.get("score", "-")
            st.write(f"- {title} (점수: {score})")
    else:
        st.caption("중요도 데이터가 없습니다.")