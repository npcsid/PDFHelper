import pypdf
from backend.utils.chunker import chunk_text

def process_pdf(file_path: str) -> list[str]:

  """
  Reads a pdf file, extracts it and then chunks it (w/ the help of chunker util)

  Args:
    file_path: Path to temporary PDF file

  Returns:
    List of text chunks
  """

  try:
    reader = pypdf.PdfReader(file_path)
    full_text = ""
  
    for i, page in enumerate(reader.pages):
      text = page.extract_text()
      if text:
        full_text += text + "\n"

    chunks = chunk_text(full_text, chunk_size=1000, overlap=200)
    return chunks

  except Exception as e:
    print(f"Error processsing pdf: {e}")
    return []

