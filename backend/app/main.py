from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import DEEPSEEK_MODEL, deepseek_ready
from app.routes.documents import router as documents_router
from app.routes.qa import router as qa_router
from app.routes.search import router as search_router
from app.routes.upload import router as upload_router
from app.services.vector_store import vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the persisted vector store once, before the app serves any request,
    # so previously uploaded documents survive a restart.
    vector_store.load()
    yield


app = FastAPI(
    title="DevDesk Agent API",
    description="Backend API for DevDesk Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(search_router)
app.include_router(qa_router)
app.include_router(documents_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to DevDesk Agent API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "devdesk-agent-backend",
        "use_deepseek": deepseek_ready(),
        "deepseek_model": DEEPSEEK_MODEL,
    }
