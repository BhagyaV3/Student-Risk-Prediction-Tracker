from fastapi.testclient import TestClient
from app.models.user import User
from app.services.auth_service import AuthService


def test_register_and_login_flow(client: TestClient):
    register_data = {
        "username": "test_teacher",
        "email": "teacher@example.com",
        "password": "strongpassword"
    }

    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 201
    payload = response.json()
    assert payload["username"] == "test_teacher"
    assert payload["email"] == "teacher@example.com"
    assert "password_hash" not in payload

    login_data = {
        "username": "test_teacher",
        "password": "strongpassword"
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert token_data["token_type"] == "bearer"
    assert "access_token" in token_data

    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    profile = response.json()
    assert profile["username"] == "test_teacher"
    assert profile["email"] == "teacher@example.com"
