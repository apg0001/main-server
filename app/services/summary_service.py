from sqlalchemy.ext.asyncio import AsyncSession

from app.models.summary import Summary

# summary 저장 로직
class SummaryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_summary(
        self,
        *,
        article_id: int,
        summary_text: str,
        language: str = "ko",
        model_name: str = "dify-summary-workflow",
    ) -> Summary:
        row = Summary(
            article_id=article_id,
            summary_text=summary_text,
            language=language,
            model_name=model_name,
        )
        self.db.add(row)
        await self.db.flush()
        return row