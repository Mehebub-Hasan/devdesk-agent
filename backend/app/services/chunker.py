def chunk_text_with_offsets(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[dict]:
    """
    Split text into overlapping chunks, keeping each chunk's character offsets.

    Returns a list of dicts: {"text", "char_start", "char_end"}.

    The offsets point back into the ORIGINAL `text`. We compute them here, while
    we still know exactly where each window starts, rather than searching for the
    chunk afterwards with str.find() — a search would land on the wrong copy when
    the same text repeats in the document.

    Because we .strip() each chunk (leading/trailing whitespace is noise for
    embeddings), we shift char_start past any stripped leading whitespace so the
    offsets still describe the text we actually stored.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    records = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        raw = text[start:end]
        stripped = raw.strip()

        if stripped:
            # How many characters strip() removed from the front — this is how
            # far the stored text sits inside the raw window.
            leading = len(raw) - len(raw.lstrip())
            char_start = start + leading
            char_end = char_start + len(stripped)

            records.append(
                {
                    "text": stripped,
                    "char_start": char_start,
                    "char_end": char_end,
                }
            )

        start = end - overlap

    return records


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    """
    Split a long text into smaller overlapping chunks.

    Thin wrapper over chunk_text_with_offsets() for callers that only need the
    chunk strings and not their offsets.

    Args:
        text: The full text content.
        chunk_size: Maximum number of characters in each chunk.
        overlap: Number of characters repeated between chunks.

    Returns:
        A list of text chunks.
    """

    return [
        record["text"]
        for record in chunk_text_with_offsets(text, chunk_size, overlap)
    ]
