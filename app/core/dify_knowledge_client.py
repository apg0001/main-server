from typing import Any

import httpx

from app.core.config import settings


class DifyKnowledgeClientError(Exception):
    pass


class DifyKnowledgeClient:
    def __init__(self) -> None:
        self.base_url = settings.dify_base_url.rstrip("/")
        self.timeout = settings.dify_request_timeout
        self.dataset_id = settings.dify_dataset_id
        self.metadata_field_id = settings.dify_article_id_metadata_field_id
        self.api_key = settings.knowledge_api_key

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=self._headers(), json=json_body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise DifyKnowledgeClientError(f"Knowledge 호출 실패: {detail}") from e

        return response.json()

    async def _get(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, headers=self._headers())

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise DifyKnowledgeClientError(f"Knowledge 조회 실패: {detail}") from e

        return response.json()

    async def create_document_by_text(self, *, title: str, text: str) -> dict[str, Any]:
        result = await self._post(
            f"/datasets/{self.dataset_id}/documents/create-by-text",
            {
                "name": title,
                "text": text,
                "indexing_technique": "high_quality",
                "process_rule": {
                    "mode": "automatic",
                },
            },
        )

        data = result.get("data") or {}
        document_id = data.get("document_id")
        batch = data.get("batch")

        if not document_id:
            raise DifyKnowledgeClientError("document_id를 받지 못했습니다.")

        return {
            "document_id": document_id,
            "batch": batch,
            "raw": result,
        }

    async def attach_article_id_metadata(self, *, document_id: str, article_id: int) -> None:
        await self._post(
            f"/datasets/{self.dataset_id}/documents/metadata",
            {
                "operation_data": [
                    {
                        "document_id": document_id,
                        "metadata_list": [
                            {
                                "id": self.metadata_field_id,
                                "name": "article_id",
                                "value": article_id,
                            }
                        ],
                    }
                ]
            },
        )

    async def get_indexing_status(self, *, batch: str) -> dict[str, Any]:
        return await self._get(
            f"/datasets/{self.dataset_id}/documents/{batch}/indexing-status"
        )