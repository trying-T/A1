from app.schemas.common_schema import SourceItem
from app.schemas.retrieval_schema import RetrievalSearchResponse, RetrievalSearchResult
from app.services.embedding_service import EmbeddingService
from app.vectorstore.chroma_store import ChromaStore


class RetrievalService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaStore()

    def search(self, query: str, top_k: int = 5) -> RetrievalSearchResponse:
        query_embedding = self.embedding_service.embed_text(query)
        records = self.vector_store.search(query_embedding=query_embedding, top_k=top_k)
        results = [
            RetrievalSearchResult(
                chunk_id=record["chunk_id"],
                document_id=record["document_id"],
                document_title=record.get("metadata", {}).get("filename", record["document_id"]),
                chunk_text=record["chunk_text"],
                score=round(float(record["score"]), 6),
                metadata=record.get("metadata", {}),
            )
            for record in records
        ]
        return RetrievalSearchResponse(query=query, results=results)

    def retrieve(self, question: str, equipment_type: str | None = None) -> list[SourceItem]:
        response = self.search(question, top_k=5)
        return [
            SourceItem(
                title=result.document_title,
                snippet=result.chunk_text,
                source_type=result.metadata.get("source_type", "chunk"),
            )
            for result in response.results
        ]
