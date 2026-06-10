# 📘 Assignment: FastAPI — JWT Authentication + SQLite

## 🎯 Objective

Implement token-based authentication (JWT) and persistent storage using SQLite in a FastAPI application. Students will secure endpoints and perform CRUD operations on user-owned resources.

## 📝 Tasks

### 🛠️ Implement authentication with JWT

#### Description
Add user registration and login endpoints that issue JSON Web Tokens (JWT). Implement password hashing and token verification.

#### Requirements
- Create endpoints to register users and to obtain access tokens.
- Hash passwords before storing them in the database.
- Issue JWTs with an expiration time and include the user identifier.
- Provide a dependency `get_current_user` that validates the token and returns the authenticated user.

### 🛠️ Persist data with SQLite and secure CRUD endpoints

#### Description
Use SQLite (via SQLAlchemy) to persist items. Only authenticated users should create, read, update, or delete their own items.

#### Requirements
- Define SQLAlchemy models and create the SQLite database.
- Add CRUD endpoints for items that enforce ownership.
- Return appropriate HTTP status codes and JSON error details for invalid requests.

### 🛠️ Add basic tests or manual verification steps (optional)

#### Description
Provide simple instructions or tests to verify authentication and persistence.

#### Requirements
- Include curl examples or a short script to obtain a token and call protected endpoints.

## ▶️ Setup & Run

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app with uvicorn from this folder:

```bash
uvicorn starter-code:app --reload
```

## ⏱️ Estimated time

90–150 minutes depending on familiarity with web security and databases.
