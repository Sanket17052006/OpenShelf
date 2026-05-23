from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.schemas.book import BookSearchResult, BookDetail


@pytest.fixture
def token(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "bookuser",
            "email": "bookuser@example.com",
            "password": "secret123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "bookuser", "password": "secret123"},
    )
    return resp.json()["access_token"]


@patch("app.routers.books.openlibrary.search_books")
def test_search_books(mock_search, client: TestClient, token):
    mock_search.return_value = [
        BookSearchResult(
            ol_id="OL123W",
            title="Test Book",
            author="Test Author",
            first_publish_year=2020,
            cover_url="https://covers.openlibrary.org/b/id/1-M.jpg",
        )
    ]

    resp = client.get(
        "/books/search?q=test", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Book"


@patch("app.routers.books.openlibrary.get_book_detail")
def test_book_detail(mock_detail, client: TestClient, token):
    mock_detail.return_value = BookDetail(
        ol_id="OL123W",
        title="Test Book",
        author="Test Author",
        description="A test book",
        subjects=["fiction"],
    )

    resp = client.get(
        "/books/OL123W", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Test Book"
