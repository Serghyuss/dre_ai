import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza o diretório onde o config.py está e sobe um nível para chegar na raiz
base_dir = Path(__file__).resolve().parent.parent
dotenv_path = base_dir / ".env"

load_dotenv("../.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")