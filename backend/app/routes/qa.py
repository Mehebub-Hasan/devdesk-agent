from fastapi import APIRouter, HTTPException

from app.models.schemas import QuestionRequest
from app.services.embeddings import create_embeddings
from app.services.vector_store import vector_store

router = APIRouter(prefix="/qa", tags=["Question Answering"])


@router.post("/ask")
def ask_question(request: QuestionRequest) -> dict:
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    question_embedding = create_embeddings([question])[0]

    results = vector_store.search(
        query_embedding=question_embedding,
        top_k=request.top_k,
    )

    if not results:
        return {
            "question": question,
            "answer": "No document content was found. Please upload a file first, then ask your question again.",
            "source_count": 0,
            "sources": [],
        }

    retrieved_chunks = [result["text"].strip() for result in results]
    combined_context = "\n\n".join(retrieved_chunks)

    sources = []

    for result in results:
        metadata = result.get("metadata", {})
        text = result.get("text", "")

        sources.append(
            {
                "filename": metadata.get("filename"),
                "chunk_index": metadata.get("chunk_index"),
                "similarity_score": round(result.get("score", 0), 4),
                "text_preview": text[:250],
            }
        )

    return {
        "question": question,
        "answer": (
            "Based on the uploaded document, the most relevant information I "
            f"found is: {combined_context}"
        ),
        "source_count": len(sources),
        "sources": sources,
    }
