from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".md", ".py", ".js", ".csv"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = Path(file.filename).name if file.filename else ""

    if not filename:
        raise HTTPException(status_code=400, detail="No file name provided.")

    file_extension = Path(filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_extension}' is not supported yet.",
        )

    save_path = UPLOAD_DIR / filename

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    return {
        "message": "File uploaded successfully.",
        "filename": filename,
        "file_extension": file_extension,
        "content_type": file.content_type,
        "size_bytes": save_path.stat().st_size,
        "saved_path": str(save_path),
    }