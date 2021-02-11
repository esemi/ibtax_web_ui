import pytest
from starlette.testclient import TestClient

from web_ui.webapp import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
