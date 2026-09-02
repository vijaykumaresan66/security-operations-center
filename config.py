import os
from pathlib import Path

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================
class Config:

    SECRET_KEY=os.getenv(
        "SECRET_KEY",
        "change-this-secret-key-in-production"
    )

    PERMANENT_SESSION_LIFETIME = 3600

    DATABASE_PATH = BASE_DIR / "database" / "soc.db"

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "txt",
        "log",
        "csv"
    }

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key-in-production"
    )

    DATABASE_PATH = BASE_DIR / "database" / "soc.db"

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

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

(BASE_DIR / "database").mkdir(
    parents=True,
    exist_ok=True
)