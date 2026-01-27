# config.py
import os

from .auth import ensure_env

API_BASE = "https://mineru.net/api/v4"

ensure_env("MINERU_TOKEN")
TOKEN = os.getenv("MINERU_TOKEN")

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx"}
