# GitHub Repository Tracker – FastAPI Backend Assessment

## Problem Understanding & Assumptions

### Interpretation

The goal of this assignment is to build a **robust REST API service** using **FastAPI** and **PostgreSQL** that demonstrates:

* Proper state management using a relational database
* Integration with an external API
* Strict request and response validation
* Clean architecture, testing, and documentation

The service must expose **exactly four REST endpoints** (POST, GET, PUT, DELETE), all of which interact with the database.

### Use Case Chosen

**GitHub Repository Tracker**

The application allows users to:

* Submit a GitHub repository reference (owner + repo name)
* Fetch live metadata from the GitHub API
* Persist selected metadata in PostgreSQL
* Perform CRUD operations on stored repository records

This use case was chosen because:

* GitHub provides a reliable, real-world public API
* It naturally demonstrates external API integration
* It keeps user input minimal while showcasing data enrichment

### Assumptions (Mandatory)

* Users are **not authenticated** (authentication was not required in the prompt)
* GitHub API is publicly accessible without authentication (rate limits are acceptable for demo)
* Only essential repository metadata (stars) is stored to keep schema simple
* External API failures should not crash the service
* Exactly four endpoints are required, so no additional APIs (health checks, auth, etc.) were added

---

## Design Decisions

### Database Schema

Table: `repositories`

| Column    | Type         | Reason                         |
| --------- | ------------ | ------------------------------ |
| id        | UUID (PK)    | Globally unique, safe for APIs |
| owner     | VARCHAR(100) | GitHub username                |
| repo_name | VARCHAR(100) | Repository name                |
| stars     | INTEGER      | Key metric from GitHub         |

**Indexing**:

* Composite index on `(owner, repo_name)` to optimize lookups and avoid duplicates

### Project Structure

The project follows a **Layered Architecture**:

```
app/
├── api.py        # API routes (presentation layer)
├── services/     # External API logic
├── crud.py       # Database operations
├── models.py    # ORM models
├── schemas.py   # Pydantic validation
├── database.py  # DB connection
├── main.py      # Application entry point
```

This separation improves:

* Maintainability
* Testability
* Clarity of responsibilities

### Validation Logic

Validation is enforced using **Pydantic models**:

* Request bodies validated automatically by FastAPI
* Field constraints (min/max length)
* Response schemas ensure consistent output

Invalid data never reaches the business logic or database.

### External API Design

* GitHub REST API is accessed using `httpx.AsyncClient`
* Timeout of 5 seconds is enforced
* Errors from GitHub are gracefully handled and converted into user-friendly responses
* External logic is isolated in a service layer to simplify mocking during tests

---

##  Solution Approach (Data Flow)

1. **Client sends POST request** with `owner` and `repo_name`
2. **FastAPI validates input** using Pydantic
3. **Service layer calls GitHub API** to fetch live repository data
4. **Relevant fields are extracted** (stars)
5. **Data is persisted** in PostgreSQL via SQLAlchemy ORM
6. **Structured response** is returned to the client

For GET, PUT, and DELETE requests:

* Data is fetched directly from PostgreSQL
* Database acts as the single source of truth

---

##  Error Handling Strategy

The application uses **centralized error handling**:

### Handled Failures

| Scenario           | Strategy                             |
| ------------------ | ------------------------------------ |
| Invalid request    | 422 via Pydantic                     |
| Record not found   | 404 HTTPException                    |
| GitHub API failure | Graceful ValueError + global handler |
| Database issues    | SQLAlchemy transaction safety        |

### Global Exception Handler

A FastAPI exception handler captures and formats unexpected errors, preventing application crashes and ensuring consistent responses.

Logging is enabled to track:

* API requests
* External API failures
* Critical operations

---

##  How to Run the Project

### Option 1: Local Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

### Option 2: Docker (Recommended)

```bash
docker-compose up --build
```

---

## 🔐 Environment Variables

`.env.example`

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/githubdb
```

---

## 📬 Example API Calls

### Create Repository (POST)

```bash
curl -X POST http://localhost:8000/repos \
-H "Content-Type: application/json" \
-d '{"owner": "fastapi", "repo_name": "fastapi"}'
```

### Get Repository (GET)

```bash
curl http://localhost:8000/repos/{repo_id}
```

### Update Repository (PUT)

```bash
curl -X PUT http://localhost:8000/repos/{repo_id}
```

### Delete Repository (DELETE)

```bash
curl -X DELETE http://localhost:8000/repos/{repo_id}
```

---

##  Testing

* Pytest is used for unit and integration testing
* External API calls are designed to be mockable
* Tests validate endpoint behavior and data flow

---

##  Final Notes

This project demonstrates:

* Clean backend architecture
* Robust data handling
* External API integration
* Strong validation and error handling

It fully satisfies the requirements of the **Python Backend Engineer Take-Home Assessment**.
