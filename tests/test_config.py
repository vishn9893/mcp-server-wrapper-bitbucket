import pytest

from bitbucket_mcp.config import Settings


def test_settings_from_token(monkeypatch):
    monkeypatch.setenv("BITBUCKET_URL", "https://bitbucket.example.com/")
    monkeypatch.setenv("BITBUCKET_TOKEN", "secret")
    settings = Settings.from_env()
    assert settings.base_url == "https://bitbucket.example.com"
    assert settings.token == "secret"


def test_settings_requires_auth(monkeypatch):
    monkeypatch.setenv("BITBUCKET_URL", "https://bitbucket.example.com")
    monkeypatch.delenv("BITBUCKET_TOKEN", raising=False)
    monkeypatch.delenv("BITBUCKET_USERNAME", raising=False)
    monkeypatch.delenv("BITBUCKET_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="BITBUCKET_TOKEN"):
        Settings.from_env()
