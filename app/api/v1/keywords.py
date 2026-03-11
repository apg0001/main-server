from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field, field_validator

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


class CreateKeywordRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100)
    language: Literal["ko", "en"] | None = None


class UpdateKeywordActiveRequest(BaseModel):
    is_active: bool


class BatchKeywordRequest(BaseModel):
    keywords: list[str] = Field(..., min_length=1)
    language: Literal["ko", "en"] | None = None

    @field_validator("keywords")
    @classmethod
    def validate_keywords(cls, value: list[str]) -> list[str]:
        cleaned = [item.strip() for item in value if item.strip()]
        if not cleaned:
            raise ValueError("keywords must not be empty")
        return cleaned


@router.post("")
async def create_keyword(
    request: Request,
    body: CreateKeywordRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        status_code=201,
        data={
            "id": 1,
            "keyword": body.keyword,
            "language": body.language or current_user.default_language,
            "is_active": True,
            "created_at": None,
        },
    )


@router.get("")
async def list_keywords(
    request: Request,
    page: int = 1,
    size: int = 20,
    is_active: bool | None = None,
    language: Literal["ko", "en"] | None = None,
    q: str | None = None,
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "id": 1,
            "keyword": "AI",
            "language": "en",
            "is_active": True,
            "created_at": "2026-02-21T10:20:00Z",
        },
        {
            "id": 2,
            "keyword": "삼성전자",
            "language": "ko",
            "is_active": False,
            "created_at": "2026-02-20T09:15:00Z",
        },
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


@router.patch("/{keyword_id}")
async def update_keyword_active(
    keyword_id: int,
    request: Request,
    body: UpdateKeywordActiveRequest,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "id": keyword_id,
            "keyword": "AI",
            "language": "en",
            "is_active": body.is_active,
            "updated_at": None,
        },
    )


@router.delete("/{keyword_id}")
async def delete_keyword(
    keyword_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "deleted": True,
            "keyword_id": keyword_id,
        },
    )


@router.post("/batch")
async def create_keywords_batch(
    request: Request,
    body: BatchKeywordRequest,
    current_user: User = Depends(get_current_user),
):
    items = [
        {
            "keyword": keyword,
            "status": "CREATED",
            "id": idx + 1,
            "reason": None,
        }
        for idx, keyword in enumerate(body.keywords)
    ]

    return success_response(
        request,
        data={
            "created_count": len(items),
            "skipped_count": 0,
            "items": items,
        },
    )