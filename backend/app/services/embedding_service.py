import hashlib
import json
import math
import re
import urllib.error
import urllib.request

from app.config import (
    EMBEDDING_API_KEY,
    EMBEDDING_BASE_URL,
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    EMBEDDING_TIMEOUT_SECONDS,
)


class EmbeddingError(Exception):
    """Raised when the configured embedding provider cannot return vectors."""


class EmbeddingService:
    def __init__(
        self,
        provider: str = EMBEDDING_PROVIDER,
        base_url: str = EMBEDDING_BASE_URL,
        api_key: str = EMBEDDING_API_KEY,
        model: str = EMBEDDING_MODEL,
        timeout_seconds: float = EMBEDDING_TIMEOUT_SECONDS,
        mock_dimension: int = 256,
    ) -> None:
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = "mock-hash-embedding" if provider == "mock" else model
        self.timeout_seconds = timeout_seconds
        self.mock_dimension = mock_dimension

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if self.provider == "mock":
            return [self._mock_embed_text(text) for text in texts]
        if self.provider in {"siliconflow", "openai_compatible"}:
            return self._embed_texts_openai_compatible(texts)
        raise EmbeddingError(f"Unsupported embedding provider ({self._provider_label()})")

    def provider_info(self) -> dict[str, str]:
        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
        }

    def _embed_texts_openai_compatible(self, texts: list[str]) -> list[list[float]]:
        if not self.base_url:
            raise EmbeddingError(f"Missing EMBEDDING_BASE_URL ({self._provider_label()})")
        if not self.api_key:
            raise EmbeddingError(f"Missing EMBEDDING_API_KEY ({self._provider_label()})")
        if not self.model:
            raise EmbeddingError(f"Missing EMBEDDING_MODEL ({self._provider_label()})")

        endpoint = f"{self.base_url}/embeddings"
        payload = json.dumps({"model": self.model, "input": texts}).encode("utf-8")
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
            raise EmbeddingError(
                f"Embedding API request failed ({self._provider_label()}): HTTP {exc.code} {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise EmbeddingError(
                f"Embedding API connection failed ({self._provider_label()}): {exc.reason}"
            ) from exc

        data = response_payload.get("data")
        if not isinstance(data, list):
            raise EmbeddingError(f"Embedding API response missing data array ({self._provider_label()})")

        ordered_data = sorted(data, key=lambda item: item.get("index", 0))
        embeddings = [item.get("embedding") for item in ordered_data]
        if len(embeddings) != len(texts) or any(not isinstance(item, list) for item in embeddings):
            raise EmbeddingError(f"Embedding API returned invalid vector count or format ({self._provider_label()})")
        return embeddings

    def _provider_label(self) -> str:
        return f"provider={self.provider}, model={self.model}"

    def _mock_embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.mock_dimension
        tokens = self._tokenize(text)
        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.mock_dimension
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    def _tokenize(self, text: str) -> list[str]:
        normalized = re.sub(r"\s+", "", text.lower())
        if not normalized:
            return []

        tokens = list(normalized)
        tokens.extend(normalized[index : index + 2] for index in range(len(normalized) - 1))
        tokens.extend(normalized[index : index + 3] for index in range(len(normalized) - 2))
        return tokens
