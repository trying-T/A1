class ChunkService:
    def __init__(self, chunk_size: int = 700, overlap: int = 100) -> None:
        if not 500 <= chunk_size <= 800:
            raise ValueError("chunk_size 必须位于 500 到 800 之间。")
        if overlap >= chunk_size:
            raise ValueError("overlap 必须小于 chunk_size。")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text: str) -> list[dict[str, int | str]]:
        normalized = self._normalize_text(text)
        if not normalized:
            return []

        chunks: list[dict[str, int | str]] = []
        start = 0
        chunk_index = 0
        step = self.chunk_size - self.overlap

        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))
            chunk_text = normalized[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "chunk_text": chunk_text,
                        "chunk_index": chunk_index,
                        "start_offset": start,
                        "end_offset": end,
                    }
                )
                chunk_index += 1

            if end >= len(normalized):
                break
            start += step

        return chunks

    def _normalize_text(self, text: str) -> str:
        return "\n".join(line.rstrip() for line in text.splitlines()).strip()
