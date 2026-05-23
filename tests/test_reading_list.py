import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def token(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "listuser",
            "email": "listuser@example.com",
            "password": "secret123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "listuser", "password": "secret123"},
    )
    return resp.json()["access_token"]


def test_add_to_list(client: TestClient, token):
    resp = client.post(
        "/list/add",
        json={
            "ol_id": "OL123W",
            "title": "Test Book",
            "author": "Test Author",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["ol_id"] == "OL123W"


def test_get_list(client: TestClient, token):
    client.post(
        "/list/add",
        json={"ol_id": "OL456W", "title": "Another Book"},
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = client.get(
        "/list", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert any(item["ol_id"] == "OL456W" for item in resp.json())


def test_remove_from_list(client: TestClient, token):
    client.post(
        "/list/add",
        json={"ol_id": "OL789W", "title": "Remove Me"},
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = client.delete(
        "/list/OL789W", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 204
