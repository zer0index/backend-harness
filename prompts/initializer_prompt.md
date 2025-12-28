## YOUR ROLE - INITIALIZER AGENT (Session 1 of Many)

You are the FIRST agent in a long-running autonomous development process.
Your job is to set up the foundation for all future coding agents to build
a production-quality FastAPI backend.

### FIRST: Read the Project Specification

Start by reading `app_spec.txt` in your working directory. This file contains
the complete specification for the backend API you need to build. Read it carefully
before proceeding.

### CRITICAL FIRST TASK: Create feature_list.json

Based on `app_spec.txt`, create a file called `feature_list.json` with {{MIN_TESTS}}-{{MAX_TESTS}} detailed
API test cases. This file is the single source of truth for what needs to be built.

**Target:** {{MIN_ENDPOINTS}}-{{MAX_ENDPOINTS}} API endpoints, with {{TESTS_PER_ENDPOINT}} test cases per endpoint = {{MIN_TESTS}}-{{MAX_TESTS}} total tests

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
- {{MIN_TESTS}}-{{MAX_TESTS}} test cases total ({{MIN_ENDPOINTS}}-{{MAX_ENDPOINTS}} endpoints × {{TESTS_PER_ENDPOINT}} tests each)
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
├── docker-compose.yml       # PostgreSQL service (use with: docker compose)
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
7. **docker-compose.yml** - PostgreSQL 15+ with healthcheck (use with: docker compose)
8. **alembic.ini** - Database migration configuration
9. **.env.example** - Template for environment variables

### THIRD TASK: Create init.sh and init.ps1 (Setup Scripts)

Create TWO setup scripts for cross-platform compatibility:
- `init.sh` for Unix/Linux/macOS/Git Bash users
- `init.ps1` for Windows PowerShell users

**init.sh** (Bash version):

```bash
#!/bin/bash

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

# Start PostgreSQL with Docker (optional - skip if using SQLite)
echo "Starting PostgreSQL database..."
if command -v docker &> /dev/null; then
    if docker compose up -d postgres 2>/dev/null; then
        echo "  ✓ Docker database started"
        sleep 5
    else
        echo "  → Skipping Docker (using SQLite or already running)"
    fi
else
    echo "  → Docker not found - skipping (project may use SQLite)"
fi

# Run database migrations (optional - skip if app auto-creates schema)
echo "Running database migrations..."
if python -m alembic upgrade head 2>/dev/null; then
    echo "  ✓ Migrations applied successfully"
else
    echo "  → Skipping migrations (app may auto-create schema on startup)"
fi

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

**init.ps1** (PowerShell version for Windows users):
```powershell
# init.ps1 - PowerShell setup script for Windows
Write-Host "=== Backend Development Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check for Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python 3 is required but not installed" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start PostgreSQL with Docker (optional - skip if using SQLite)
Write-Host "Starting PostgreSQL database..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    try {
        docker compose up -d postgres 2>$null
        Write-Host "  Docker database started" -ForegroundColor Green
        Start-Sleep -Seconds 5
    } catch {
        Write-Host "  Skipping Docker (using SQLite or already running)" -ForegroundColor Gray
    }
} else {
    Write-Host "  Docker not found - skipping (project may use SQLite)" -ForegroundColor Gray
}

# Run database migrations (optional - skip if app auto-creates schema)
Write-Host "Running database migrations..." -ForegroundColor Yellow
try {
    python -m alembic upgrade head 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Migrations applied successfully" -ForegroundColor Green
    } else {
        Write-Host "  Skipping migrations (app may auto-create schema on startup)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  Alembic not configured - skipping (app may auto-create schema on startup)" -ForegroundColor Gray
}

