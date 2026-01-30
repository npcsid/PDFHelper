import openai
import numpy as np
from backend.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text: str):

  try:
    print(f"DEBUG: Generating embedding for text replacement... Text length: {len(text)}")
    clean_text = text.replace("\n", " ")
    print("DEBUG: Replacement successful.")
    response = client.embeddings.create(
      input=[clean_text],
      model="text-embedding-3-small"
    )

    return response.data[0].embedding
  except Exception as e:
    print(f"Error occured while embedding fetch: {e}")
    return []

# Adding a comment here so that this doesn't kill me in the future
# Cosine similarity is a metric used to measure how similar two things are in this case, pieces of text.
# Think of each piece of text (like a user's question or a paragraph from a PDF) as an arrow pointing in a specific direction in a multi-dimensional space.
# Similar meanings = arrows point in roughly the same direction (small angle).
# Different meanings = arrows point in different directions (large angle).
def cosine_similarity(a, b):
    return np.dot(a, b)
