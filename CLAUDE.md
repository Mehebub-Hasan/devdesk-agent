# DevDesk Agent

A local RAG workspace assistant. Upload documents, ask questions, get answers
with source references.

**Core principle: retrieval is 100% local. Only the final answer-generation call
leaves the machine.** Embeddings, vector storage, and search never touch an
external API. DeepSeek receives only a question plus a few retrieved text chunks.

---

## Stack

- **Backend:** FastAPI (Python), SentenceTransformers, NumPy vector search
- **Frontend:** Next.js, TypeScript, Tailwind CSS
- **LLM:** DeepSeek via the OpenAI SDK compatibility layer, behind a
  `USE_DEEPSEEK` feature flag (defaults to `false`)

---

## Layout

backend/
  app/
    routes/      documents.py, health.py, qa.py, search.py, upload.py
    services/    llm.py, embeddings.py, vector_store.py, chunker.py, file_reader.py
    models/      schemas.py (Pydantic)
    config.py    env vars
    main.py      app entry
  uploads/       user documents (gitignored)
  .env           real secrets (gitignored)
  .env.example   committed template
frontend/
  app/           layout.tsx, page.tsx, globals.css
  src/components/  BackendStatus, FileUploader, QuestionAnswer
docs/

---

## Commands

```bash
# Backend  (run from backend/, venv activated)
uvicorn app.main:app --reload

# Frontend (run from frontend/)
npm run dev
```

Backend: http://localhost:8000 · Frontend: http://localhost:3000

---

## Pipeline

```
Upload → Extract text → Chunk → Local embeddings → Store vectors
                                                        ↓
                                            Vector search (top-K)
                                                        ↓
                            ┌───────────── boundary ─────────────┐
                            │  services/llm.py is the ONLY file  │
                            │  that talks to an external API     │
                            └────────────────────────────────────┘
                                                        ↓
                                    DeepSeek (if USE_DEEPSEEK=true)
                                                        ↓
                                          Answer + sources → client
```

---

## Rules

**Secrets**
- Never write a real API key into any file, ever. Leave `DEEPSEEK_API_KEY` empty.
- Never commit `.env`. Never suggest committing it.

**Git**
- I run all git commands myself. Do not run `git add`, `git commit`, `git rm`,
  `git checkout`, `git reset`, or anything destructive.
- `git status` and `git diff` for inspection are fine.

**Scope**
- Read the relevant files first, then give me a plan, then wait for approval
  before editing.
- Do not refactor, rename, or reformat code outside the task I asked for.
- Do not add dependencies without asking.
- Retrieval stays local. DeepSeek is for generation only — never embeddings.

**Style**
- Beginner-friendly code. Comment the *why*, not the *what*.
- Prefer clear and obvious over clever and short.
- Don't narrate every edit as you go — give one summary at the end.

---

## Naming

- The LLM entry point is `generate_answer_with_deepseek(question, context_chunks)`
  in `services/llm.py`. It falls back to a local answer unless
  `deepseek_ready()` is true (flag set AND key present).

---

## Gotchas

- `load_dotenv()` runs once at import, so `--reload` does **not** reliably pick
  up `.env` changes. Fully restart uvicorn after editing `.env`.
- Windows dev machine (`E:\devdesk-agent`). Build `.env` paths from `__file__`,
  not from the current working directory.
- The health endpoint reports `deepseek_ready()` (flag AND key present), not the
  raw flag — so a missing key shows up as `use_deepseek: false`.
- If a DeepSeek call fails, fall back to the local answer. An API outage must
  never produce a 500.

---

## Status

**Current phase:** Phase 13 — source references display

Done: FastAPI setup · file upload · text extraction · chunking · local
embeddings · vector search · QA API · document management · Next.js frontend ·
upload UI · chat UI · DeepSeek integration

Next up: chunk metadata + vector persistence · eval set · error handling ·
early deploy · retrieval quality (threshold, reranking) · streaming · auth
