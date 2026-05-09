import json
import urllib.error
import urllib.request

from app.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_TIMEOUT_SECONDS,
)


class LLMError(Exception):
    """Raised when the configured chat completion provider fails."""


OPENAI_COMPATIBLE_PROVIDERS = {"siliconflow", "openai_compatible", "deepseek"}


class LLMService:
    def __init__(
        self,
        provider: str = LLM_PROVIDER,
        base_url: str = LLM_BASE_URL,
        api_key: str = LLM_API_KEY,
        model: str = LLM_MODEL,
        timeout_seconds: float = LLM_TIMEOUT_SECONDS,
    ) -> None:
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate_chat_completion(self, messages: list[dict]) -> str:
        if self.provider not in OPENAI_COMPATIBLE_PROVIDERS:
            raise LLMError(
                "请配置 LLM_PROVIDER=siliconflow、deepseek 或 openai_compatible 后再调用 RAG 问答。"
            )
        if not self.base_url:
            raise LLMError("真实 LLM 调用需要配置 LLM_BASE_URL。")
        if not self.api_key:
            raise LLMError("真实 LLM 调用需要配置 LLM_API_KEY。")
        if not self.model:
            raise LLMError("真实 LLM 调用需要配置 LLM_MODEL。")

        endpoint = f"{self.base_url}/chat/completions"
        payload = json.dumps(
            {
                "model": self.model,
                "messages": messages,
                "temperature": 0.2,
            },
            ensure_ascii=False,
        ).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise LLMError(f"LLM API 请求失败：HTTP {exc.code} {detail}") from exc
        except urllib.error.URLError as exc:
            raise LLMError(f"LLM API 连接失败：{exc.reason}") from exc

        choices = response_payload.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMError("LLM API 返回格式缺少 choices。")

        message = choices[0].get("message", {})
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError("LLM API 返回内容为空。")
        return content.strip()

    def provider_info(self) -> dict[str, str]:
        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
        }
