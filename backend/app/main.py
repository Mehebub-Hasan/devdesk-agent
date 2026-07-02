from fastapi import FastAPI

from app.routes.upload import router as upload_router

app = FastAPI(
    title="DevDesk Agent API",
    description="Backend API for DevDesk Agent",
    version="0.1.0",
)

app.include_router(upload_router)


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