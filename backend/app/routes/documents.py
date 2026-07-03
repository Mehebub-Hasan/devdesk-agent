from fastapi import APIRouter

from app.models.schemas import DocumentStatsResponse
from app.services.vector_store import vector_store

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/stats", response_model=DocumentStatsResponse)
def get_document_stats() -> dict:
    return vector_store.get_stats()


@router.delete("/clear")
def clear_documents() -> dict:
    return vector_store.clear()
