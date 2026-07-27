from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=5)


class SourceInfo(BaseModel):
    filename: str
    chunk_index: int
    similarity_score: float
    text_preview: str


class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    chunk_count: int


class DocumentStatsResponse(BaseModel):
    total_chunks: int
    total_embeddings: int
    total_files: int
    files: list[str]
    # Per-document breakdown so a UI can identify and delete a single document.
    # Defaulted so any older caller/response still validates.
    documents: list[DocumentInfo] = []
