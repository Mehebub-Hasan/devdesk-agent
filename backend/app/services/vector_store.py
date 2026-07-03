from typing import Any

import numpy as np


class InMemoryVectorStore:
    """
    A simple in-memory vector store.

    This stores:
    - text chunks
    - embeddings
    - metadata such as filename and chunk index

    Later we can replace this with FAISS or a database-backed vector store.
    """

    def __init__(self):
        self.embeddings: list[list[float]] = []
        self.texts: list[str] = []
        self.metadata: list[dict[str, Any]] = []

    def add_documents(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        filename: str,
    ) -> int:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length")

        for index, chunk in enumerate(chunks):
            self.texts.append(chunk)
            self.embeddings.append(embeddings[index])
            self.metadata.append(
                {
                    "filename": filename,
                    "chunk_index": index,
                }
            )

        return len(chunks)

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


vector_store = InMemoryVectorStore()
