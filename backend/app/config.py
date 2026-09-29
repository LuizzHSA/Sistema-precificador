import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _database_url():
    """Resolve PostgreSQL em produção/Vercel e SQLite apenas no ambiente local."""
    url = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("POSTGRES_PRISMA_URL")
        or os.getenv("POSTGRES_URL_NON_POOLING")
    )

    if url:
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return url

    if os.getenv("VERCEL"):
        # Mantém a aplicação inicializável para que /health exponha
        # claramente a ausência do PostgreSQL, sem cair silenciosamente em SQLite.
        return "sqlite:////tmp/price-tracker-missing-postgres.db"

    return "sqlite:///price_tracker.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    AUTH_EMAIL = os.getenv("AUTH_EMAIL")
    AUTH_PASSWORD_HASH = os.getenv("AUTH_PASSWORD_HASH")
    AUTH_NAME = os.getenv("AUTH_NAME", "Administrador")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "1048576"))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "120"))
    RATE_WINDOW_SECONDS = int(os.getenv("RATE_WINDOW_SECONDS", "60"))

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM = os.getenv("SMTP_FROM", "noreply@localhost")
    SMTP_TLS = os.getenv("SMTP_TLS", "true").lower() == "true"
    NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8080,http://localhost:5173,http://localhost:3000",
        ).split(",")
        if origin.strip()
    ]


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = "https"


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
