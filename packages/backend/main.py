from fastapi import FastAPI
from backend.routes import upload, chat

app = FastAPI()

# Register the routes
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "ChatPDF API is running"}