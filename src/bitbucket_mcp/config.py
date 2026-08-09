from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    base_url: str
    token: str | None = None
    username: str | None = None
    password: str | None = None
    verify_ssl: bool = True

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("BITBUCKET_URL", "").rstrip("/")
        if not base_url:
            raise ValueError("BITBUCKET_URL is required")
        token = os.getenv("BITBUCKET_TOKEN")
        username = os.getenv("BITBUCKET_USERNAME")
        password = os.getenv("BITBUCKET_PASSWORD")
        verify_ssl = os.getenv("BITBUCKET_VERIFY_SSL", "true").lower() not in {"0", "false", "no"}
        if not token and not (username and password):
            raise ValueError("Set BITBUCKET_TOKEN or BITBUCKET_USERNAME and BITBUCKET_PASSWORD")
        return cls(base_url, token, username, password, verify_ssl)