# Run tests to verify setup
Write-Host "Running tests..." -ForegroundColor Yellow
pytest -v

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server:"
Write-Host "  uvicorn app.main:app --reload --port 8000"
Write-Host ""
Write-Host "API will be available at:"
Write-Host "  http://localhost:8000"
Write-Host "  http://localhost:8000/docs (Swagger UI)"
Write-Host "  http://localhost:8000/redoc (ReDoc)"
Write-Host ""
Write-Host "To run tests:"
Write-Host "  pytest -v"
Write-Host "  pytest --cov=app --cov-report=term-missing"
Write-Host ""
```

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

### SIXTH TASK: Create Lean Frontend Handoff Package

Create a minimal, non-redundant handoff package for frontend developers using:
- **app_spec.txt** (business context - already exists)
- **openapi.json** (API spec - auto-generated)
- **mock-data/** (realistic sample data)
- **QUICKSTART.md** (simple integration guide)

**Philosophy:** Avoid duplication. Use existing sources of truth instead of reformatting them.

#### 6.1: Setup Directories

```bash
mkdir -p docs/mock-data
mkdir -p scripts
```

#### 6.2: Copy App Specification

Copy the app specification to the handoff package:

```bash
# The app_spec.txt already contains business context, workflows, and feature priorities
cp app_spec.txt docs/app_spec.txt
```

**Why include this?**
- Provides business context (what the app does, who uses it)
- Explains user workflows and journeys
- Suggests screens and features
- Defines feature priorities (MVP vs. nice-to-have)

Frontend developers read this to understand **what to build and why**.

#### 6.3: Generate Mock Data Files

Create realistic mock data that perfectly mirrors your data models.

**Step 1:** Install faker library (if not in dependencies):
```bash
pip install faker
```

**Step 2:** Create `scripts/generate_mock_data.py`

This script should generate realistic mock data for all entities:

```python
#!/usr/bin/env python3
"""Generate realistic mock data for frontend development."""

from faker import Faker
import json
from datetime import datetime, timedelta
import random
from pathlib import Path

fake = Faker()
Faker.seed(42)  # For reproducible data
random.seed(42)

# Output directory
output_dir = Path('docs/mock-data')
output_dir.mkdir(parents=True, exist_ok=True)

print("Generating mock data...")

# Generate Users ({{MOCK_USERS}} users)
print("- Generating users...")
users = []
roles = ["admin", "manager", "user"]
role_distribution = [1, 3, 16]  # 1 admin, 3 managers, rest users

for i in range(1, {{MOCK_USERS}} + 1):
    if i == 1:
        role = "admin"
    elif i <= 4:
        role = "manager"
    else:
        role = "user"

    users.append({
        "id": i,
        "email": fake.email(),
        "name": fake.name(),
        "role": role,
        "is_active": random.choice([True] * 9 + [False]),  # 90% active
        "created_at": fake.date_time_between(start_date='-1y').isoformat() + 'Z',
        "updated_at": fake.date_time_between(start_date='-30d').isoformat() + 'Z'
    })

# Save users
with open(output_dir / 'users.json', 'w') as f:
    json.dump(users, f, indent=2)
print(f"  ✓ Generated {len(users)} users")

# Generate Tasks ({{MOCK_MAIN_ENTITY}} tasks/main entities)
print("- Generating tasks...")
tasks = []
statuses = ["pending", "in_progress", "completed", "cancelled"]
priorities = ["low", "medium", "high", "urgent"]

for i in range(1, {{MOCK_MAIN_ENTITY}} + 1):
    creator = random.choice(users)
    # 80% of tasks are assigned
    assignee = random.choice(users) if random.random() > 0.2 else None
    status = random.choice(statuses)
    created = fake.date_time_between(start_date='-60d')
    due = created + timedelta(days=random.randint(7, 60))

    task = {
        "id": i,
        "title": fake.sentence(nb_words=6).rstrip('.'),
        "description": fake.paragraph(nb_sentences=3) if random.random() > 0.2 else None,
        "status": status,
        "priority": random.choice(priorities),
        "assignee_id": assignee["id"] if assignee else None,
        "creator_id": creator["id"],
        "due_date": due.isoformat() + 'Z',
        "completed_at": (created + timedelta(days=random.randint(1, 30))).isoformat() + 'Z' if status == "completed" else None,
        "created_at": created.isoformat() + 'Z',
        "updated_at": fake.date_time_between(start_date=created).isoformat() + 'Z'
    }
    tasks.append(task)

with open(output_dir / 'tasks.json', 'w') as f:
    json.dump(tasks, f, indent=2)
print(f"  ✓ Generated {len(tasks)} tasks")

# Generate Tags ({{MOCK_SECONDARY}} tags/secondary entities)
print("- Generating tags...")
tag_names = ["Backend", "Frontend", "Bug", "Feature", "Documentation", "Testing", "DevOps", "Design", "Research", "Urgent"]
colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FF33F3", "#33FFF3", "#F3FF33", "#FF8C33", "#8C33FF", "#33FF8C"]

