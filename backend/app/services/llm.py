from app.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    deepseek_ready,
)


SYSTEM_MESSAGE = (
    "You are DevDesk Agent, an AI assistant that answers questions using only "
    "the provided project context. If the context is insufficient, say so "
    "clearly. Keep answers concise and grounded. Do not invent information "
    "outside the provided context."
)


def _build_fallback_answer(context_chunks: list[str]) -> str:
    combined_context = "\n\n".join(context_chunks)

    return (
        "Based on the uploaded document, the most relevant information I "
        f"found is: {combined_context}"
    )


def generate_answer_with_deepseek(question: str, context_chunks: list[str]) -> str:
    # Fall back locally unless DeepSeek is both enabled AND has a key. A flag
    # set to true with an empty key used to raise (a 502 to the client); now it
    # quietly uses the local answer instead.
    if not deepseek_ready():
        return _build_fallback_answer(context_chunks)

    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError(
            "The openai package is not installed. Run pip install -r "
            "requirements.txt from the backend folder."
        ) from error

    combined_context = "\n\n---\n\n".join(
        chunk.strip() for chunk in context_chunks if chunk.strip()
    )

    user_message = f"""
Question:
{question}

Context:
{combined_context}
""".strip()

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    if not answer:
        return _build_fallback_answer(context_chunks)

    return answer.strip()
