from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_refresh_token import AuthRefreshToken


async def create_refresh_token_record(
    db: AsyncSession,
    user_id: int,
    refresh_token: str,
    expires_at,
) -> AuthRefreshToken:
    token_record = AuthRefreshToken(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=expires_at,
        is_revoked=False,
    )
    db.add(token_record)
    await db.flush()
    return token_record


async def get_refresh_token_record(
    db: AsyncSession,
    refresh_token: str,
) -> AuthRefreshToken | None:
    result = await db.execute(
        select(AuthRefreshToken).where(
            AuthRefreshToken.refresh_token == refresh_token
        )
    )
    return result.scalar_one_or_none()


async def revoke_refresh_token(
    db: AsyncSession,
    token_record: AuthRefreshToken,
) -> None:
    token_record.is_revoked = True
    token_record.revoked_at = datetime.now(timezone.utc)
    await db.flush()


async def delete_refresh_token(
    db: AsyncSession,
    token_record: AuthRefreshToken,
) -> None:
    await db.delete(token_record)
    await db.flush()


async def revoke_all_user_refresh_tokens(
    db: AsyncSession,
    user_id: int,
) -> None:
    result = await db.execute(
        select(AuthRefreshToken).where(
            AuthRefreshToken.user_id == user_id,
            AuthRefreshToken.is_revoked == False,  # noqa: E712
        )
    )
    tokens = result.scalars().all()
    now = datetime.now(timezone.utc)
    for token in tokens:
        token.is_revoked = True
        token.revoked_at = now
    await db.flush()