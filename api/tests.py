from fastapi.testclient import TestClient
from main import app, get_current_username
from requests.auth import HTTPBasicAuth

client = TestClient(app)

def test_read_main():
    response = client.get('/user')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_security_http_basic():
    auth = HTTPBasicAuth(username="username", password="password")
    response = client.get("/user", auth=auth)
    assert response.status_code == 200, response.text
    assert response.json() == {'username': 'user', 'password': 'password'}

async def override_dependency():
    return {"username": 'username', "password": 'password'}

#avoiding auth for the unit test usage
app.dependency_overrides[get_current_username] = override_dependency

def test_encoding():
    response = client.post(
        "/coding",
        json={
            "contents": "foo",
        },
    )
    assert response.status_code == 200, response.text

def test_decoding():
    response = client.post(
        "/decoding",
        json={
            "contents": "foo",
        },
    )
    assert response.status_code == 200, response.text

#pytest tests.py

