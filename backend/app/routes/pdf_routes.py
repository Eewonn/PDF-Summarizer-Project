from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter()

def validate_pdf(filename: str) -> bool:
    return filename.endswith(".pdf")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not validate_pdf(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")
    return {
        "filename": file.filename,
        "content-type": file.content_type,
    }
