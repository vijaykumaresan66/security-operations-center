import os
from pathlib import Path


# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# RUNTIME DIRECTORY
# ==========================================

# Vercel's project directory is read-only.
# Use /tmp for files that need to be created at runtime.
IS_VERCEL = bool(os.getenv("VERCEL"))

if IS_VERCEL:
    RUNTIME_DIR = Path("/tmp/soc_analyst")
else:
    RUNTIME_DIR = BASE_DIR


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key-in-production"
    )

    PERMANENT_SESSION_LIFETIME = 3600

    DATABASE_PATH = RUNTIME_DIR / "database" / "soc.db"

    UPLOAD_FOLDER = RUNTIME_DIR / "uploads"

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "txt",
        "log",
        "csv"
    }


# ==========================================
# CREATE RUNTIME DIRECTORIES
# ==========================================

Config.UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

Config.DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)