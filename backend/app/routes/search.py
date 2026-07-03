from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.embeddings import create_embeddings
from app.services.vector_store import vector_store

router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


@router.post("")
def search_documents(request: SearchRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    query_embedding = create_embeddings([query])[0]

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=request.top_k,
    )

    return {
        "query": query,
        "top_k": request.top_k,
        "result_count": len(results),
        "results": results,
    }