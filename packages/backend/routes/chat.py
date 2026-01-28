from fastapi import APIRouter
from backend.models.document import ChatQuery, ChatResponse
from backend.services.embedding import get_embedding
from backend.routes.upload import DB_MEMORY
import numpy as np
import openai

router = APIRouter()

# Adding a comment here so that this doesn't kill me in the future
# Cosine similarity is a metric used to measure how similar two things are in this case, pieces of text.
# Think of each piece of text (like a user's question or a paragraph from a PDF) as an arrow pointing in a specific direction in a multi-dimensional space.
# Similar meanings = arrows point in roughly the same direction (small angle).
# Different meanings = arrows point in different directions (large angle).

def cosine_similarity(a, b):
    return np.dot(a, b)

@router.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery):
    # converts the user's text question into a mathematical vector (a list of numbers) so the computer can "understand" its meaning.
    q_vector = get_embedding(query.question)
    
    similarities = []
    for doc in DB_MEMORY["chunks"]:
        score = cosine_similarity(q_vector, doc["vector"])
        similarities.append((score, doc["text"]))
    
    similarities.sort(key=lambda x: x[0], reverse=True)
    top_docs = [text for score, text in similarities[:3]]
    
    context = "\n".join(top_docs)
    prompt = f"Answer based on context:\n{context}\n\nQuestion: {query.question}"
    
    
    return ChatResponse(
        answer=f"Context found: {top_docs[0][:50]}...",
        sources=top_docs
    )