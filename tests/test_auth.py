from fastapi.testclient import TestClient


def test_register(client: TestClient):
    resp = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "secret123",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data


def test_register_duplicate_username(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "dupuser",
            "email": "dup@example.com",
            "password": "secret123",
        },
    )
    resp = client.post(
        "/auth/register",
        json={
            "username": "dupuser",
            "email": "other@example.com",
            "password": "secret123",
        },
    )
    assert resp.status_code == 400


def test_login(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "secret123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "loginuser", "password": "secret123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "badpwd",
            "email": "badpwd@example.com",
            "password": "secret123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "badpwd", "password": "wrong"},
    )
    assert resp.status_code == 401
