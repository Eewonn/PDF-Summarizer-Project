from fastapi import HTTPException
import pymupdf

class PDFService:
    def __init__(self):
        self.doc = None
    
    #open pdf
    def open_pdf(self, file_path: str):
        try:
            self.doc = pymupdf.open(file_path)
            return self.doc
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="PDF File not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error opening PDF: {e}")
    
    #get page count
    def get_page_count(self) -> int:
        if not self.doc:
            raise HTTPException(status_code=400, detail="PDF not opened")
        return self.doc.page_count
    
    #extract text from specific page
    def extract_text(self, page_number: int = 0) -> str:
        if not self.doc:
            raise HTTPException(status_code=400, detail="PDF not opened")
        
        try:
            page = self.doc.load_page(page_number)
            return page.get_text()
        except IndexError:
            raise HTTPException(status_code=400, detail=f"Page {page_number} not found")
        
    def extract_all_text(self) -> list[str]:
        texts = []
        for page_number in range(self.doc.page_count):
            texts.append(self.extract_text(page_number))
        return texts

    def close_pdf(self):
        if self.doc:
            self.doc.close()

