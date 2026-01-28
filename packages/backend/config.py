import os
from dotenv import load_dotenv

from pathlib import Path

# Load .env from project root (packages/backend/config.py -> ... -> ... -> root)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = "data/uploads"