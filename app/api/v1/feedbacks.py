from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


class ArticleFeedbackRequest(BaseModel):
    action: Literal["LIKE", "DISLIKE"]


class RankingFeedbackRequest(BaseModel):
    article_ids: list[int] = Field(..., min_length=1)
    keyword_id: int | None = None


@router.post("/articles/{article_id}/feedback")
async def create_or_update_feedback(
    article_id: int,
    request: Request,
    body: ArticleFeedbackRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "article_id": article_id,
            "action": body.action,
            "created": True,
            "updated_at": "2026-02-21T11:10:00Z",
        },
    )


@router.get("/articles/{article_id}/feedbacks")
async def get_my_feedback_for_article(
    article_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "article_id": article_id,
            "action": "LIKE",
            "created_at": "2026-02-21T11:10:00Z",
            "updated_at": "2026-02-21T11:12:00Z",
        },
    )


@router.get("/feedbacks/me")
async def get_my_feedbacks(
    request: Request,
    page: int = 1,
    size: int = 20,
    action: Literal["LIKE", "DISLIKE"] | None = None,
    keyword_id: int | None = None,
    q: str | None = None,
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "article_id": 101,
            "action": "LIKE",
            "updated_at": "2026-02-21T11:12:00Z",
            "article": {
                "title": "OpenAI releases new model",
                "url": "https://example.com/articles/101",
                "source": "Example News",
                "published_at": "2026-02-21T09:10:00Z",
                "keyword_id": 12,
                "importance": 0.82,
            },
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


@router.delete("/feedbacks/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "deleted": True,
            "feedback_id": feedback_id,
        },
    )


@router.post("/feedbacks/ranking")
async def create_ranking_feedback(
    request: Request,
    body: RankingFeedbackRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "saved": True,
            "count": len(body.article_ids),
            "created_at": "2026-02-21T12:10:00Z",
        },
    )