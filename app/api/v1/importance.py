from typing import Literal

from fastapi import APIRouter, Depends, Request

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


@router.get("")
async def list_importance(
    request: Request,
    page: int = 1,
    size: int = 20,
    keyword_id: int | None = None,
    from_date: str | None = None,
    to: str | None = None,
    min_score: float | None = None,
    max_score: float | None = None,
    status: Literal["PENDING", "PROCESSING", "COMPLETED", "FAILED"] | None = None,
    sort: Literal["scored_at_desc", "scored_at_asc", "score_desc", "score_asc"] = "scored_at_desc",
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "article_id": 101,
            "title": "OpenAI releases new model",
            "url": "https://example.com/articles/101",
            "keyword_id": 12,
            "score": 0.82,
            "status": "COMPLETED",
            "scored_at": "2026-02-21T10:40:00Z",
            "created_at": "2026-02-21T10:39:10Z",
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


@router.get("/articles/{article_id}/importance")
async def get_article_importance(
    article_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "article_id": article_id,
            "status": "COMPLETED",
            "score": 0.82,
            "model": "importance-v1",
            "scored_at": "2026-02-21T10:40:00Z",
            "created_at": "2026-02-21T10:39:10Z",
            "updated_at": "2026-02-21T10:40:00Z",
        },
    )