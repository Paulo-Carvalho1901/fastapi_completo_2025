import pytest

from fastapi.testclient import TestClient

from main import app


# Bloco de teste reutilizavel (DRY)
@pytest.fixture
def client():
    return TestClient(app)