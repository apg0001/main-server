from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import update_user_profile
from app.schemas.user import UpdateMeResponse


async def patch_me(
    db: AsyncSession,
    current_user: User,
    update_data: dict,
) -> UpdateMeResponse:
    updated_user = await update_user_profile(
        db=db,
        user=current_user,
        name=update_data.get("name"),
        default_language=update_data.get("default_language"),
        update_name="name" in update_data,
        update_default_language="default_language" in update_data,
    )

    await db.commit()

    return UpdateMeResponse(
        id=updated_user.id,
        email=updated_user.email,
        name=updated_user.name,
        default_language=updated_user.default_language,
        updated_at=updated_user.updated_at,
    )