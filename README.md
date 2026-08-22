# OpenShelf 📚

A RESTful API for searching books and managing personal reading lists, powered by the [Open Library](https://openlibrary.org) public API.

**Live API:** [link](https://openshelf-pbk0.onrender.com)

**Interactive docs:** [link](https://openshelf-pbk0.onrender.com/docs)

## What It Does

OpenShelf lets users search for books by title, author, or subject using Internet Archive's Open Library public API, and maintain a personal reading list. All reading list operations are user-specific and secured with JWT authentication.

## Tech Stack

- **FastAPI** — async-first Python web framework
- **PostgreSQL** — relational database for structured user and reading list data
- **SQLAlchemy** — ORM for database interactions
- **httpx** — async HTTP client for Open Library API calls
- **JWT (python-jose)** — stateless authentication
- **Docker** — containerised local development
- **Render** — free web service host
- **Neon** — free serverless PostgreSQL provider

## Architecture Decisions

**FastAPI over Flask:** FastAPI's async support means book search requests to Open Library's external API don't block the server — other requests can be handled while waiting for the external response.

**PostgreSQL over MongoDB:** User accounts and reading lists have a natural relational structure — a user has many reading list items. SQL foreign keys enforce this relationship and prevent orphaned data. MongoDB's flexibility isn't needed here.

**JWT over sessions:** Stateless authentication means the server stores nothing between requests. Identity is always resolved from the verified token — never from the request body — preventing impersonation.

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Sanket17052006/openshelf.git
cd openshelf

# Start the app and database
docker compose up -d

# API is now running at
http://localhost:8000

# Interactive docs
http://localhost:8000/docs
```

## API Endpoints

Authentication: All endpoints except `/auth/register` and `/auth/login` require a Bearer JWT token in the `Authorization` header.

 POST  `/auth/register` - Create a new account 
 POST  `/auth/login` - Login and receive JWT token
 GET  `/books/search?q=` - Search books by title, author or subject
 GET  `/books/{ol_id}` - Get details of a specific book
 POST  `/list/add` - Add a book to your reading list 
 GET  `/list` - Get your reading list
 DELETE  `/list/{ol_id}` - Remove a book from your reading list
 GET  `/health` - Health check

## Example Usage

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "sanket", "password": "secret"}'

# Login and get token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "sanket", "password": "secret"}'

# Search books
curl http://localhost:8000/books/search?q=robinson+crusoe \
  -H "Authorization: Bearer <your_token>"
```
