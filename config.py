import os
from pathlib import Path


# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# VERCEL / LOCAL STORAGE
# ==========================================

# Vercel's application directory is read-only.
# /tmp is writable but temporary.
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

    # Database
    DATABASE_PATH = RUNTIME_DIR / "database" / "soc.db"

    # Uploaded log files
    UPLOAD_FOLDER = RUNTIME_DIR / "uploads"

    # Maximum upload size: 10 MB
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Allowed upload extensions
    ALLOWED_EXTENSIONS = {
        "txt",
        "log",
        "csv"
    }


# ==========================================
# CREATE REQUIRED DIRECTORIES
# ==========================================

Config.UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

Config.DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)