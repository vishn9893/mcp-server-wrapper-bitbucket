import pytest

from bitbucket_mcp.config import Settings


def test_api_url_is_normalized():
    assert Settings(url="https://bb.example/", token="x").api_url == "https://bb.example/rest/api/1.0"


def test_auth_validation_accepts_token_or_basic():
    Settings(token="x").validate_auth()
    Settings(username="u", password="p").validate_auth()
    with pytest.raises(ValueError):
        Settings().validate_auth()
