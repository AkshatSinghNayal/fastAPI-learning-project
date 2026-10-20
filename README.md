# FastAPI Learning Project

A small FastAPI application for learning how to build an API with SQLAlchemy and
Pydantic. The current implementation exposes a task-creation endpoint backed by
SQLite by default.

## Requirements

- Python 3.10 or newer
- `pip`

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, use `.venv\Scripts\Activate.ps1` instead.

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   DATABASE_URL=sqlite:///./blog.db
   ```

   `.env` and the local SQLite database are ignored by Git.

## Run the API

Start the development server with:

```bash
uvicorn main:app --reload
```

The API is available at <http://127.0.0.1:8000>. Interactive documentation is
available at <http://127.0.0.1:8000/docs>.

## API

### Create a task

`POST /tasks/create`

Example request:

```json
{
  "title": "Learn FastAPI",
  "description": "Build a task API with SQLAlchemy",
  "status": false
}
```

The endpoint returns a success message after the task is stored in the
database.

## Project structure

```text
.
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── src/
    ├── tasks/           # Task model, schema, controller, and routes
    ├── user/            # Reserved for user-related functionality
    └── utils/           # Settings and database configuration
```
