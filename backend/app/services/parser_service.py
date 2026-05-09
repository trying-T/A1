from pathlib import Path


class ParseError(Exception):
    """Raised when a document cannot be parsed into plain text."""


class ParserService:
    def parse_file(self, file_path: Path, file_type: str) -> str:
        if file_type == "pdf":
            return self._parse_pdf(file_path)
        if file_type in {"txt", "markdown"}:
            return self._parse_text_file(file_path)
        raise ParseError(f"暂不支持解析该文件类型：{file_type}")

    def _parse_pdf(self, file_path: Path) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ParseError("解析 PDF 需要安装 pypdf 依赖。") from exc

        reader = PdfReader(str(file_path))
        page_texts: list[str] = []
        for page in reader.pages:
            extracted = (page.extract_text() or "").strip()
            if extracted:
                page_texts.append(extracted)

        text = "\n\n".join(page_texts).strip()
        if not text:
            raise ParseError("PDF 未提取到可用文本，可能是扫描件或图片型文档。")
        return text

    def _parse_text_file(self, file_path: Path) -> str:
        encodings = ("utf-8", "utf-8-sig", "gb18030", "gbk", "utf-16")
        for encoding in encodings:
            try:
                text = file_path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
            if text.strip():
                return text
        raise ParseError("文本文件解码失败，请确认文件编码为 UTF-8、GBK 或 UTF-16。")
