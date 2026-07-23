from fastapi import APIRouter, HTTPException

from app.models.schemas import QuestionRequest
from app.services.embeddings import create_embeddings
from app.services.llm import generate_answer_with_deepseek
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

    try:
        answer = generate_answer_with_deepseek(
            question=question,
            context_chunks=retrieved_chunks,
        )
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"DeepSeek answer generation failed: {error}",
        ) from error

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
        "answer": answer,
        "source_count": len(sources),
        "sources": sources,
    }
