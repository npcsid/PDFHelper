import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = "data/uploads"

CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "pdf-helper")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")  # Optional: Custom domain or public bucket URL

CF_API_TOKEN = os.getenv("CF_API_TOKEN")
D1_DATABASE_ID = os.getenv("D1_DATABASE_ID")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/callback")
JWT_SECRET = os.getenv("JWT_SECRET", "random-jwt-secret-key")