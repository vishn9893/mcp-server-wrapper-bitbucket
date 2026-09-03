import pytest
from confluence_mcp.config import Settings

def test_api_url(): assert Settings(url="https://site.atlassian.net/", email="e", token="t").api_url == "https://site.atlassian.net/wiki/api/v2"
def test_auth():
    Settings(email="e", token="t").validate_auth()
    Settings(url="https://confluence.example.local", personal_token="t").validate_auth()
    with pytest.raises(ValueError): Settings().validate_auth()

def test_data_center_api_url():
    settings = Settings(url="https://confluence.example.local", personal_token="t")
    assert settings.is_cloud is False
    assert settings.api_url == "https://confluence.example.local/rest/api/2"
