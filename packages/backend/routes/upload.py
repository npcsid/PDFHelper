import shutil
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.pdf import process_pdf
from backend.services.embedding import get_embedding
from backend.data.storage import add_chunk

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
  """
  1. Save file locally
  2. Extract Text & Chunk
  3. Embed & Store in Memory
  """
  try:
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer) 
      print(f"📂 Saved file to {file_path}")
      text_chunks = process_pdf(file_path)
      if not text_chunks:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
        print(f"🧠 Generating embeddings for {len(text_chunks)} chunks...")
        count = 0
        for chunk_text in text_chunks:
            vector = get_embedding(chunk_text)
            if vector:
                add_chunk(chunk_text, vector, file.filename)
                count += 1
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_processed": count,
            "message": "Document ready for chatting!"
        }
  except Exception as e:
    print(f"Error while uploading document: {e}")
    raise HTTPException(status_code=500, detail=str(e))