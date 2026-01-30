from pydantic import BaseModel

class ChatQuery(BaseModel):
  question: str

class ChatResponse(BaseModel):
  answer: str
  sources: list

