from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


class CreateChatRequest(BaseModel):
    title: str | None = None
    context_type: Literal["GENERAL", "NEWS_ANALYSIS", "ARTICLE_QA"] = "GENERAL"


class SendMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    article_ids: list[int] | None = None


@router.post("")
async def create_chat(
    request: Request,
    body: CreateChatRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        status_code=201,
        data={
            "id": 21,
            "title": body.title,
            "context_type": body.context_type,
            "created_at": "2026-02-21T13:10:00Z",
        },
    )


@router.get("")
async def list_chats(
    request: Request,
    page: int = 1,
    size: int = 20,
    q: str | None = None,
    context_type: Literal["GENERAL", "NEWS_ANALYSIS", "ARTICLE_QA"] | None = None,
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "id": 21,
            "title": "AI 뉴스 분석",
            "context_type": "NEWS_ANALYSIS",
            "last_message": "오늘 주요 AI 뉴스 정리해줘",
            "last_message_at": "2026-02-21T13:20:00Z",
            "created_at": "2026-02-21T13:10:00Z",
        }
    ]

    return success_response(
        request,
        data={
            "items": items,
            "page_info": {
                "page": page,
                "size": size,
                "total": len(items),
                "has_next": False,
            },
        },
    )


@router.get("/{chat_id}")
async def get_chat_detail(
    chat_id: int,
    request: Request,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "id": chat_id,
            "title": "AI 뉴스 분석",
            "context_type": "NEWS_ANALYSIS",
            "created_at": "2026-02-21T13:10:00Z",
            "messages": {
                "items": [
                    {
                        "id": 301,
                        "role": "USER",
                        "content": "오늘 주요 AI 뉴스 정리해줘",
                        "created_at": "2026-02-21T13:20:00Z",
                    },
                    {
                        "id": 302,
                        "role": "ASSISTANT",
                        "content": "오늘 주요 AI 뉴스는 다음과 같습니다...",
                        "created_at": "2026-02-21T13:20:05Z",
                    },
                ],
                "page_info": {
                    "page": page,
                    "size": size,
                    "total": 2,
                    "has_next": False,
                },
            },
        },
    )


@router.post("/{chat_id}/messages")
async def send_message(
    chat_id: int,
    request: Request,
    body: SendMessageRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "user_message_id": 501,
            "assistant_message_id": 502,
            "answer": "오늘 주요 AI 뉴스는 다음과 같습니다. 첫째, OpenAI가 새로운 모델을 발표했습니다...",
            "created_at": "2026-02-21T14:05:00Z",
        },
    )