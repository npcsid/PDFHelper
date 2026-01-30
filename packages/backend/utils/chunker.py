from typing import List

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:

  """
  Splits a long text into smaller chunks for processing.

  Args:
    text: The full string content.
    chunk_size: How many characters per chunk.
    overlap: How many characters to repeat from the previous chunk (preserves context).
                 
  Returns:
    A list of string chunks.
  """

  if not text:
    return []

  chunks = []
  start = 0
  text_length = len(text)

  while start < text_length:
    end = start + chunk_size
    chunk = text[start:end]
    
    cleaned_chunk = chunk.replace('\n', ' ').strip()
    
    if cleaned_chunk:
      chunks.append(cleaned_chunk)
      
    start = end - overlap

    if start >= text_length:
      break
             
  return chunks
