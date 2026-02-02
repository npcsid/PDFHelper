import shutil
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.pdf import process_pdf
from backend.services.embedding import get_embedding
from backend.data.storage import add_chunk
from backend.services.r2 import upload_to_r2, download_from_r2
from backend.services.d1 import save_document, update_document_status, init_schema
import httpx
from fastapi.responses import StreamingResponse

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 6MB limit for now, this will be fixed sometime later
MAX_FILE_SIZE = 6 * 1024 * 1024 

def check_file_size(file: UploadFile):
    """Checks if the uploaded file is within the size limit."""
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large ({file.size / 1024 / 1024:.1f}MB). Max limit is 5MB."
        )

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
  """
  1. Save file locally
  2. Extract Text & Chunk
  3. Embed & Store in Memory
  """
  check_file_size(file)
  try:
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
      shutil.copyfileobj(file.file, buffer) 
    print(f"Saved file to {file_path}")

    text_chunks = process_pdf(file_path)
    if not text_chunks:
      raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    
    print(f"Generating embeddings for {len(text_chunks)} chunks...")
    count = 0
    for chunk_text in text_chunks:
        vector = get_embedding(chunk_text)
        if vector:
            await add_chunk(chunk_text, vector, file.filename)
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


@router.post("/upload/cloud")
async def upload_to_cloud(file: UploadFile = File(...), user_id: str = None):
  """
  Upload PDF to R2, save metadata to D1, and extract/embed text.
  """
  check_file_size(file)
  try:
    file_content = await file.read()
    
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail="File content exceeds the 15MB limit."
        )
        
    original_filename = file.filename
    
    print(f"Uploading {original_filename} to R2...")
    r2_result = upload_to_r2(file_content, original_filename, file.content_type or "application/pdf")
    
    print(f"Saving metadata to D1...")
    doc_record = await save_document(
        filename=r2_result['r2_key'].split('/')[-1],
        original_name=original_filename,
        r2_key=r2_result['r2_key'],
        r2_url=r2_result['r2_url'],
        file_size=r2_result['file_size'],
        user_id=user_id
    )

    tmp_path = f"data/uploads/tmp_{doc_record['id']}.pdf"
    with open(tmp_path, "wb") as f:
        f.write(file_content)
    
    text_chunks = process_pdf(tmp_path)
    os.remove(tmp_path)

    if not text_chunks:
        await update_document_status(doc_record['id'], 'error')
        raise HTTPException(status_code=400, detail="Could not extract text from PDF (Empty or Scanned).")
    
    print(f"Embedding {len(text_chunks)} chunks...")
    count = 0
    total = len(text_chunks)
    for i, chunk_text in enumerate(text_chunks):
        # Log embedding progress every 50 chunks
        if (i + 1) % 50 == 0 or (i + 1) == total:
            print(f"Embedding progress: {i + 1}/{total} chunks...")
            
        vector = get_embedding(chunk_text)
        if vector:
            await add_chunk(chunk_text, vector, original_filename, document_id=doc_record['id'])
            count += 1
    
    await update_document_status(doc_record['id'], 'processed', count)
    
    return {
        "status": "success",
        "id": doc_record['id'],
        "url": r2_result['r2_url'],
        "chunks_processed": count
    }
    
  except Exception as e:
    print(f"Cloud Upload Error: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/init-db")
async def initialize_database():
  """
  Initialize the D1 database schema.
  Call this once to set up the tables.
  """
  try:
    await init_schema()
    return {"status": "success", "message": "Database schema initialized"}
  except Exception as e:
    print(f"Error initializing database: {e}")
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/proxy-pdf")
async def proxy_pdf(url: str):
    """
    Proxy a PDF from a remote URL to bypass CORS issues.
    """
    async def stream_file():
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("GET", url) as response:
                    if response.status_code != 200:
                        raise HTTPException(status_code=response.status_code, detail="Failed to fetch remote PDF")
                    
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except Exception as e:
                print(f"Proxy error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    return StreamingResponse(stream_file(), media_type="application/pdf")