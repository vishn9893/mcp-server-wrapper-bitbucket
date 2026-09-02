import pytest
from confluence_mcp.config import Settings

def test_api_url(): assert Settings(url="https://x/", email="e", token="t").api_url == "https://x/wiki/api/v2"
def test_auth():
    Settings(email="e", token="t").validate_auth()
    with pytest.raises(ValueError): Settings().validate_auth()
