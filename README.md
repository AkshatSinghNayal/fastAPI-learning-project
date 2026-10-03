# FastAPI Learning Project

## Dev Day 1

This project is a Day 1 FastAPI learning exercise that builds a small blog
API. It covers:

- Creating a FastAPI application
- Defining SQLAlchemy models and SQLite persistence
- Validating request and response data with Pydantic
- Creating and verifying JWT bearer tokens
- Protecting the blog creation endpoint with a dependency

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- `python-jose`

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the development server from the project directory:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

The SQLite database is created as `test.db` when the application starts.

## API routes

| Method | Route | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/login` | Returns a bearer access token for the demo user | No |
| `POST` | `/blogs` | Creates a blog post | Bearer token |
| `GET` | `/getBlogs` | Lists all blog posts | No |
| `GET` | `/blog/{id}` | Gets one blog post by ID | No |
| `PUT` | `/update/{id}` | Updates a blog post by ID | No |
| `DELETE` | `/delete/{id}` | Deletes a blog post by ID | No |

To create a post, first call `POST /login`, copy the returned token, and send
it as an HTTP header:

```text
Authorization: Bearer <access-token>
```

Example request body:

```json
{
  "title": "My first blog",
  "content": "Learning FastAPI on Dev Day 1."
}
```

## Project structure

```text
auth.py      JWT creation and bearer-token verification
database.py  SQLite engine and SQLAlchemy session setup
main.py      FastAPI application and blog routes
models.py    SQLAlchemy Blog model
schemas.py   Pydantic request and response schemas
```

## Learning note

This is an educational project. The JWT secret in `auth.py` is intentionally
simple for local learning and should be replaced with a secure environment
variable before using a similar API in production.
