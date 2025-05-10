from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.pdf_service import PDFService
import tempfile
import os

router = APIRouter()

def validate_pdf(filename: str) -> bool:
    return filename.endswith(".pdf")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    #validate file format
    if not validate_pdf(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")

    #save file to temp directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        #initialize pdf service
        pdf_service = PDFService()
        pdf_service.open_pdf(temp_path)

        #return text from first page
        text = pdf_service.extract_text(0)
        
        return {
            "filename": file.filename,
            "text": text
        }
    
    finally:
        #clean up temp file
        os.remove(temp_path)
        