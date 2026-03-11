from typing import Literal

from fastapi import APIRouter, Depends, Request

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


@router.get("/articles")
async def list_articles(
    request: Request,
    page: int = 1,
    size: int = 20,
    keyword_id: int | None = None,
    q: str | None = None,
    language: Literal["ko", "en"] | None = None,
    from_date: str | None = None,
    to: str | None = None,
    min_importance: float | None = None,
    max_importance: float | None = None,
    has_feedback: bool | None = None,
    liked: bool | None = None,
    sort: Literal[
        "published_at_desc",
        "published_at_asc",
        "importance_desc",
        "importance_asc",
    ] = "published_at_desc",
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "id": 101,
            "title": "OpenAI releases new model",
            "summary": "A new model was announced with improved reasoning performance.",
            "url": "https://example.com/articles/101",
            "source": "Example News",
            "language": "en",
            "published_at": "2026-02-21T09:10:00Z",
            "keyword_id": 12,
            "importance": 0.82,
            "is_liked": True,
            "has_feedback": False,
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


@router.get("/articles/{article_id}")
async def get_article_detail(
    article_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "id": article_id,
            "title": "OpenAI releases new model",
            "summary": "A new model was announced with improved reasoning performance.",
            "content": "Full article content ...",
            "url": "https://example.com/articles/101",
            "source": "Example News",
            "language": "en",
            "published_at": "2026-02-21T09:10:00Z",
            "keyword_id": 12,
            "importance": 0.82,
            "is_liked": True,
            "has_feedback": False,
            "created_at": "2026-02-21T09:12:30Z",
        },
    )