tags = []
for i, (name, color) in enumerate(zip(tag_names[:{{MOCK_SECONDARY}}], colors[:{{MOCK_SECONDARY}}]), 1):
    tags.append({
        "id": i,
        "name": name,
        "color": color,
        "created_at": fake.date_time_between(start_date='-1y').isoformat() + 'Z'
    })

with open(output_dir / 'tags.json', 'w') as f:
    json.dump(tags, f, indent=2)
print(f"  ✓ Generated {len(tags)} tags")

# Generate Comments ({{MOCK_SECONDARY}}*3 comments - roughly 3x secondary entities)
print("- Generating comments...")
comments = []
num_comments = {{MOCK_SECONDARY}} * 3
for i in range(1, num_comments + 1):
    task = random.choice(tasks)
    user = random.choice(users)
    created = fake.date_time_between(
        start_date=datetime.fromisoformat(task["created_at"].rstrip('Z')),
        end_date='now'
    )

    comments.append({
        "id": i,
        "task_id": task["id"],
        "user_id": user["id"],
        "content": fake.paragraph(nb_sentences=random.randint(1, 3)),
        "created_at": created.isoformat() + 'Z',
        "updated_at": created.isoformat() + 'Z'
    })

with open(output_dir / 'comments.json', 'w') as f:
    json.dump(comments, f, indent=2)
print(f"  ✓ Generated {len(comments)} comments")

print("\nMock data generation complete!")
print(f"Files created in {output_dir}/")
```

**Step 3:** Run the script:
```bash
chmod +x scripts/generate_mock_data.py
python scripts/generate_mock_data.py
```

**Step 4:** Verify the files were created:
```bash
ls -la docs/mock-data/
```

You should see: `users.json`, `tasks.json`, `tags.json`, `comments.json`

#### 6.4: Create Mock Data README

Create `docs/mock-data/README.md` using the template in `prompts/templates/MOCK_DATA_README_TEMPLATE.md`.

This file explains:
- What each mock data file contains
- Example records from each file
- Field types and relationships
- How to use the mock data in frontend code

**Key sections:**
1. Overview - Why use mock data
2. Available Files - List each JSON file with examples and field descriptions
3. How to Use - Code examples showing import and usage
4. Data Integrity - How data aligns with backend schemas

#### 6.5: Create QUICKSTART.md

Create `docs/QUICKSTART.md` using the template in `prompts/templates/QUICKSTART_TEMPLATE.md`.

This is a **simple 1-page guide** that tells frontend developers:
1. **What's Included** - Table showing app_spec.txt, openapi.json, mock-data/ and their purposes
2. **Quick Start Steps**:
   - Read app_spec.txt for business context
   - Explore API via Swagger UI or generate TypeScript types from openapi.json
   - Build UI with mock data
   - Swap mock data for real API calls when ready
3. **Key Concepts** - Authentication, pagination, error handling
4. **Development Workflow** - Design with mock data → integrate with API → test
5. **Reference Links** - Where to find complete documentation

**Keep it concise!** This should be a 5-minute read that gets developers started quickly.

The template provides all the content - you just need to create the file.

#### 6.6: Export OpenAPI Specification

After you've set up the FastAPI application structure (main.py with basic routes):

**Option 1:** If you have basic endpoints set up:
```bash
# Start FastAPI server temporarily
uvicorn app.main:app --port 8000 &
UVICORN_PID=$!
sleep 5

# Export OpenAPI spec
curl http://localhost:8000/openapi.json > openapi.json

# Stop server
pkill -P $UVICORN_PID || pkill uvicorn

# Verify
ls -lh openapi.json
```

**Option 2:** If endpoints aren't ready yet:
- Skip this step for now
- The coding agent will export openapi.json after implementing endpoints
- Add a TODO comment in claude-progress.txt to export it later

#### 6.7: Add to Git

Commit the handoff documentation:

```bash
git add docs/ scripts/generate_mock_data.py openapi.json
git status
git commit -m "Add lean frontend handoff package

- Copied app_spec.txt to docs/ (business context and workflows)
- Created QUICKSTART.md with integration guide
- Generated realistic mock data for all entities:
  * users.json (20 users with various roles)
  * tasks.json (50 tasks with assignments and statuses)
  * tags.json (10 tags with colors)
  * comments.json (30 comments on tasks)
