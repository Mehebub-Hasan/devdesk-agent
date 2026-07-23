from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.chunker import chunk_text_with_offsets
from app.services.embeddings import create_embeddings
from app.services.file_reader import read_text_file
from app.services.vector_store import vector_store

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".md", ".py", ".js", ".csv"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = Path(file.filename).name if file.filename else ""

    if not filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    file_extension = Path(filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_extension}' is not supported yet.",
        )

    save_path = UPLOAD_DIR / filename

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    extracted_text = read_text_file(save_path)

    # chunk_records carry each chunk's text plus its char_start/char_end offsets
    # into extracted_text, so citations can point at the exact source span.
    chunk_records = chunk_text_with_offsets(extracted_text)
    chunk_texts = [record["text"] for record in chunk_records]
    embeddings = create_embeddings(chunk_texts)

    # One stable id per uploaded file, shared by all of its chunks.
    doc_id = str(uuid4())

    stored_chunk_count = vector_store.add_documents(
        doc_id=doc_id,
        filename=filename,
        chunk_records=chunk_records,
        embeddings=embeddings,
    )

    embedding_dimension = len(embeddings[0]) if embeddings else 0

    return {
        "message": "File uploaded, processed, embedded, and stored successfully.",
        "doc_id": doc_id,
        "filename": filename,
        "file_extension": file_extension,
        "content_type": file.content_type,
        "size_bytes": save_path.stat().st_size,
        "saved_path": str(save_path),
        "character_count": len(extracted_text),
        "chunk_count": len(chunk_texts),
        "stored_chunk_count": stored_chunk_count,
        "embedding_count": len(embeddings),
        "embedding_dimension": embedding_dimension,
        "text_preview": extracted_text[:500],
        "chunks_preview": chunk_texts[:3],
    }