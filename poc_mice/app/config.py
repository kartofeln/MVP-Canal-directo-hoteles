from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Siempre la raíz del paquete POC (poc_mice/), aunque uvicorn se lance desde otro cwd.
_POC_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_POC_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Por defecto SQLite = funciona sin Docker. Para Postgres: ver .env.example
    database_url: str = "sqlite:///./mice_poc.db"
    dataforseo_login: str = ""
    dataforseo_password: str = ""
    anthropic_api_key: str = ""
    kapso_api_key: str = ""
    kapso_test_to: str = ""
    kapso_webhook_secret: str = ""
    # Solo pruebas: 1 = permite POST /v1/ingest/demo-local (filas ficticias, sin DataForSEO)
    poc_allow_fake_data: int = 0

    @model_validator(mode="after")
    def resolve_sqlite_relative_path(self) -> Self:
        """Evita BD vacía si el cwd no es poc_mice (sqlite:///./… es relativo al proceso)."""
        url = self.database_url.strip()
        if not url.lower().startswith("sqlite:///"):
            return self
        rest = url.removeprefix("sqlite:///")
        if not rest or rest.lower().startswith(":memory"):
            return self
        p = Path(rest)
        if not p.is_absolute():
            p = (_POC_DIR / rest).resolve()
            self.database_url = f"sqlite:///{p.as_posix()}"
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
