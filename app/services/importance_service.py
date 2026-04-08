from datetime import datetime, timezone
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.importance_score import ImportanceScore
from app.repositories.importance_repository import ImportanceRepository
from app.repositories.article_repository import ArticleRepository


class ImportanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.importance_repository = ImportanceRepository(db)
        self.article_repository = ArticleRepository(db)

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

    async def get_importance_list(self, user_id: int, query):
        return await self.importance_repository.get_importance_list(
            user_id=user_id,
            query=query,
        )

    async def get_article_importance(self, user_id: int, article_id: int):
        await self.article_repository.validate_articles_exist_and_accessible(
            user_id=user_id,
            article_ids=[article_id],
        )

        result = await self.importance_repository.get_current_score(
            user_id=user_id,
            article_id=article_id,
        )

        if result is None:
            return {
                "article_id": article_id,
                "score": None,
                "reason": None,
                "status": "NOT_FOUND",
            }

        return result

    async def run_importance_scoring(self, user_id: int, article_ids: list[int]):
        await self.article_repository.validate_articles_exist_and_accessible(
            user_id=user_id,
            article_ids=article_ids,
        )

        articles = await self.article_repository.get_articles_for_importance_scoring(
            user_id=user_id,
            article_ids=article_ids,
        )

        saved_items = []
        for article in articles:
            row = await self.save_score(
                article_id=article["article_id"],
                user_id=user_id,
                score=0.5,
                reason="temporary default score",
            )
            saved_items.append(
                {
                    "article_id": row.article_id,
                    "score": row.score,
                    "status": row.status,
                    "reason": row.reason,
                }
            )

        return {
            "items": saved_items,
            "count": len(saved_items),
        }