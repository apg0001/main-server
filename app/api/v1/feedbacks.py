from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter(tags=["feedbacks"])


class FeedbackCreateRequest(BaseModel):
    article_id: int
    action: Literal["LIKE", "DISLIKE"]


class RankingFeedbackRequest(BaseModel):
    article_ids: list[int] = Field(..., min_length=1)
    keyword_id: int | None = None


@router.post("/feedbacks")
async def create_or_update_feedback(
    request: Request,
    body: FeedbackCreateRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "article_id": body.article_id,
            "action": body.action,
            "created": True,
            "updated_at": "2026-02-21T11:10:00Z",
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