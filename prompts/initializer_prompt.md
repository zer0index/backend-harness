## YOUR ROLE - INITIALIZER AGENT (Session 1 of Many)

You are the FIRST agent in a long-running autonomous development process.
Your job is to set up the foundation for all future coding agents to build
a production-quality FastAPI backend.

### FIRST: Read the Project Specification

Start by reading `app_spec.txt` in your working directory. This file contains
the complete specification for the backend API you need to build. Read it carefully
before proceeding.

### CRITICAL FIRST TASK: Create feature_list.json

Based on `app_spec.txt`, create a file called `feature_list.json` with 100-200 detailed
API test cases. This file is the single source of truth for what needs to be built.

**Target:** 30-50 API endpoints, with 3-5 test cases per endpoint = 100-200 total tests

**Format:**
```json
[
  {
    "id": 1,
    "category": "endpoint",
    "method": "POST",
    "path": "/api/v1/users",
    "description": "Create a new user account",
    "request_schema": {
      "email": "string (required, valid email format)",
      "password": "string (required, min 8 chars)",
      "name": "string (required)",
      "role": "string (optional, default: 'user')"
    },
    "response_schema": {
      "id": "integer",
      "email": "string",
      "name": "string",
      "role": "string",
      "created_at": "datetime"
    },
    "test_cases": [
      {
        "name": "valid_user_creation",
        "description": "Create user with valid data",
        "input": {
          "email": "test@example.com",
          "password": "SecurePass123",
          "name": "Test User"
        },
        "expected_status": 201,
        "expected_response_contains": ["id", "email", "name", "created_at"]
      },
      {
        "name": "duplicate_email",
        "description": "Reject duplicate email address",
        "input": {
          "email": "existing@example.com",
          "password": "SecurePass123",
          "name": "Test User"
        },
        "expected_status": 409,
        "expected_error": "Email already registered"
      },
      {
        "name": "invalid_email_format",
        "description": "Reject invalid email format",
        "input": {
          "email": "not-an-email",
          "password": "SecurePass123",
          "name": "Test User"
        },
        "expected_status": 422,
        "expected_error": "Invalid email format"
      },
      {
        "name": "weak_password",
        "description": "Reject password shorter than 8 characters",
        "input": {
          "email": "test@example.com",
          "password": "weak",
          "name": "Test User"
        },
        "expected_status": 422,
        "expected_error": "Password must be at least 8 characters"
      },
      {
        "name": "missing_required_field",
        "description": "Reject request missing required field",
        "input": {
          "email": "test@example.com",
          "password": "SecurePass123"
        },
        "expected_status": 422,
        "expected_error": "name is required"
      }
    ],
    "passes": false
  },
  {
    "id": 2,
    "category": "endpoint",
    "method": "GET",
    "path": "/api/v1/users/{id}",
    "description": "Get user details by ID",
    "request_schema": {
      "id": "integer (path parameter)"
    },
    "response_schema": {
      "id": "integer",
      "email": "string",
      "name": "string",
      "role": "string",
      "created_at": "datetime"
    },
    "test_cases": [
      {
        "name": "get_existing_user",
        "description": "Retrieve user with valid ID",
        "input": {"id": 1},
        "expected_status": 200,
        "expected_response_contains": ["id", "email", "name"]
      },
      {
        "name": "user_not_found",
        "description": "Return 404 for non-existent user ID",
        "input": {"id": 99999},
        "expected_status": 404,
        "expected_error": "User not found"
      },
      {
        "name": "invalid_id_type",
        "description": "Reject non-numeric ID",
        "input": {"id": "abc"},
        "expected_status": 422,
        "expected_error": "Invalid user ID"
      }
    ],
    "passes": false
  }
]
```

**Test Categories:**

- **endpoint**: HTTP endpoint behavior (status codes, response format)
- **model**: Database model operations (CRUD, relationships, constraints)
- **business_logic**: Service layer business rules (validations, workflows)
- **integration**: Cross-feature flows (auth → create → list → update)
- **edge_case**: Error handling, limits, boundary conditions

**Requirements for feature_list.json:**
- 100-200 test cases total (30-50 endpoints × 3-5 tests each)
- Cover all CRUD operations for each resource
- Include authentication/authorization tests
- Test happy paths AND error cases (400s, 404s, 422s, etc.)
- Order endpoints by priority: core resources first
- ALL tests start with "passes": false
- Cover every requirement in app_spec.txt exhaustively

**CRITICAL INSTRUCTION:**
IT IS CATASTROPHIC TO REMOVE OR EDIT TESTS IN FUTURE SESSIONS.
Tests can ONLY be marked as passing (change "passes": false to "passes": true).
Never remove tests, never edit test_cases array, never modify schemas.
This ensures complete API coverage.

### SECOND TASK: Create FastAPI Project Structure

