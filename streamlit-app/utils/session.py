import streamlit as st


def init_state():
    defaults = {
        "access_token": None,
        "refresh_token": None,
        "user": None,
        "selected_keyword_id": None,
        "selected_keyword_name": None,
        "chat_messages": [],
        "articles": [],
        "importance_items": [],
        "keyword_page_info": None,
        "article_page_info": None,
        "importance_page_info": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_auth_state():
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None
    st.session_state["user"] = None


def set_selected_keyword(keyword_id, keyword_name):
    st.session_state["selected_keyword_id"] = keyword_id
    st.session_state["selected_keyword_name"] = keyword_name


def reset_chat():
    st.session_state["chat_messages"] = []