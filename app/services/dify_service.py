import httpx

# DB저장은 각각 다른 서비스코드에서 진행
class DifyService:
    def __init__(
        self,
        base_url: str,
        chatflow_api_key: str,
        summary_workflow_api_key: str,
        importance_workflow_api_key: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.chatflow_api_key = chatflow_api_key
        self.summary_workflow_api_key = summary_workflow_api_key
        self.importance_workflow_api_key = importance_workflow_api_key
        self.timeout = timeout

    async def _post(self, path: str, api_key: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 500:
            raise RuntimeError("UPSTREAM_ERROR")

        if response.status_code >= 400:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise RuntimeError(f"DIFY_ERROR: {detail}")

        return response.json()

    async def send_chat_message(
        self,
        *,
        user_id: int,
        message: str,
        conversation_id: str = "",
        article_id: int | None = None,
    ) -> dict:
        inputs = {
            "user_id": user_id,
        }
        if article_id is not None:
            inputs["article_id"] = article_id

        payload = {
            "inputs": inputs,
            "query": message,
            "conversation_id": conversation_id or "",
            "response_mode": "blocking",
            "user": str(user_id),
        }

        data = await self._post("/chat-messages", self.chatflow_api_key, payload)

        return {
            "answer": data.get("answer", ""),
            "conversation_id": data.get("conversation_id"),
            "raw": data,
        }

    async def run_summary_workflow(
        self,
        *,
        user_id: int,
        article_id: int,
        title: str,
        content: str,
        publisher: str | None = None,
        published_at: str | None = None,
    ) -> dict:
        payload = {
            "inputs": {
                "user_id": user_id,
                "article_id": article_id,
                "title": title,
                "content": content,
                "publisher": publisher,
                "published_at": published_at,
            },
            "response_mode": "blocking",
            "user": str(user_id),
        }

        data = await self._post("/workflows/run", self.summary_workflow_api_key, payload)
        result_data = data.get("data") or {}
        outputs = result_data.get("outputs") or {}

        return {
            "workflow_run_id": result_data.get("workflow_run_id"),
            "task_id": result_data.get("task_id"),
            "outputs": outputs,
            "raw": data,
        }

    async def run_importance_workflow(
        self,
        *,
        user_id: int,
        article_id: int,
        title: str,
        content: str,
        publisher: str | None = None,
        published_at: str | None = None,
        keyword: str | None = None,
    ) -> dict:
        payload = {
            "inputs": {
                "user_id": user_id,
                "article_id": article_id,
                "title": title,
                "content": content,
                "publisher": publisher,
                "published_at": published_at,
                "keyword": keyword,
            },
            "response_mode": "blocking",
            "user": str(user_id),
        }

        data = await self._post("/workflows/run", self.importance_workflow_api_key, payload)
        result_data = data.get("data") or {}
        outputs = result_data.get("outputs") or {}

        return {
            "workflow_run_id": result_data.get("workflow_run_id"),
            "task_id": result_data.get("task_id"),
            "outputs": outputs,
            "raw": data,
        }