- Created mock data generation script (scripts/generate_mock_data.py)
- Added mock data field guide (docs/mock-data/README.md)
- Exported openapi.json (complete API specification)
- Ready for frontend development (no backend dependency needed)"
```

**Lean Handoff Package Complete!**

At this point, you have created a complete, non-redundant handoff package:
- ✅ `docs/app_spec.txt` - Business context, workflows, and feature priorities (source: original spec)
- ✅ `docs/QUICKSTART.md` - Simple 1-page integration guide
- ✅ `docs/mock-data/*.json` - Realistic sample data files
- ✅ `docs/mock-data/README.md` - Mock data field guide
- ✅ `scripts/generate_mock_data.py` - Script to regenerate mock data
- ✅ `openapi.json` - Complete API specification (auto-generated by FastAPI)

**Why this is better:**
- ✅ No duplication (app_spec.txt is the source of truth for business context)
- ✅ No manual maintenance (openapi.json is auto-generated)
- ✅ Less to read (QUICKSTART.md is 1 page vs. multiple long docs)
- ✅ No sync issues (using source files instead of reformatted copies)

Frontend developers can start building immediately using mock data and refer to openapi.json for API details.

---

### SIXTH-POINT-FIVE: OpenAPI Best Practices (CRITICAL)

Before implementing authentication and endpoints, establish these OpenAPI standards that will apply to ALL endpoints:

#### 6.5.1: Standardized Error Responses

Create `app/schemas/common.py` with reusable error and pagination schemas:

```python
"""Common schemas used across all API endpoints."""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Any

class ErrorResponse(BaseModel):
    """
    Standardized error response for all API errors.

    Used for 401, 403, 404, 409, 422, 429, 500 responses.
    """
    code: str = Field(..., description="Machine-readable error code (e.g., 'USER_NOT_FOUND')")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(None, description="Additional error context")
    request_id: str | None = Field(None, description="Request ID for tracing")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "USER_NOT_FOUND",
                "message": "User with ID 123 not found",
                "details": {"user_id": 123},
                "request_id": "req_abc123"
            }
        }


class MessageResponse(BaseModel):
    """Simple message response for operations that don't return data."""
    message: str = Field(..., description="Operation result message")

    class Config:
        json_schema_extra = {
            "example": {"message": "User deleted successfully"}
        }


# Pagination (for list endpoints)
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standardized pagination response for list endpoints.

    Use this for ALL endpoints that return lists.
    """
    items: list[T] = Field(..., description="List of items in this page")
    total: int = Field(..., description="Total count of all items")
    limit: int = Field(..., description="Page size requested")
    offset: int = Field(..., description="Starting position")
    count: int = Field(..., description="Actual items in this response")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [...],
                "total": 100,
                "limit": 20,
                "offset": 0,
                "count": 20
            }
        }
```

**Define common HTTP error responses to reuse across endpoints:**

Create `app/schemas/errors.py`:

```python
"""Common error response definitions for OpenAPI documentation."""

from app.schemas.common import ErrorResponse

# Reusable error responses for OpenAPI
COMMON_RESPONSES = {
    401: {
        "model": ErrorResponse,
        "description": "Unauthorized - Missing or invalid authentication token",
        "content": {
            "application/json": {
                "example": {
                    "code": "UNAUTHORIZED",
                    "message": "Authentication required",
                }
            }
        }
    },
    403: {
        "model": ErrorResponse,
        "description": "Forbidden - Insufficient permissions for this operation",
        "content": {
            "application/json": {
                "example": {
                    "code": "FORBIDDEN",
                    "message": "You do not have permission to perform this action",
                }
            }
        }
    },
    404: {
        "model": ErrorResponse,
        "description": "Not Found - Requested resource does not exist",
        "content": {
            "application/json": {
                "example": {
                    "code": "NOT_FOUND",
                    "message": "Resource not found",
                }
            }
        }
    },
    409: {
        "model": ErrorResponse,
        "description": "Conflict - Resource already exists or constraint violation",
        "content": {
            "application/json": {
                "example": {
                    "code": "ALREADY_EXISTS",
                    "message": "Email already registered",
                }
            }
        }
    },
    422: {
        "model": ErrorResponse,
        "description": "Validation Error - Invalid request data format or values",
    },
    429: {
        "model": ErrorResponse,
        "description": "Too Many Requests - Rate limit exceeded",
        "content": {
            "application/json": {
                "example": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "Too many requests, please try again later",
                }
            }
        }
    },
}
```

**Apply these to endpoints:**

```python
from app.schemas.errors import COMMON_RESPONSES

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    operation_id="createUser",
    responses={
        409: COMMON_RESPONSES[409],  # Email already exists
        422: COMMON_RESPONSES[422],  # Validation error
    }
)
async def create_user(user: UserCreate):
    """Create a new user account."""
    # ... implementation
    pass

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    operation_id="getUserById",
    responses={
        404: COMMON_RESPONSES[404],  # User not found
    }
)
async def get_user(user_id: int):
    """Get user by ID."""
    # ... implementation
    pass
```

#### 6.5.2: Response Schema Guidelines

**CRITICAL RULE: NEVER return empty response schemas `{}`**

Every endpoint must have EITHER:
1. **A defined Pydantic response model** (use `response_model=YourSchema`), OR
2. **HTTP 204 No Content** (use `status_code=204` with no body)

**Examples:**

```python
# ✅ GOOD: Endpoint with data returns explicit schema
@router.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int):
    return user_data

# ✅ GOOD: Endpoint without data returns 204
@router.delete("/users/{id}", status_code=204)
async def delete_user(id: int):
    # Perform deletion
    return Response(status_code=204)

# ✅ GOOD: Simple confirmation uses MessageResponse
from app.schemas.common import MessageResponse

@router.post("/users/{id}/activate", response_model=MessageResponse)
async def activate_user(id: int):
    # Perform activation
    return {"message": "User activated successfully"}

# ❌ BAD: Don't do this (creates empty schema {} in OpenAPI)
@router.get("/health")
async def health():
    return {"status": "ok"}  # Missing response_model!
```

#### 6.5.3: API Path Naming Conventions

Follow these rules consistently for ALL endpoints:

1. **NO trailing slashes**: `/api/v1/users` ✅ not `/api/v1/users/` ❌
2. **Lowercase with hyphens**: `/api/v1/user-profiles` ✅ not `/api/v1/userProfiles` ❌
3. **Plural nouns for collections**: `/api/v1/users` ✅ not `/api/v1/user` ❌
4. **Singular for single resource**: `/api/v1/users/{id}` ✅
5. **Action verbs for non-CRUD**: `/api/v1/users/{id}/activate` ✅

**Rationale:** FastAPI treats `/users` and `/users/` as DIFFERENT routes, causing client confusion.

#### 6.5.4: OperationId Naming Convention

Provide explicit, human-readable operation IDs for better SDK generation:

**Pattern:**
- `{verb}{Resource}` for single items: `getUser`, `updateUser`, `deleteUser`
- `{verb}{PluralResource}` for collections: `listUsers`, `createUser`
- `{verb}{Resource}{Action}` for actions: `activateUser`, `resetUserPassword`

**Examples:**

```python
@router.get("/users", operation_id="listUsers")
async def list_users(): pass

@router.post("/users", operation_id="createUser")
async def create_user(): pass

@router.get("/users/{id}", operation_id="getUserById")
async def get_user(): pass

@router.put("/users/{id}", operation_id="updateUser")
async def update_user(): pass

@router.delete("/users/{id}", operation_id="deleteUser")
async def delete_user(): pass

@router.post("/users/{id}/activate", operation_id="activateUser")
async def activate_user(): pass
```

**Why this matters:**
- Stable across code refactors (changing function names won't break generated clients)
- Cleaner SDK method names
- Easier to reference in documentation

#### 6.5.5: Pagination for List Endpoints

Use `PaginatedResponse` from `app/schemas/common.py` for ALL list endpoints:

```python
from fastapi import Query
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserResponse

@router.get(
    "/users",
    response_model=PaginatedResponse[UserResponse],
    operation_id="listUsers"
)
async def list_users(
    limit: int = Query(default=20, ge=1, le=100, description="Page size"),
    offset: int = Query(default=0, ge=0, description="Starting position"),
    db: AsyncSession = Depends(get_db),
):
    """
    List all users with pagination.

    Returns paginated list of users.
    """
    # Get total count
    total_query = select(func.count()).select_from(User)
    total_result = await db.execute(total_query)
    total = total_result.scalar()

    # Get paginated items
    query = select(User).offset(offset).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "items": users,
        "total": total,
        "limit": limit,
        "offset": offset,
        "count": len(users),
    }
```

#### 6.5.6: Privacy & Security Schema Guidelines

**NEVER expose internal database IDs in anonymous/discovery contexts.**

If your application has privacy requirements:

```python
# ❌ BAD: Exposes real user ID in anonymous discovery
class BuddyCard(BaseModel):
    candidate_id: int  # Real database ID!
    name: str

# ✅ GOOD: Uses opaque token instead
import uuid

class BuddyCard(BaseModel):
    card_token: str  # Opaque UUID that maps to user internally
    name: str

# Backend generates token:
card_token = str(uuid.uuid4())
# Store mapping: card_token -> user_id in database or cache
```

**NEVER use untyped dicts for structured data.**

```python
# ❌ BAD: Untyped settings (creates additionalProperties: true)
class UserResponse(BaseModel):
    privacy_settings: dict  # Unknown structure!

# ✅ GOOD: Explicit nested schema
class PrivacySettings(BaseModel):
    profile_visible: bool = True
    show_location: bool = True
    allow_discovery: bool = True

class UserResponse(BaseModel):
    privacy_settings: PrivacySettings  # Strongly typed
```

---

### SEVENTH TASK: Implement Mock Authentication with OpenAPI Security Schemes

Since real authentication will be implemented later, create a mock auth system **with proper OpenAPI documentation**:

**app/dependencies/auth.py**:
```python
"""Mock authentication for development."""

from typing import Annotated
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Security scheme for OpenAPI documentation
security = HTTPBearer()

# Mock user for all requests
MOCK_USER = {
    "id": 1,
    "email": "test@example.com",
    "name": "Test User",
    "role": "admin"
}

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]
) -> dict:
    """
    Mock authentication dependency.

    Always returns the MOCK_USER for development.
    In production, this will validate JWT tokens.

    Args:
        credentials: HTTP Bearer token (required for OpenAPI but ignored in mock)

    Returns:
        Mock user dict with id, email, name, role
    """
    # TODO: Replace with real JWT validation
    # For now, accept any token and return mock user
    return MOCK_USER

async def get_current_user_optional(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(security)] = None
) -> dict | None:
    """
    Optional authentication dependency for public endpoints.

    Returns user if authenticated, None otherwise.
    """
    if credentials:
        return MOCK_USER
    return None
```

**CRITICAL: Configure OpenAPI Security in app/main.py**

When creating your FastAPI app, configure it with proper security schemes and servers:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Your API Name",  # From app_spec.txt
    version="1.0.0",
    description="Description from app_spec.txt",
    # IMPORTANT: Configure servers for different environments
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://staging.yourdomain.com",
            "description": "Staging environment"
        },
        {
            "url": "https://api.yourdomain.com",
            "description": "Production environment"
        }
    ],
    # Security scheme will be auto-detected from HTTPBearer dependency
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For public endpoints (like /health), explicitly mark as unauthenticated:**

```python
from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    """Health check response - NEVER use empty schema {}"""
    status: str
    version: str
    environment: str

@router.get(
    "/health",
    response_model=HealthResponse,
    operation_id="healthCheck",  # Human-readable operation ID
    tags=["health"],
    summary="Health check endpoint",
    # CRITICAL: Mark as public (no auth required)
    dependencies=[],  # No auth dependency
)
async def health_check():
    """
    Health check endpoint - returns API status.

    This endpoint is public and does not require authentication.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development"
    }
```

**For protected endpoints, include the auth dependency:**

```python
from fastapi import Depends
from app.dependencies.auth import get_current_user

@router.get(
    "/users/me",
    response_model=UserResponse,
    operation_id="getCurrentUser",  # Human-readable operation ID
    tags=["users"],
    summary="Get current user profile",
    # Protected endpoint - requires authentication
    dependencies=[Depends(get_current_user)],
)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """Get the currently authenticated user's profile."""
    return current_user
```

**Why this matters:**
- ✅ OpenAPI spec will show proper `securitySchemes.bearerAuth`
- ✅ Swagger UI will have "Authorize" button
- ✅ Public endpoints clearly marked with `security: []`
- ✅ Protected endpoints show lock icon in docs
- ✅ Generated SDKs will handle auth correctly

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
