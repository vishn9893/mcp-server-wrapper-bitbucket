from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="BITBUCKET_", extra="ignore")

    url: str = Field("http://localhost:7990", description="Bitbucket Server base URL")
    token: str | None = None
    username: str | None = None
    password: str | None = None
    verify_tls: bool = True
    timeout: float = Field(30.0, gt=0)
    max_retries: int = Field(3, ge=0, le=10)
    transport: str = "stdio"

    @property
    def api_url(self) -> str:
        return self.url.rstrip("/") + "/rest/api/1.0"

    def validate_auth(self) -> None:
        if not self.token and not (self.username and self.password):
            raise ValueError("Set BITBUCKET_TOKEN or both BITBUCKET_USERNAME and BITBUCKET_PASSWORD")


@lru_cache
def get_settings() -> Settings:
    return Settings()
