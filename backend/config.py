import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))



class Config:
    # ── Core ─────────────────────────────────────────
    SECRET_KEY      = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DEBUG           = False
    TESTING         = False

    # ── Database ─────────────────────────────────────
    # Switch to PostgreSQL in prod: postgresql+psycopg2://user:pw@host/db
    _db_path = os.environ.get("DB_PATH") or os.path.join(BASE_DIR, "jaggery.db")
    SQLALCHEMY_DATABASE_URI      = os.environ.get("DATABASE_URL") or f"sqlite:///{_db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS    = {"pool_pre_ping": True}

    # ── JWT ──────────────────────────────────────────
    JWT_SECRET_KEY              = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES    = timedelta(days=7)
    JWT_TOKEN_LOCATION          = ["headers"]
    JWT_HEADER_NAME             = "Authorization"
    JWT_HEADER_TYPE             = "Bearer"

    # ── Mail (SMTP) ───────────────────────────────────
    MAIL_SERVER           = os.environ.get("MAIL_SERVER") or "smtp.gmail.com"
    MAIL_PORT             = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS          = (os.environ.get("MAIL_USE_TLS") or "true").lower() == "true"
    MAIL_USE_SSL          = False
    MAIL_USERNAME         = os.environ.get("MAIL_USERNAME") or ""
    MAIL_PASSWORD         = os.environ.get("MAIL_PASSWORD") or ""
    MAIL_DEFAULT_SENDER   = os.environ.get("MAIL_SENDER") or "KhagRaj <noreply@khagraj.in>"
    MAIL_SUPPRESS_SEND    = not bool(MAIL_USERNAME)  # disable if not configured
    MAIL_DEBUG            = False

    # ── Cache ─────────────────────────────────────────
    # Use "RedisCache" in production when REDIS_URL is set.
    # Fallback to "NullCache" to prevent Gunicorn multi-worker consistency issues.
    _redis                = os.environ.get("REDIS_URL", "").strip()
    REDIS_URL             = _redis or "redis://localhost:6379/0"
    CACHE_TYPE            = "RedisCache" if _redis else "NullCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL       = REDIS_URL

    # ── Celery ────────────────────────────────────────
    CELERY_BROKER_URL    = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_ALWAYS_EAGER = not bool(_redis)
    CELERY_ACCEPT_CONTENT  = ["json"]
    CELERY_TASK_SERIALIZER = "json"

    # ── Uploads ───────────────────────────────────────
    UPLOAD_FOLDER      = os.environ.get("UPLOAD_FOLDER") or os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024   # 10 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

    # ── CORS ──────────────────────────────────────────
    FRONTEND_URL = os.environ.get("FRONTEND_URL") or "http://localhost:5173"

    # ── Admin seed ────────────────────────────────────
    ADMIN_EMAIL    = os.environ.get("ADMIN_EMAIL") or "khagrajindia2017@gmail.com"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "Admin@2025"
    ADMIN_NAME     = os.environ.get("ADMIN_NAME") or "Admin"

    # ── Pagination ────────────────────────────────────
    PRODUCTS_PER_PAGE = 20

    ORDERS_PER_PAGE   = 20


class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    CELERY_TASK_ALWAYS_EAGER = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}
