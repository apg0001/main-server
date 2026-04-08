from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import build_error, ErrorCode
from app.core.transnews_client import TransNewsClient
from app.models.user import User
from app.repositories.keyword_repository import (
    create_keyword,
    delete_keyword,
    get_keyword_by_id,
    get_keyword_by_text,
    list_user_keywords,
    update_keyword_is_active,
)
from app.schemas.keyword import (
    BatchCreateKeywordResponse,
    BatchKeywordItemResult,
    BatchKeywordItemStatus,
    DeleteKeywordResponse,
    KeywordListItem,
    KeywordListResponse,
    KeywordResponse,
    PageInfo,
    UpdateKeywordStatusResponse,
)
from app.services.crawl_run_service import CrawlRunService


async def create_user_keyword(
    db: AsyncSession,
    current_user: User,
    keyword: str,
    language: str | None = None,
) -> KeywordResponse:
    normalized_keyword = keyword.strip()
    if not normalized_keyword:
        raise build_error(
            ErrorCode.VALIDATION_ERROR,
            "keyword is required",
            details=[{"field": "keyword", "reason": "required"}],
        )

    existing_keyword = await get_keyword_by_text(
        db=db,
        user_id=current_user.id,
        keyword_text=normalized_keyword,
    )
    if existing_keyword is not None:
        raise build_error(
            ErrorCode.CONFLICT_DUPLICATE,
            "keyword already exists",
        )

    final_language = language or current_user.default_language

    created_keyword = await create_keyword(
        db=db,
        user_id=current_user.id,
        keyword_text=normalized_keyword,
        language=final_language,
    )

    await db.commit()

    # 최초 1회 크롤링
    try:
        crawl_service = CrawlRunService(
            db=db,
            transnews_client=TransNewsClient(),
        )
        await crawl_service.create_crawl_run(
            user_id=current_user.id,
            keyword_ids=[created_keyword.id],
            force=False,
        )
    except Exception as e:
        print("INITIAL CRAWL FAILED =", e)

    return KeywordResponse(
        id=created_keyword.id,
        keyword=created_keyword.keyword_text,
        language=created_keyword.language,
        is_active=created_keyword.is_active,
        created_at=created_keyword.created_at,
    )