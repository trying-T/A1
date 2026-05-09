import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
PARSED_DOCUMENT_DIR = DATA_DIR / "parsed" / "documents"
SQLITE_DIR = DATA_DIR / "sqlite"
SQLITE_DB_PATH = SQLITE_DIR / "app.db"
VECTOR_DB_DIR = DATA_DIR / "vector_db" / "chroma"

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "mock").strip().lower()
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "").strip()
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "").strip()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mock-hash-embedding").strip()
EMBEDDING_TIMEOUT_SECONDS = float(os.getenv("EMBEDDING_TIMEOUT_SECONDS", "30"))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").strip().lower()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "60"))

ALLOWED_DOCUMENT_TYPES = {
    ".pdf": "pdf",
    ".txt": "txt",
    ".md": "markdown",
    ".markdown": "markdown",
}
