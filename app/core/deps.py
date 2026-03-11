#'현재 로그인한 사용자'를 가져오는 인증 의존성(dependency)를 구현한 것
# 요청에 포함된 JWT 토큰 검증 -> 해당 유저 DB에서 조회 -> 라우터에 User객체를 전달하는 코드
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ErrorCode, build_error
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)

 
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if credentials is None:
        raise build_error(ErrorCode.AUTH_REQUIRED, "Authentication required")

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except JWTError:
        raise build_error(ErrorCode.AUTH_REQUIRED, "Authentication required")

    user_id = payload.get("sub")
    token_type = payload.get("type")

    if not user_id or token_type != "access":
        raise build_error(ErrorCode.AUTH_REQUIRED, "Authentication required")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise build_error(ErrorCode.AUTH_REQUIRED, "Authentication required")

    return user