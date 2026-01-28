import pypdf
from backend.utils.chunker import chunk_text

async def process_pdf(file_path: str) -> list[str]:
  reader = pypdf.PdfReader(file_path)
  text = ""
  for page in reader.pages:
    text += page.extract_text() 

  chunks = chunk_text(text)
  return chunks

