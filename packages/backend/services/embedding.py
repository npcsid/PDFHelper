import openai
from backend.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text: str):
  text = text.replace("\n")
  return client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

