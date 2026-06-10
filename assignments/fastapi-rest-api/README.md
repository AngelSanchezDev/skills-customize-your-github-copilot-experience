# 📘 Assignment: FastAPI REST API

## 🎯 Objective

Build a REST API using FastAPI to handle requests, return JSON responses, and manage simple in-memory data.

## 📝 Tasks

### 🛠️ Create a basic FastAPI application

#### Description
Build the initial FastAPI app and add a working GET endpoint that returns a list of items.

#### Requirements
Completed program should:

- Define a FastAPI app instance.
- Create a GET endpoint at `/items/`.
- Return JSON data from the endpoint using a Python list or dictionary.
- Keep the app runnable with `uvicorn`.

### 🛠️ Add REST endpoints for item management

#### Description
Extend the API with endpoints to create and retrieve individual items using request bodies and path parameters.

#### Requirements
Completed program should:

- Define a Pydantic model for request/response data.
- Add a POST endpoint to create a new item.
- Add a GET endpoint to fetch a single item by its ID.
- Return appropriate HTTP status codes for success and missing items.

### 🛠️ Add query parameters and error handling

#### Description
Enhance the API with query filtering and clear error responses for invalid requests.

#### Requirements
Completed program should:

- Support a query parameter for listing or searching items.
- Raise an HTTP error when a requested item ID does not exist.
- Return JSON error details instead of plain text.
