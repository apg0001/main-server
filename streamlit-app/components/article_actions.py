import streamlit as st
from api.ai_actions import request_article_summary, request_articles_scoring


def render_article_action_buttons():
    st.subheader("AI 작업")

    selected_article_id = st.session_state.get("selected_article_id")
    selected_article_title = st.session_state.get("selected_article_title")
    article_list = st.session_state.get("articles", [])

    article_ids = [
        article["id"]
        for article in article_list
        if isinstance(article, dict) and article.get("id") is not None
    ]

    col1, col2 = st.columns(2)

    with col1:
        if selected_article_title:
            st.caption(f"선택 기사: {selected_article_title}")
        else:
            st.caption("선택된 기사가 없습니다.")

        summary_disabled = selected_article_id is None

        if st.button("선택 기사 요약", use_container_width=True, disabled=summary_disabled):
            try:
                with st.spinner("기사 요약 생성 중..."):
                    result = request_article_summary(selected_article_id)

                summary = extract_summary_text(result)
                st.session_state["article_summary_result"] = summary
                st.success("기사 요약이 완료되었습니다.")
            except Exception as e:
                st.error(f"요약 요청 실패: {e}")

    with col2:
        st.caption(f"중요도 계산 대상 기사 수: {len(article_ids)}건")

        scoring_disabled = len(article_ids) == 0

        if st.button("전체 기사 중요도 계산", use_container_width=True, disabled=scoring_disabled):
            try:
                with st.spinner("전체 기사 중요도 계산 중..."):
                    result = request_articles_scoring(article_ids)

                scoring_map = extract_scoring_result(result)
                st.session_state["article_scoring_result"] = scoring_map
                st.success("전체 기사 중요도 계산이 완료되었습니다.")
            except Exception as e:
                st.error(f"중요도 계산 실패: {e}")

    if st.session_state.get("article_summary_result"):
        st.markdown("### 요약 결과")
        st.write(st.session_state["article_summary_result"])

    scoring_result = st.session_state.get("article_scoring_result")
    if scoring_result:
        st.markdown("### 중요도 결과")
        st.write(scoring_result)


def extract_summary_text(result):
    if not isinstance(result, dict):
        return "요약 결과를 해석하지 못했습니다."

    data = result.get("data", result)

    if isinstance(data, dict):
        outputs = data.get("outputs", {})
        if isinstance(outputs, dict):
            return (
                outputs.get("summary")
                or outputs.get("result")
                or outputs.get("text")
                or str(outputs)
            )

    return str(data)


def extract_scoring_result(result):
    if not isinstance(result, dict):
        return {"raw": "중요도 결과를 해석하지 못했습니다."}

    data = result.get("data", result)

    if isinstance(data, dict):
        outputs = data.get("outputs", {})
        if isinstance(outputs, dict):
            return (
                outputs.get("scores")
                or outputs.get("results")
                or outputs
            )

    return {"raw": str(data)}