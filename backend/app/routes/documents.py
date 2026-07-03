from fastapi import APIRouter

from app.services.vector_store import vector_store

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("/stats")
def get_document_stats():
    return vector_store.get_stats()


@router.delete("/clear")
def clear_documents():
    return vector_store.clear()
