from PyPDF2 import PdfReader
from backend.utils.chunker import chunk_text

def process_pdf(file_path: str) -> list[str]:
  """
  Extracts text from PDF and splits into chunks.
  Optimized for large files with page-level logging.
  """
  try:
    print(f"Opening PDF: {file_path}")
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    print(f"Found {num_pages} pages.")
    
    text = ""
    for i, page in enumerate(reader.pages):
      try:
        if (i + 1) % 50 == 0 or (i + 1) == num_pages:
          print(f"Extracting text: {i + 1}/{num_pages} pages...")
          
        page_text = page.extract_text()
        if page_text:
          text += page_text + "\n"
      except Exception as page_err:
        print(f"Warning: Could not extract page {i+1}: {page_err}")
        continue
    
    if not text.strip():
      print(f"Error: No readable text found in {file_path}")
      return []

    print(f"Chunking {len(text)} characters of text...")
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    print(f"Success: Extracted {len(chunks)} chunks.")
    return chunks

  except Exception as e:
    print(f"PyPDF2 Fatal Error: {str(e)}")
    return []
