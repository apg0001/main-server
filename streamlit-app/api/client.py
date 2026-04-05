import os
from typing import Any, Dict, Optional

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001/api/v1")
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://localhost/v1")
TIMEOUT = 20


class APIError(Exception):
    pass


DIFY_API_KEY = os.getenv("DIFY_API_KEY")

def get_headers(with_auth: bool = True, is_ai: bool = False) -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
    }

    # 👉 AI 서버용
    if is_ai:
        if DIFY_API_KEY:
            headers["Authorization"] = f"Bearer {DIFY_API_KEY}"
        return headers

    # 👉 일반 API용
    if with_auth:
        token = st.session_state.get("access_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    return headers

def unwrap_response(response_json: Dict[str, Any]) -> Any:
    if isinstance(response_json, dict) and "data" in response_json:
        return response_json["data"]
    return response_json


def handle_response(response: requests.Response) -> Any:
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise APIError(f"HTTP {response.status_code}: {detail}") from e

    if not response.text.strip():
        return None

    try:
        result = response.json()
    except Exception as e:
        raise APIError(f"JSON 파싱 실패: {response.text}") from e

    return unwrap_response(result)


def _request(method: str, base_url: str, path: str, *, data=None, params=None, with_auth=True):
    url = f"{base_url}{path}"
    response = requests.request(
        method=method,
        url=url,
        headers=get_headers(with_auth=with_auth),
        json=data,
        params=params,
        timeout=TIMEOUT,
    )
    return handle_response(response)


def api_get(path: str, params: Optional[Dict[str, Any]] = None, with_auth: bool = True) -> Any:
    return _request("GET", BASE_URL, path, params=params, with_auth=with_auth)


def api_post(path: str, data: Optional[Dict[str, Any]] = None, with_auth: bool = True) -> Any:
    return _request("POST", BASE_URL, path, data=data, with_auth=with_auth)


def api_patch(path: str, data: Optional[Dict[str, Any]] = None, with_auth: bool = True) -> Any:
    return _request("PATCH", BASE_URL, path, data=data, with_auth=with_auth)


def api_delete(path: str, with_auth: bool = True) -> Any:
    return _request("DELETE", BASE_URL, path, with_auth=with_auth)


def ai_post(path: str, data=None) -> Any:
    return _request(
        "POST",
        AI_BASE_URL,
        path,
        data=data,
        with_auth=False,   # ❗ JWT 안 씀
        headers=get_headers(is_ai=True)
    )