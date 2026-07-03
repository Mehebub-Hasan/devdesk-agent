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


class DocumentStatsResponse(BaseModel):
    total_chunks: int
    total_embeddings: int
    total_files: int
    files: list[str]
