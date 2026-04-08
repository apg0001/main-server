from datetime import datetime, timezone
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.importance_score import ImportanceScore

#중요도 저장 로직
class ImportanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_score(
        self,
        *,
        article_id: int,
        user_id: int,
        score: float,
        reason: str | None,
        engine: str = "dify-importance-workflow",
        version: int = 1,
    ) -> ImportanceScore:
        await self.db.execute(
            update(ImportanceScore)
            .where(
                ImportanceScore.article_id == article_id,
                ImportanceScore.user_id == user_id,
                ImportanceScore.is_current.is_(True),
            )
            .values(is_current=False)
        )

        row = ImportanceScore(
            article_id=article_id,
            user_id=user_id,
            score=score,
            reason=reason,
            status="COMPLETED",
            scored_at=datetime.now(timezone.utc),
            engine=engine,
            version=version,
            is_current=True,
        )
        self.db.add(row)
        await self.db.flush()
        return row