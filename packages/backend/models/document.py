from pydantic import BaseModel

class ChatQuery(BaseModel):
  question: str

class ChatResponse(BaseModel):
  answer: str
  sources: list

class DocumentBase(BaseModel):
    filename: str
    original_name: str
    user_id: Optional[str] = None

class Document(DocumentBase):
    id: str
    r2_key: str
    r2_url: str
    status: str
    created_at: str

