import streamlit as st

from api.client import api_get, api_post


def login(email: str, password: str):
    payload = {
        "email": email,
        "password": password,
    }
    result = api_post("/auth/login", payload, with_auth=False)

    # 실제 LoginResponse는 snake_case
    access_token = result.get("access_token")
    refresh_token = result.get("refresh_token")

    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token

    # 로그인 후 /users/me 따로 조회
    try:
        st.session_state["user"] = get_me()
    except Exception:
        st.session_state["user"] = None

    return result


def logout():
    refresh_token = st.session_state.get("refresh_token")
    if not refresh_token:
        return None
    return api_post("/auth/logout", {"refresh_token": refresh_token})


def get_me():
    return api_get("/users/me")