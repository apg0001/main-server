from datetime import datetime
from typing import Any
from email.utils import parsedate_to_datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.transnews_client import TransNewsClient
from app.models.crawl_run import CrawlRun
from app.models.crawl_run_keyword import CrawlRunKeyword
from app.models.article import Article
from app.models.article_match import ArticleMatch
from app.models.summary import Summary
from app.models.keyword import Keyword
from app.services.dify_service import DifyArticleUploadService


class CrawlRunService:
    def __init__(
        self,
        db: AsyncSession,
        transnews_client: TransNewsClient,
        dify_upload_service: DifyArticleUploadService | None = None,
    ):
        self.db = db
        self.transnews_client = transnews_client
        self.dify_upload_service = dify_upload_service or DifyArticleUploadService()

    async def create_crawl_run(
        self,
        *,
        user_id: int,
        keyword_ids: list[int] | None = None,
        force: bool = False,
    ) -> dict[str, Any]:
        keywords = await self._get_user_keywords(user_id=user_id, keyword_ids=keyword_ids)
        if not keywords:
            raise ValueError("크롤링할 키워드가 없습니다.")

        crawl_run = CrawlRun(
            user_id=user_id,
            status="RUNNING",
            force_run=force,
            article_count=0,
            started_at=datetime.utcnow(),
        )
        self.db.add(crawl_run)
        await self.db.flush()

        for keyword in keywords:
            self.db.add(CrawlRunKeyword(crawl_run_id=crawl_run.id, keyword_id=keyword.id))

        article_count = 0
        newly_created_articles: list[Article] = []

        for keyword in keywords:
            news_response = await self.transnews_client.search_news(keyword.keyword_text)
            print("NEWS RESPONSE =", news_response)

            if news_response.get("status") != "SUCCESS":
                print("SKIP: news search failed =", news_response)
                continue

            news_items = news_response.get("data") or []
            print("NEWS ITEMS COUNT =", len(news_items))

            for item in news_items:
                article, is_new = await self._upsert_article(item)
                print("UPSERT RESULT =", article, "IS_NEW =", is_new)

                if article is None:
                    print("SKIP: article is None")
                    continue

                await self._ensure_article_match(
                    article_id=article.id,
                    keyword_id=keyword.id,
                    crawl_run_id=crawl_run.id,
                )

                if is_new:
                    newly_created_articles.append(article)

                article_count += 1

        dify_result = await self._upload_new_articles_to_dify(newly_created_articles)

        crawl_run.status = "COMPLETED"
        crawl_run.article_count = article_count
        crawl_run.finished_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(crawl_run)

        return {
            "crawl_run_id": crawl_run.id,
            "status": crawl_run.status,
            "article_count": crawl_run.article_count,
            "new_article_count": len(newly_created_articles),
            "dify_uploaded_count": dify_result["uploaded_count"],
            "dify_failed_count": dify_result["failed_count"],
            "dify_failed_items": dify_result["failed"],
        }

    async def crawl_active_keywords(self) -> list[dict[str, Any]]:
        from sqlalchemy import select
        from app.models.user import User

        result = await self.db.execute(select(User.id).distinct())
        user_ids = [row[0] for row in result.all()]

        outcomes: list[dict[str, Any]] = []

        for user_id in user_ids:
            try:
                keywords = await self._get_user_keywords(user_id=user_id, keyword_ids=None)
                if not keywords:
                    continue

                outcome = await self.create_crawl_run(
                    user_id=user_id,
                    keyword_ids=[k.id for k in keywords],
                    force=False,
                )
                outcomes.append(
                    {
                        "user_id": user_id,
                        "status": "COMPLETED",
                        "result": outcome,
                    }
                )
            except Exception as e:
                outcomes.append(
                    {
                        "user_id": user_id,
                        "status": "FAILED",
                        "reason": str(e),
                    }
                )

        return outcomes

    async def _get_user_keywords(self, *, user_id: int, keyword_ids: list[int] | None):
        from sqlalchemy import select

        stmt = select(Keyword).where(
            Keyword.user_id == user_id,
            Keyword.is_active.is_(True),
        )
        if keyword_ids:
            stmt = stmt.where(Keyword.id.in_(keyword_ids))

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def _upsert_article(self, item: dict[str, Any]) -> tuple[Article | None, bool]:
        from sqlalchemy import select

        url = item.get("url") or item.get("link")
        published_raw = item.get("published_at") or item.get("published")

        published_at = None
        if published_raw:
            try:
                published_at = parsedate_to_datetime(published_raw)
            except Exception as e:
                print("DATE PARSE FAILED =", published_raw, e)

        if not url:
            print("SKIP IN UPSERT: url is missing")
            return None, False

        title = item.get("title") or "제목 없음"
        publisher = item.get("publisher") or item.get("source")
        language = item.get("language") or "ko"

        result = await self.db.execute(select(Article).where(Article.url == url))
        article = result.scalar_one_or_none()

        if article:
            print("EXISTING ARTICLE FOUND, id =", article.id)
            article.title = title
            article.publisher = publisher
            article.source_type = article.source_type or "TRANSNEWS"
            article.language = article.language or language
            if published_at is not None:
                article.published_at = published_at
            return article, False

        article = Article(
            source_type="TRANSNEWS",
            source_article_id=None,
            url=url,
            title=title,
            publisher=publisher,
            published_at=published_at,
            content=item.get("content") or "",
            language=language,
        )
        self.db.add(article)
        await self.db.flush()

        print("NEW ARTICLE INSERTED, id =", article.id)
        return article, True

    async def _ensure_article_match(self, *, article_id: int, keyword_id: int, crawl_run_id: int):
        from sqlalchemy import select

        result = await self.db.execute(
            select(ArticleMatch).where(
                ArticleMatch.article_id == article_id,
                ArticleMatch.keyword_id == keyword_id,
            )
        )
        match = result.scalar_one_or_none()

        if match is None:
            self.db.add(
                ArticleMatch(
                    article_id=article_id,
                    keyword_id=keyword_id,
                    crawl_run_id=crawl_run_id,
                )
            )
            print(f"ARTICLE MATCH ADDED: article_id={article_id}, keyword_id={keyword_id}")
        else:
            print(f"ARTICLE MATCH EXISTS: article_id={article_id}, keyword_id={keyword_id}")

    async def _upload_new_articles_to_dify(self, articles: list[Article]) -> dict[str, Any]:
        if not articles:
            return {
                "uploaded_count": 0,
                "failed_count": 0,
                "uploaded": [],
                "failed": [],
            }

        return await self.dify_upload_service.upload_articles_to_knowledge(articles)

    async def _upsert_summary(self, article_id: int, summary_text: str):
        from sqlalchemy import select

        result = await self.db.execute(
            select(Summary).where(
                Summary.article_id == article_id,
                Summary.language == "ko",
            )
        )
        summary = result.scalar_one_or_none()

        if summary:
            summary.summary_text = summary_text
            summary.model_name = "transnews-pipeline"
            print(f"SUMMARY UPDATED: article_id={article_id}")
            return

        self.db.add(
            Summary(
                article_id=article_id,
                language="ko",
                summary_text=summary_text,
                model_name="transnews-pipeline",
            )
        )
        print(f"SUMMARY ADDED: article_id={article_id}")