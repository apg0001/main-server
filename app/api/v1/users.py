from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core.deps import get_current_user
from app.core.response import success_response
from app.models.user import User

router = APIRouter()


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    default_language: Literal["ko", "en"] | None = None


@router.get("/me")
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return success_response(
        request,
        data={
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        },
    )


@router.patch("/me")
async def update_me(
    request: Request,
    body: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
):
    # TODO: 실제 DB update 연결
    updated_name = body.name if body.name is not None else current_user.name
    updated_language = (
        body.default_language if body.default_language is not None else current_user.default_language
    )

    return success_response(
        request,
        data={
            "id": current_user.id,
            "email": current_user.email,
            "name": updated_name,
            "default_language": updated_language,
            "updated_at": None,
        },
    )