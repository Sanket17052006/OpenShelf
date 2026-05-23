from typing import Optional

import httpx

from app.schemas.book import BookSearchResult, BookDetail

OPEN_LIBRARY_BASE = "https://openlibrary.org"


async def search_books(
    query: str, limit: int = 10
) -> list[BookSearchResult]:
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{OPEN_LIBRARY_BASE}/search.json", params=params
        )
        resp.raise_for_status()
        data = resp.json()

    results = []
    for doc in data.get("docs", [])[:limit]:
        ol_id = doc.get("key", "").replace("/works/", "")
        author = None
        if doc.get("author_name"):
            author = doc["author_name"][0]

        cover_url = None
        if doc.get("cover_i"):
            cover_url = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"

        results.append(
            BookSearchResult(
                ol_id=ol_id,
                title=doc.get("title", "Unknown"),
                author=author,
                first_publish_year=doc.get("first_publish_year"),
                cover_url=cover_url,
            )
        )
    return results


async def get_book_detail(ol_id: str) -> Optional[BookDetail]:
    if not ol_id or "/" in ol_id or "\\" in ol_id or ".." in ol_id:
        return None
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{OPEN_LIBRARY_BASE}/works/{ol_id}.json"
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()

    author = None
    if data.get("authors"):
        author_data = data["authors"][0]
        author_key = author_data.get("author", {}).get("key", "")
        if author_key:
            author = await _get_author_name(author_key)

    description = None
    desc_data = data.get("description")
    if desc_data:
        if isinstance(desc_data, dict):
            description = desc_data.get("value", "")
        else:
            description = desc_data

    subjects = data.get("subjects", [])

    cover_url = None
    if data.get("covers"):
        cover_url = f"https://covers.openlibrary.org/b/id/{data['covers'][0]}-L.jpg"

    return BookDetail(
        ol_id=ol_id,
        title=data.get("title", "Unknown"),
        author=author,
        description=description,
        first_publish_year=data.get("first_publish_date"),
        cover_url=cover_url,
        subjects=subjects[:10],
        pages=data.get("number_of_pages_median"),
    )


async def _get_author_name(author_key: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{OPEN_LIBRARY_BASE}{author_key}.json")
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data.get("name")
