from typing import Any

from app.core.dify_knowledge_client import DifyKnowledgeClient, DifyKnowledgeClientError
from app.models.article import Article


class DifyUploadError(Exception):
    pass


class DifyArticleUploadService:
    def __init__(self, knowledge_client: DifyKnowledgeClient | None = None) -> None:
        self.knowledge_client = knowledge_client or DifyKnowledgeClient()

    async def upload_article_to_knowledge(self, article: Article) -> dict[str, Any]:
        if not article.content or not article.content.strip():
            raise DifyUploadError(f"article_id={article.id} 본문이 비어 있어 업로드할 수 없습니다.")

        try:
            created = await self.knowledge_client.create_document_by_text(
                title=article.title or f"article-{article.id}",
                text=article.content,
            )

            document_id = created["document_id"]
            batch = created.get("batch")

            await self.knowledge_client.attach_article_id_metadata(
                document_id=document_id,
                article_id=article.id,
            )

            return {
                "article_id": article.id,
                "document_id": document_id,
                "batch": batch,
                "status": "UPLOADED",
            }

        except DifyKnowledgeClientError as e:
            raise DifyUploadError(f"article_id={article.id} Dify 업로드 실패: {e}") from e

    async def upload_articles_to_knowledge(self, articles: list[Article]) -> dict[str, Any]:
        uploaded = []
        failed = []

        for article in articles:
            try:
                result = await self.upload_article_to_knowledge(article)
                uploaded.append(result)
            except Exception as e:
                failed.append(
                    {
                        "article_id": article.id,
                        "status": "FAILED",
                        "reason": str(e),
                    }
                )

        return {
            "uploaded_count": len(uploaded),
            "failed_count": len(failed),
            "uploaded": uploaded,
            "failed": failed,
        }