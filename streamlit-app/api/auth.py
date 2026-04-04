import streamlit as st

from api.client import api_get, api_post


def login(email: str, password: str):
    payload = {
        "email": email,
        "password": password,
    }
    result = api_post("/auth/login", payload)

    # 백엔드 응답 구조에 따라 조정 필요
    # 예시:
    # {
    #   "accessToken": "...",
    #   "refreshToken": "...",
    #   "user": {...}
    # }
    access_token = result.get("accessToken") or result.get("access_token")
    refresh_token = result.get("refreshToken") or result.get("refresh_token")
    user = result.get("user")

    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token
    st.session_state["user"] = user

    return result


def get_me():
    return api_get("/users/me")