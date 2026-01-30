from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.embedding import get_embedding
from backend.services.search import search_similar_chunks
from backend.services.llm import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
  try:
    user_question = request.question
    query_vector = get_embedding(user_question)
    if not query_vector:
      raise HTTPException(status_code=500, detail="Failed to generate embedding")
    relevant_chunks = search_similar_chunks(query_vector, limit=3)
    if not relevant_chunks:
      return {
        "answer": "I don't have any documents loaded yet. Please upload a PDF first.",
        "sources": []
      }
      
    ai_answer = generate_answer(user_question, relevant_chunks)
    return {
      "answer": ai_answer,
      "sources": [c['text'][:100] + "..." for c in relevant_chunks] 
    }
  except Exception as e:
    print(f"Error: {e}")
    raise HTTPException(status_code=500, detail=str(e))