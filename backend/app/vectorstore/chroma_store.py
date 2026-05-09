import json
import math
from pathlib import Path
from typing import Any

from app.config import VECTOR_DB_DIR


class ChromaStore:
    """Small persistent vector store adapter under data/vector_db/chroma.

    The class keeps the Chroma-facing boundary in place while the project uses a
    lightweight local implementation for MVP validation.
    """

    def __init__(self, persist_dir: Path = VECTOR_DB_DIR) -> None:
        self.persist_dir = persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.store_path = self.persist_dir / "chunks.json"

    def add_chunks(self, chunks: list[dict[str, Any]]) -> int:
        records = self._load_records()
        document_ids = {chunk["document_id"] for chunk in chunks}
        records = [record for record in records if record["document_id"] not in document_ids]
        records.extend(chunks)
        self._save_records(records)
        return len(chunks)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        records = self._load_records()
        scored: list[dict[str, Any]] = []
        for record in records:
            score = self._cosine_similarity(query_embedding, record.get("embedding", []))
            scored.append({**record, "score": score})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def _load_records(self) -> list[dict[str, Any]]:
        if not self.store_path.exists():
            return []
        try:
            payload = json.loads(self.store_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        if not isinstance(payload, list):
            return []
        return payload

    def _save_records(self, records: list[dict[str, Any]]) -> None:
        self.store_path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0
        dot = sum(left_value * right_value for left_value, right_value in zip(left, right))
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)
