from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="JIRA_", extra="ignore")
    url: str = Field("https://your-domain.atlassian.net", description="Atlassian site URL")
    email: str | None = None
    token: str | None = None
    username: str | None = None
    password: str | None = None
    personal_token: str | None = None
    verify_tls: bool = True
    timeout: float = Field(30.0, gt=0)
    max_retries: int = Field(3, ge=0, le=10)
    transport: str = "stdio"

    @property
    def api_url(self) -> str:
        return self.url.rstrip("/") + ("/rest/api/3" if self.is_cloud else "/rest/api/2")

    @property
    def is_cloud(self) -> bool:
        return self.url.lower().split("/", 3)[2].endswith(".atlassian.net") if "://" in self.url else False
    def validate_auth(self) -> None:
        if self.is_cloud and (not self.token or not self.email): raise ValueError("Set JIRA_EMAIL and JIRA_TOKEN for Jira Cloud")
        if not self.is_cloud and not (self.personal_token or self.token or (self.username and self.password)):
            raise ValueError("Set JIRA_PERSONAL_TOKEN, JIRA_TOKEN, or JIRA_USERNAME and JIRA_PASSWORD for Data Center")

@lru_cache
def get_settings() -> Settings: return Settings()
