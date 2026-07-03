from fastapi import FastAPI

from app.routes.qa import router as qa_router
from app.routes.search import router as search_router
from app.routes.upload import router as upload_router

app = FastAPI(
    title="DevDesk Agent API",
    description="Backend API for DevDesk Agent",
    version="0.1.0",
)

app.include_router(upload_router)
app.include_router(search_router)
app.include_router(qa_router)


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
    }
