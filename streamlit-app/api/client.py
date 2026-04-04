import os
from typing import Any, Dict, Optional

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/api/v1")
TIMEOUT = 15


class APIError(Exception):
    pass


def get_headers() -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
    }

    token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def unwrap_response(response_json: Dict[str, Any]) -> Any:
    """
    공통 응답 형식:
    {
      "success": true,
      "data": ...,
      "error": null,
      "meta": ...
    }
    를 가정하고 data만 꺼냄.
    공통 응답 형식이 아니면 원본 그대로 반환.
    """
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


def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    url = f"{BASE_URL}{path}"
    response = requests.get(url, headers=get_headers(), params=params, timeout=TIMEOUT)
    return handle_response(response)


def api_post(path: str, data: Optional[Dict[str, Any]] = None) -> Any:
    url = f"{BASE_URL}{path}"
    response = requests.post(url, headers=get_headers(), json=data, timeout=TIMEOUT)
    return handle_response(response)


def api_patch(path: str, data: Optional[Dict[str, Any]] = None) -> Any:
    url = f"{BASE_URL}{path}"
    response = requests.patch(url, headers=get_headers(), json=data, timeout=TIMEOUT)
    return handle_response(response)


def api_delete(path: str) -> Any:
    url = f"{BASE_URL}{path}"
    response = requests.delete(url, headers=get_headers(), timeout=TIMEOUT)
    return handle_response(response)