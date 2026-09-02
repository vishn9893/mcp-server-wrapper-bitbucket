from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CONFLUENCE_", extra="ignore")
    url: str = Field("https://your-domain.atlassian.net", description="Atlassian site URL")
    email: str | None = None
    token: str | None = None
    verify_tls: bool = True
    timeout: float = Field(30.0, gt=0)
    max_retries: int = Field(3, ge=0, le=10)
    transport: str = "stdio"

    @property
    def api_url(self) -> str:
        return self.url.rstrip("/") + "/wiki/api/v2"

    def validate_auth(self) -> None:
        if not self.token or not self.email:
            raise ValueError("Set CONFLUENCE_EMAIL and CONFLUENCE_TOKEN")


@lru_cache
def get_settings() -> Settings:
    return Settings()
