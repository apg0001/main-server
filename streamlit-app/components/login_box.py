import streamlit as st

from api.auth import login, logout


def render_login_box():
    st.sidebar.subheader("로그인")

    is_logged_in = st.session_state.get("is_logged_in", False)
    user = st.session_state.get("user")

    if is_logged_in:
        st.sidebar.success("로그인됨")

        if user:
            email = user.get("email", "")
            nickname = user.get("nickname") or user.get("name") or ""
            if nickname:
                st.sidebar.caption(f"{nickname} ({email})")
            else:
                st.sidebar.caption(email)

        if st.sidebar.button("로그아웃", use_container_width=True):
            logout()
            st.rerun()

        st.sidebar.divider()
        return

    email = st.sidebar.text_input("이메일", key="login_email")
    password = st.sidebar.text_input("비밀번호", type="password", key="login_password")

    if st.sidebar.button("로그인", use_container_width=True):
        if not email or not password:
            st.sidebar.warning("이메일과 비밀번호를 입력하세요.")
        else:
            try:
                login(email, password)
                st.sidebar.success("로그인 성공")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"로그인 실패: {e}")

    st.sidebar.divider()