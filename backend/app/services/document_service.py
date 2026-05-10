import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.config import ALLOWED_DOCUMENT_TYPES, PARSED_DOCUMENT_DIR, UPLOAD_DIR
from app.db.session import get_connection
from app.schemas.document_schema import (
    DocumentCreateResponse,
    DocumentItem,
    DocumentListResponse,
    DocumentProcessResponse,
)
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingError, EmbeddingService
from app.services.parser_service import ParseError, ParserService
from app.vectorstore.chroma_store import ChromaStore


class DocumentService:
    def __init__(self) -> None:
        self.upload_root = UPLOAD_DIR
        self.parsed_root = PARSED_DOCUMENT_DIR
        self.parser_service = ParserService()
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaStore()
        self.upload_root.mkdir(parents=True, exist_ok=True)
        self.parsed_root.mkdir(parents=True, exist_ok=True)

    def list_documents(self) -> DocumentListResponse:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT document_id, filename, file_path, file_type, status, upload_time
                FROM documents
                ORDER BY upload_time DESC
                """
            ).fetchall()

        items = [self._row_to_document_item(row) for row in rows]
        return DocumentListResponse(items=items)

    async def save_upload(self, file: UploadFile) -> DocumentCreateResponse:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="上传失败：文件名不能为空。",
            )

        original_name = Path(file.filename).name
        suffix = Path(original_name).suffix.lower()
        file_type = ALLOWED_DOCUMENT_TYPES.get(suffix)
        if file_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="仅支持上传 PDF、TXT、Markdown 文件。",
            )

        document_id = f"doc-{uuid4().hex[:8]}"
        stored_filename = f"{document_id}_{original_name}"
        target_path = self.upload_root / stored_filename
        target_path.write_bytes(await file.read())

        upload_time = datetime.now(timezone.utc).isoformat()
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    document_id, filename, file_path, file_type, status, upload_time, parsed_text_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    original_name,
                    str(target_path),
                    file_type,
                    "uploaded",
                    upload_time,
                    None,
                ),
            )

        item = DocumentItem(
            document_id=document_id,
            filename=original_name,
            file_path=str(target_path),
            file_type=file_type,
            status="uploaded",
            upload_time=upload_time,
        )
        return DocumentCreateResponse(
            **item.model_dump(),
            message="文档上传成功，当前状态为 uploaded。",
        )

    def parse_document(self, document_id: str) -> DocumentProcessResponse:
        document = self._get_document_row(document_id)
        self._clear_document_processing_data(document_id, clear_parsed_path=True)
        file_path = Path(document["file_path"])
        if not file_path.exists():
            message = "未找到原始文件，无法执行解析。"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        try:
            parsed_text = self.parser_service.parse_file(file_path, document["file_type"])
        except ParseError as exc:
            message = f"文档解析失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            ) from exc
        except Exception as exc:
            message = f"文档解析失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            ) from exc

        parsed_path = self.parsed_root / f"{document_id}.txt"
        try:
            parsed_path.write_text(parsed_text, encoding="utf-8")
            with get_connection() as connection:
                connection.execute(
                    """
                    UPDATE documents
                    SET status = ?, parsed_text_path = ?, error_message = ?
                    WHERE document_id = ?
                    """,
                    ("parsed", str(parsed_path), None, document_id),
                )
        except Exception as exc:
            message = f"解析结果写入失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            ) from exc

        return DocumentProcessResponse(
            document_id=document_id,
            status="parsed",
            message="文档解析完成。",
            output_path=str(parsed_path),
        )

    def chunk_document(self, document_id: str) -> DocumentProcessResponse:
        document = self._get_document_row(document_id)
        self._clear_document_processing_data(document_id, clear_parsed_path=False)
        parsed_text_path = document["parsed_text_path"]
        if not parsed_text_path:
            message = "文档尚未解析，请先执行解析。"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )

        parsed_path = Path(parsed_text_path)
        if not parsed_path.exists():
            message = "解析后的文本文件不存在，请重新执行解析。"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        try:
            chunks = self.chunk_service.split_text(parsed_path.read_text(encoding="utf-8"))
        except Exception as exc:
            message = f"文本切分失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            ) from exc
        if not chunks:
            message = "文档内容为空，无法切分。"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )

        try:
            with get_connection() as connection:
                for chunk in chunks:
                    metadata = {
                        "filename": document["filename"],
                        "file_type": document["file_type"],
                        "chunk_size": self.chunk_service.chunk_size,
                        "overlap": self.chunk_service.overlap,
                        "start_offset": chunk["start_offset"],
                        "end_offset": chunk["end_offset"],
                    }
                    connection.execute(
                        """
                        INSERT INTO chunks (
                            chunk_id, document_id, chunk_text, chunk_index, metadata_json
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            f"chk-{uuid4().hex[:12]}",
                            document_id,
                            chunk["chunk_text"],
                            chunk["chunk_index"],
                            json.dumps(metadata, ensure_ascii=False),
                        ),
                    )

                connection.execute(
                    "UPDATE documents SET status = ?, error_message = ? WHERE document_id = ?",
                    ("chunked", None, document_id),
                )
        except Exception as exc:
            message = f"文本切分写入失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            ) from exc

        return DocumentProcessResponse(
            document_id=document_id,
            status="chunked",
            message="文本切分完成，切片已写入 SQLite。",
            chunk_count=len(chunks),
        )

    def index_document(self, document_id: str) -> DocumentProcessResponse:
        document = self._get_document_row(document_id)
        self.vector_store.delete_document(document_id)
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT chunk_id, document_id, chunk_text, chunk_index, metadata_json
                FROM chunks
                WHERE document_id = ?
                ORDER BY chunk_index ASC
                """,
                (document_id,),
            ).fetchall()

        if not rows:
            message = "文档尚未切分，请先执行切分。"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )

        chunk_texts = [row["chunk_text"] for row in rows]
        try:
            embeddings = self.embedding_service.embed_texts(chunk_texts)
        except EmbeddingError as exc:
            message = f"文档向量入库失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=message,
            ) from exc
        records = []
        for row, embedding in zip(rows, embeddings):
            metadata = json.loads(row["metadata_json"])
            metadata.update(
                {
                    "document_id": row["document_id"],
                    "chunk_id": row["chunk_id"],
                    "chunk_index": row["chunk_index"],
                    "filename": document["filename"],
                    "file_type": document["file_type"],
                    "source_type": metadata.get("source_type", "manual"),
                }
            )
            records.append(
                {
                    "chunk_id": row["chunk_id"],
                    "document_id": row["document_id"],
                    "chunk_text": row["chunk_text"],
                    "embedding": embedding,
                    "metadata": metadata,
                }
            )

        try:
            indexed_count = self.vector_store.add_chunks(records)
        except Exception as exc:
            message = f"向量存储写入失败：{exc}"
            self._set_document_failed(document_id, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            ) from exc
        with get_connection() as connection:
            connection.execute(
                "UPDATE documents SET status = ?, error_message = ? WHERE document_id = ?",
                ("indexed", None, document_id),
            )

        return DocumentProcessResponse(
            document_id=document_id,
            status="indexed",
            message="文档向量入库完成。",
            chunk_count=indexed_count,
        )

    def _get_document_row(self, document_id: str) -> dict:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT document_id, filename, file_path, file_type, status, upload_time, parsed_text_path
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到对应文档。",
            )
        return dict(row)

    def _row_to_document_item(self, row: dict) -> DocumentItem:
        return DocumentItem(
            document_id=row["document_id"],
            filename=row["filename"],
            file_path=row["file_path"],
            file_type=row["file_type"],
            status=row["status"],
            upload_time=row["upload_time"],
        )

    def _clear_document_processing_data(self, document_id: str, clear_parsed_path: bool) -> None:
        self.vector_store.delete_document(document_id)
        with get_connection() as connection:
            connection.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            if clear_parsed_path:
                connection.execute(
                    """
                    UPDATE documents
                    SET parsed_text_path = ?, error_message = ?
                    WHERE document_id = ?
                    """,
                    (None, None, document_id),
                )
            else:
                connection.execute(
                    "UPDATE documents SET error_message = ? WHERE document_id = ?",
                    (None, document_id),
                )

    def _set_document_failed(self, document_id: str, message: str) -> None:
        with get_connection() as connection:
            connection.execute(
                "UPDATE documents SET status = ?, error_message = ? WHERE document_id = ?",
                ("failed", message, document_id),
            )
