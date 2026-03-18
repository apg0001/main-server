import httpx

from app.core.config import settings


class DifyService:
    def __init__(self):
        self.base_url = settings.DIFY_BASE_URL.rstrip("/")
        self.api_key = settings.DIFY_API_KEY
        self.timeout = settings.DIFY_REQUEST_TIMEOUT

    async def send_chat_message(
        self,
        query: str,
        user: str,
        conversation_id: str | None = None,
        inputs: dict | None = None,
    ) -> dict:
        url = f"{self.base_url}/chat-messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "query": query,
            "user": user,
            "inputs": inputs or {},
            "response_mode": "blocking",
        }

        if conversation_id:
            payload["conversation_id"] = conversation_id

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 500:
            raise RuntimeError("UPSTREAM_ERROR")

        if response.status_code >= 400:
            raise RuntimeError(f"DIFY_ERROR:{response.status_code}:{response.text}")

        data = response.json()

        return {
            "conversation_id": data.get("conversation_id"),
            "message_id": data.get("message_id"),
            "answer": data.get("answer"),
            "created_at": data.get("created_at"),
            "raw": data,
        }