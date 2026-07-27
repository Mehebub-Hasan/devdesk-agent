import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.models.schemas import DocumentStatsResponse
from app.services.vector_store import vector_store

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])

# Raw uploads live here. Mirror upload.py, which saves to Path("uploads")
# relative to the working directory, so we look in the same place.
UPLOAD_DIR = Path("uploads")


@router.get("/stats", response_model=DocumentStatsResponse)
def get_document_stats() -> dict:
    return vector_store.get_stats()


@router.delete("/clear")
def clear_documents() -> dict:
    return vector_store.clear()


# Declared AFTER /clear so that DELETE /documents/clear keeps matching the
# literal route above, instead of being captured here as doc_id="clear".
@router.delete("/{doc_id}")
def delete_document(doc_id: str) -> dict:
    result = vector_store.delete_document(doc_id)

    # No chunk matched this id — a clear 404, never a 500.
    if result["deleted_chunks"] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No document found with doc_id '{doc_id}'.",
        )

    # Raw-file cleanup: delete uploads/{filename} only if NO remaining chunk
    # still references that filename. The same file uploaded twice (different
    # doc_ids) shares one raw file on disk, so we must not delete it while
    # another document still points at it.
    remaining_files = {meta["filename"] for meta in vector_store.metadata}
    removed_files = []

    for filename in result["filenames"]:
        if filename in remaining_files:
            continue

        file_path = UPLOAD_DIR / filename
        try:
            if file_path.exists():
                file_path.unlink()
                removed_files.append(filename)
        except OSError as error:
            # A failed file delete must not fail the whole request — the index
            # is already updated. Log it and move on.
            logger.warning("Could not delete raw file %s: %s", file_path, error)

    return {
        "message": f"Document '{doc_id}' deleted.",
        "doc_id": doc_id,
        "deleted_chunks": result["deleted_chunks"],
        "removed_files": removed_files,
    }
