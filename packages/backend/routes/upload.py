from fastapi import APIRouter, UploadFile, File
import shutil
import os
from backend.services.pdf import process_pdf
from backend.services.embedding import get_embedding

router = APIRouter()

DB_MEMORY = {"chunks": []} 

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    
    # Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Process PDF
    text_chunks = await process_pdf(file_location)
    
    # Create Embeddings & Store in Memory
    DB_MEMORY["chunks"] = [] # Clear previous file
    for chunk in text_chunks:
        vector = get_embedding(chunk)
        DB_MEMORY["chunks"].append({
            "text": chunk,
            "vector": vector
        })
        
    return {"message": "PDF processed", "chunks": len(text_chunks)}