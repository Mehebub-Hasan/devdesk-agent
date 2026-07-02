from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def create_embeddings(text_chunks: list[str]) -> list[list[float]]:
    """
    Convert text chunks into embedding vectors.
    """

    if not text_chunks:
        return []

    model = get_embedding_model()
    embeddings = model.encode(text_chunks, convert_to_numpy=True)

    return embeddings.tolist()