Set up a production-ready FastAPI project structure:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Async SQLAlchemy setup
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py          # Base model class
│   │   └── user.py          # Example: User model
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── user.py          # Example: UserCreate, UserResponse
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── users.py     # Example: /api/v1/users endpoints
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py  # Example: User business logic
│   └── dependencies/        # Dependency injection
│       ├── __init__.py
│       ├── auth.py          # Mock auth for now
│       └── database.py      # DB session dependency
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (client, db, auth)
│   └── api/
│       └── v1/
│           └── test_users.py  # Example: User endpoint tests
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── docker-compose.yml       # PostgreSQL service
├── alembic.ini
├── pyproject.toml           # Dependencies (or requirements.txt)
├── .env.example             # Environment variables template
├── feature_list.json        # Test specifications
├── init.sh                  # Setup script
└── README.md
```

**Key files to create:**

1. **app/main.py** - FastAPI application with CORS, exception handlers
2. **app/config.py** - Settings using pydantic-settings (database URL, secret key, etc.)
3. **app/database.py** - Async SQLAlchemy engine and session factory
4. **app/models/base.py** - Base model with common fields (id, created_at, updated_at)
5. **app/dependencies/auth.py** - Mock authentication that always returns a test user
6. **tests/conftest.py** - Fixtures for TestClient, test database, mock auth
7. **docker-compose.yml** - PostgreSQL 15+ with healthcheck
8. **alembic.ini** - Database migration configuration
9. **.env.example** - Template for environment variables

### THIRD TASK: Create init.sh

Create a script called `init.sh` that sets up the complete development environment:

```bash
#!/bin/bash
set -e

echo "=== Backend Development Environment Setup ==="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Start PostgreSQL with Docker
echo "Starting PostgreSQL database..."
docker-compose up -d postgres

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Run tests to verify setup
echo "Running tests..."
pytest -v

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To start the development server:"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "API will be available at:"
echo "  http://localhost:8000"
echo "  http://localhost:8000/docs (Swagger UI)"
echo "  http://localhost:8000/redoc (ReDoc)"
echo ""
echo "To run tests:"
echo "  pytest -v"
echo "  pytest --cov=app --cov-report=term-missing"
echo ""
```

Make the script executable: `chmod +x init.sh`

### FOURTH TASK: Create Dependencies Configuration

**pyproject.toml** (or requirements.txt):
```toml
[project]
name = "backend-api"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy[asyncio]>=2.0.25",
    "asyncpg>=0.29.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "alembic>=1.13.0",
    "python-jose[cryptography]>=3.3.0",  # For JWT (future)
    "passlib[bcrypt]>=1.7.4",  # For password hashing (future)
    "python-multipart>=0.0.6",  # For form data
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",  # For TestClient
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "black>=23.12.0",
    "mypy>=1.8.0",
]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d devdb"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**.env.example**:
```
DATABASE_URL=postgresql+asyncpg://devuser:devpassword@localhost:5432/devdb
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
```

### FIFTH TASK: Initialize Git

Create a git repository and make your first commit with:
- feature_list.json (complete with all 100-200 test specifications)
- FastAPI project structure (all directories and base files)
- init.sh (environment setup script)
- pyproject.toml or requirements.txt
- docker-compose.yml
- alembic.ini and alembic/ directory
- .env.example
- README.md (project overview and setup instructions)
- .gitignore (venv/, __pycache__/, .env, *.pyc, etc.)

Commit message: "Initial setup: FastAPI project structure, feature_list.json, and Docker PostgreSQL"

### SIXTH TASK: Implement Mock Authentication

Since real authentication will be implemented later, create a mock auth system:

**app/dependencies/auth.py**:
```python
"""Mock authentication for development."""

from typing import Annotated
from fastapi import Depends, HTTPException, Header

# Mock user for all requests
MOCK_USER = {
    "id": 1,
    "email": "test@example.com",
    "name": "Test User",
    "role": "admin"
}

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> dict:
    """
    Mock authentication dependency.

    Always returns the MOCK_USER for development.
    In production, this will validate JWT tokens.
    """
    # TODO: Replace with real JWT validation
    return MOCK_USER
```

### OPTIONAL: Start Implementation

If you have time remaining in this session, you may begin implementing
the highest-priority endpoints from feature_list.json. Remember:
- Work on ONE endpoint at a time
- Implement: model → schema → service → router → test
- Write pytest tests alongside implementation
- Run tests and ensure they pass before marking "passes": true
- Commit your progress incrementally

### ENDING THIS SESSION

Before your context fills up:
1. Commit all work with descriptive messages
2. Create `claude-progress.txt` with:
   - Summary of what you accomplished
   - Number of tests created in feature_list.json
   - Which endpoints (if any) were implemented
   - Next steps for the coding agent
3. Ensure feature_list.json is complete and saved
4. Ensure init.sh is executable and tested
5. Leave the environment in a clean, working state

The next agent will continue from here with a fresh context window.

---

**Remember:** You have unlimited time across many sessions. Focus on
quality over speed. Production-ready code with comprehensive test coverage is the goal.

**Key Differences from Frontend Development:**
- No browser automation - use pytest with TestClient
- No UI/visual tests - focus on API contracts
- Verification via HTTP status codes and response schemas
- Database state is part of test assertions
- Mock external dependencies (auth, external APIs) for now
