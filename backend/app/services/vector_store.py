import json
import logging
import os
from pathlib import Path
from typing import Any

import numpy as np

from app.services.embeddings import MODEL_NAME

logger = logging.getLogger(__name__)

# The store lives in backend/data/. This file is at
# backend/app/services/vector_store.py, so parents[2] is the backend/ folder.
# We build the path from __file__ (not the current working directory) so it
# resolves the same no matter where uvicorn is launched from.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
VECTORS_PATH = DATA_DIR / "vectors.npy"
STORE_PATH = DATA_DIR / "store.json"


class InMemoryVectorStore:
    """
    A simple in-memory vector store that persists to disk.

    In memory this keeps three index-aligned lists:
    - text chunks
    - embeddings
    - metadata (doc_id, filename, chunk_index, char_start, char_end, page)

    On every add or delete it saves to backend/data/ so the index survives a
    restart. Later we can replace this with FAISS or a database-backed store.
    """

    def __init__(self):
        self.embeddings: list[list[float]] = []
        self.texts: list[str] = []
        self.metadata: list[dict[str, Any]] = []

    def add_documents(
        self,
        doc_id: str,
        filename: str,
        chunk_records: list[dict[str, Any]],
        embeddings: list[list[float]],
        page: int | None = None,
    ) -> int:
        """
        Add one document's chunks to the store and persist.

        chunk_records come from chunker.chunk_text_with_offsets() and carry
        {"text", "char_start", "char_end"}. The same doc_id is stamped onto every
        chunk of this document, so a citation can always be traced back to its
        source file.
        """

        if len(chunk_records) != len(embeddings):
            raise ValueError("chunk_records and embeddings must have the same length")

        for index, record in enumerate(chunk_records):
            self.texts.append(record["text"])
            self.embeddings.append(embeddings[index])
            self.metadata.append(
                {
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": index,
                    "char_start": record["char_start"],
                    "char_end": record["char_end"],
                    "page": page,
                }
            )

        # Persist after every add so an unexpected restart keeps this document.
        self.save()

        return len(chunk_records)

    def get_stats(self) -> dict[str, Any]:
        files = sorted({item["filename"] for item in self.metadata})

        return {
            "total_chunks": len(self.texts),
            "total_embeddings": len(self.embeddings),
            "total_files": len(files),
            "files": files,
        }

    def clear(self) -> dict[str, Any]:
        deleted_chunks = len(self.texts)
        deleted_embeddings = len(self.embeddings)

        self.embeddings.clear()
        self.texts.clear()
        self.metadata.clear()

        # Persist the emptied state so the wipe also survives a restart.
        self.save()

        return {
            "message": "In-memory vector store cleared successfully.",
            "deleted_chunks": deleted_chunks,
            "deleted_embeddings": deleted_embeddings,
        }

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        if not self.embeddings:
            return []

        document_vectors = np.array(self.embeddings, dtype=np.float32)
        query_vector = np.array(query_embedding, dtype=np.float32)

        document_norms = np.linalg.norm(document_vectors, axis=1)
        query_norm = np.linalg.norm(query_vector)

        similarities = document_vectors @ query_vector / (
            document_norms * query_norm + 1e-10
        )

        top_indices = similarities.argsort()[::-1][:top_k]

        results = []

        for index in top_indices:
            results.append(
                {
                    "text": self.texts[index],
                    "score": float(similarities[index]),
                    "metadata": self.metadata[index],
                }
            )

        return results

    def save(self) -> None:
        """
        Write the store to disk atomically.

        We write each file to a .tmp path first and then os.replace() it over the
        real file. os.replace is atomic on the same filesystem, so a crash
        mid-write leaves the previous (valid) files untouched instead of a
        half-written, corrupt store.
        """

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        matrix = np.array(self.embeddings, dtype=np.float32)
        dim = int(matrix.shape[1]) if matrix.ndim == 2 and matrix.size else 0

        payload = {
            "model_name": MODEL_NAME,
            "dim": dim,
            "chunks": [
                {"text": text, "metadata": meta}
                for text, meta in zip(self.texts, self.metadata)
            ],
        }

        vectors_tmp = VECTORS_PATH.with_suffix(VECTORS_PATH.suffix + ".tmp")
        store_tmp = STORE_PATH.with_suffix(STORE_PATH.suffix + ".tmp")

        # Write through an open file handle so np.save does NOT append a second
        # ".npy" extension to our .tmp filename.
        with open(vectors_tmp, "wb") as vectors_file:
            np.save(vectors_file, matrix)
        os.replace(vectors_tmp, VECTORS_PATH)

        with open(store_tmp, "w", encoding="utf-8") as store_file:
            json.dump(payload, store_file)
        os.replace(store_tmp, STORE_PATH)

    def load(self) -> None:
        """
        Load the store from disk on startup. Defensive by design: any problem
        logs a warning and starts empty rather than crashing or returning garbage.
        """

        if not STORE_PATH.exists() or not VECTORS_PATH.exists():
            logger.warning(
                "No saved vector store found in %s. Starting with an empty index.",
                DATA_DIR,
            )
            return

        try:
            with open(STORE_PATH, "r", encoding="utf-8") as store_file:
                payload = json.load(store_file)
            matrix = np.load(VECTORS_PATH)
        except (json.JSONDecodeError, ValueError, OSError) as error:
            logger.warning(
                "Vector store files are unreadable or corrupt (%s). "
                "Starting with an empty index.",
                error,
            )
            return

        saved_model = payload.get("model_name")
        saved_dim = payload.get("dim")
        chunks = payload.get("chunks", [])

        # A different embedding model produces incompatible vectors. Comparing the
        # model name is a cheap, exact proxy for "same dimension" without loading
        # the heavyweight SentenceTransformer at startup.
        if saved_model != MODEL_NAME:
            logger.warning(
                "Saved store was built with model '%s' but the current model is "
                "'%s'. Ignoring the saved index and starting empty.",
                saved_model,
                MODEL_NAME,
            )
            return

        # Internal consistency: rows in the matrix must line up with the stored
        # dimension and the number of chunks. If not, the two files are out of
        # sync (e.g. a crash between the two writes) — start empty.
        rows = matrix.shape[0] if matrix.ndim == 2 else 0
        cols = matrix.shape[1] if matrix.ndim == 2 else 0
        expected_rows = len(chunks)

        if expected_rows == 0:
            # A validly-saved empty store. Nothing to load.
            return

        if rows != expected_rows or (saved_dim and cols != saved_dim):
            logger.warning(
                "Vector store is inconsistent (matrix %sx%s, dim=%s, chunks=%s). "
                "Starting with an empty index.",
                rows,
                cols,
                saved_dim,
                expected_rows,
            )
            return

        self.embeddings = matrix.tolist()
        self.texts = [chunk["text"] for chunk in chunks]
        self.metadata = [chunk["metadata"] for chunk in chunks]

        logger.info(
            "Loaded vector store: %s chunks across %s file(s).",
            len(self.texts),
            len({meta["filename"] for meta in self.metadata}),
        )


vector_store = InMemoryVectorStore()
