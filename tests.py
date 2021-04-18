import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Helo World!"}


@pytest.mark.parametrize("name", ["Zenek", "Marta"])
def hello_name_param(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Helo {name}'
