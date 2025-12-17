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
docker compose up -d postgres

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

### SIXTH TASK: Create Frontend Handoff Documentation

Create comprehensive documentation for frontend developers (Figma Make) to understand and integrate with the API.

This task creates documentation that will be handed off to Figma Make or other frontend tools to build the UI.

#### 6.1: Create docs/ directory

```bash
mkdir -p docs/mock-data
mkdir -p scripts
```

#### 6.2: Create APP_OVERVIEW.md

Based on the `app_spec.txt` file you read earlier, create `docs/APP_OVERVIEW.md`.

This file provides **business context and user workflows** for frontend developers.

**Structure to follow:**
1. **Purpose Section** - Extract from app_spec.txt overview (what problem does this solve?)
2. **User Roles & Permissions** - Extract from app_spec.txt business rules
3. **Core User Workflows** - Extract from "User Workflows & Journeys" section
   - Include 5-10 step-by-step workflows showing how users accomplish goals
   - Include success criteria and error cases for each workflow
4. **Suggested Screens/Views** - Suggest screens based on workflows and resources
   - Organize by user role (Public, User, Manager, Admin)
   - For each screen: describe purpose, key elements, interactions, navigation
5. **Data Relationships & Display Patterns** - Describe how data should be displayed
   - List views, detail views, reusable components
   - Common UI patterns (badges, avatars, etc.)
6. **Navigation Structure** - Suggest app navigation hierarchy
7. **Key Features by Priority** - Extract from app_spec.txt priority section
8. **Design Considerations** - Information hierarchy, responsive behavior
9. **Integration with Mock Data** - Emphasize using mock data for UI development

**Writing tips:**
- Write for **UI designers and frontend developers**, not backend developers
- Focus on **user experience and workflows**, not implementation details
- Be **specific** about suggested screens and interactions
- Reference mock data files for each entity
- Use the templates in `prompts/templates/APP_OVERVIEW_TEMPLATE.md` as a guide

**Example excerpt:**
```markdown
# Task Management API - Application Overview

## Purpose
A task management system that enables teams to create, assign, and track tasks with priorities, due dates, and collaborative comments. Designed for small to medium teams (5-50 users) who need basic project management without complex features.

## User Roles & Permissions

### Admin
**Capabilities:**
- Full system access
- Create/edit/delete any user
- Manage system settings
- View all tasks across organization

[etc...]
```

#### 6.3: Create FRONTEND_HANDOFF.md

Create `docs/FRONTEND_HANDOFF.md` with technical integration details.

This file provides **technical API integration guidance** for frontend developers.

**Structure:**
1. **Quick Start** - How to run the backend locally (commands)
2. **Authentication** - Current mock auth setup, future JWT plans
3. **Data Models** - TypeScript/JavaScript interfaces for each entity
   - Convert Pydantic schemas to TypeScript interfaces
   - Include all fields with types
   - Document relationships (has many, belongs to)
   - Reference mock data file for each entity
4. **API Endpoints** - Summary of key endpoints by resource
   - Method + Path
   - Brief description
   - Key parameters
   - Response format example
   - Common errors
   - Point to openapi.json for full details
5. **Common Patterns** - Pagination format, error response format, timestamps
6. **Example Integration** - Code examples (JavaScript/TypeScript)
   - How to fetch data with mock data
   - How to fetch data from real API
   - How to switch between them
7. **Testing the API** - How to use Swagger UI, cURL examples
8. **Resources** - Links to APP_OVERVIEW.md, mock-data/, openapi.json

**IMPORTANT:** Keep this file concise! Don't duplicate the entire OpenAPI spec. Focus on:
- Getting started quickly
- Common patterns and conventions
- Code examples
- Pointers to full documentation

Use the template in `prompts/templates/FRONTEND_HANDOFF_TEMPLATE.md` as a guide.

#### 6.4: Generate Mock Data Files

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

#### 6.5: Create Mock Data README

Create `docs/mock-data/README.md` using the template in `prompts/templates/MOCK_DATA_README_TEMPLATE.md`.

This file explains:
- What each mock data file contains
- Example records from each file
- How to use the mock data in frontend code (with code examples)
- How to simulate relationships and filtering
- How to switch between mock data and real API

**Key sections:**
1. Overview - Why use mock data
2. Available Files - List each JSON file with examples
3. How to Use - Code examples in React/Vue/Svelte
4. Common Operations - Filtering, sorting, pagination, relationships
5. Switching to Real API - How to toggle between mock and real data
6. Data Integrity - Explanation of how data aligns with schemas
7. Troubleshooting - Common issues and solutions

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
git add docs/ scripts/generate_mock_data.py
git status
git commit -m "Add frontend handoff documentation and mock data

- Added APP_OVERVIEW.md with user workflows and suggested screens
- Added FRONTEND_HANDOFF.md with technical integration guide
- Generated realistic mock data for all entities:
  * users.json (20 users with various roles)
  * tasks.json (50 tasks with assignments and statuses)
  * tags.json (10 tags with colors)
  * comments.json (30 comments on tasks)
- Created mock data generation script (scripts/generate_mock_data.py)
- Added mock data usage guide (docs/mock-data/README.md)
- Ready for Figma Make handoff"
```

**Handoff Package Complete!**

At this point, you have created a complete handoff package:
- ✅ `docs/APP_OVERVIEW.md` - Business context and workflows for UI designers
- ✅ `docs/FRONTEND_HANDOFF.md` - Technical integration guide for developers
- ✅ `docs/mock-data/*.json` - Realistic sample data files
- ✅ `docs/mock-data/README.md` - Mock data usage guide
- ✅ `scripts/generate_mock_data.py` - Script to regenerate mock data
- ✅ `openapi.json` - Complete API specification (if available)

These files can be handed off to Figma Make or any frontend tool to build the UI without needing the backend running.

---

### SEVENTH TASK: Implement Mock Authentication

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
