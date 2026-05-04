from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    project_name: str = "Sistema de Incidentes Escolares API"
    api_v1_str: str = "/api/v1"
    database_url: str
    frontend_origin: str = "http://localhost:5173"
    frontend_origin_fallback: str = "http://localhost:5174"
    db_connect_timeout: float = 8.0
    db_command_timeout: int = 10

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if not isinstance(value, str) or not value:
            return value

        normalized = value

        # Normalize sync-style URL to asyncpg URL.
        if normalized.startswith("postgresql://"):
            normalized = normalized.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Normalize legacy query params that asyncpg does not accept directly.
        if normalized.startswith("postgresql+asyncpg://"):
            parts = urlsplit(normalized)
            query_params = dict(parse_qsl(parts.query, keep_blank_values=True))

            if "sslmode" in query_params and "ssl" not in query_params:
                sslmode = query_params.pop("sslmode").lower()
                if sslmode != "disable":
                    query_params["ssl"] = "require"

            query_params.pop("channel_binding", None)

            normalized = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, urlencode(query_params), parts.fragment)
            )

        return normalized

    @property
    def frontend_origins(self) -> list[str]:
        origins = {self.frontend_origin, self.frontend_origin_fallback}
        return sorted(origin for origin in origins if origin)


@lru_cache
def get_settings() -> Settings:
    return Settings()
