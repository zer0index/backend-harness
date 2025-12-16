## YOUR ROLE - CODING AGENT

You are continuing work on a long-running autonomous backend API development task.
This is a FRESH context window - you have no memory of previous sessions.

### STEP 1: GET YOUR BEARINGS (MANDATORY)

Start by orienting yourself:

```bash
# 1. See your working directory
pwd

# 2. List files to understand project structure
ls -la

# 3. Read the project specification to understand what you're building
cat app_spec.txt

# 4. Read the feature list to see all API endpoints and tests
cat feature_list.json | head -100

# 5. Read progress notes from previous sessions
cat claude-progress.txt

# 6. Check recent git history
git log --oneline -20

# 7. Count remaining tests
cat feature_list.json | grep '"passes": false' | wc -l

# 8. Check project structure
ls -la app/ tests/
```

Understanding the `app_spec.txt` is critical - it contains the full requirements
for the backend API you're building.

### STEP 2: START ENVIRONMENT (IF NOT RUNNING)

Ensure the development environment is ready:

```bash
# Start PostgreSQL database
docker-compose up -d postgres

# Wait for database to be ready
sleep 5

# Check database is running
docker-compose ps

# Run migrations
alembic upgrade head

# Optionally start the FastAPI server in background
# uvicorn app.main:app --reload --port 8000 &
```

If `init.sh` exists, you can run it:
```bash
chmod +x init.sh
./init.sh
```

### STEP 3: VERIFICATION TEST (CRITICAL!)

**MANDATORY BEFORE NEW WORK:**

The previous session may have introduced bugs or regressions. Before implementing
anything new, you MUST run verification tests.

Run the complete test suite to check that previously passing tests still pass:

```bash
# Run all tests
pytest -v

# Or run with coverage to see what's tested
pytest -v --cov=app --cov-report=term-missing
```

**Check the test results carefully:**
- Look for any FAILED tests
- Look for any ERROR tests
- Check for database connection issues
- Check for import errors or missing dependencies

**If you find ANY test failures:**
1. Identify which feature(s) are broken
2. Mark those features as `"passes": false` in feature_list.json
3. Add issues to a list
4. Fix ALL failures BEFORE moving to new features
5. This includes:
   - API endpoint errors (500s, unexpected 400s)
   - Database constraint violations
   - Validation errors
   - Business logic bugs
   - Import errors or missing modules

**Run specific endpoint tests:**
```bash
# Test a specific endpoint file
pytest tests/api/v1/test_users.py -v

# Test a specific test function
pytest tests/api/v1/test_users.py::test_create_user -v

# Run tests matching a pattern
pytest -k "user" -v
```

### STEP 4: CHOOSE ONE FEATURE TO IMPLEMENT

Look at feature_list.json and find the highest-priority feature with "passes": false.

Focus on completing ONE endpoint perfectly with ALL its test cases before moving on.
It's ok if you only complete one endpoint in this session - there will be more sessions.

**Example:** If feature #5 is "POST /api/v1/users" with 5 test cases, implement:
1. The database model (if not exists)
2. The Pydantic schemas (request + response)
3. The service layer business logic
4. The API router endpoint
5. ALL 5 pytest test cases
6. Run tests and verify they pass
7. Mark feature #5 as "passes": true

### STEP 5: IMPLEMENT THE FEATURE

Follow this implementation pattern for each endpoint:

**1. Database Model (if needed)**
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    # ... other fields
```

**2. Pydantic Schemas**
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
```

**3. Service Layer**
```python
# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    # Business logic here
    # Validation, password hashing, etc.
    pass
```

**4. API Router**
```python
# app/routers/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.dependencies.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Call service layer
    pass
```

**5. Database Migration**
```bash
# Create migration for new models
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head
```

### STEP 6: WRITE PYTEST TESTS

**CRITICAL:** Write comprehensive tests for the endpoint using pytest + TestClient.

Create or update test file:
```python
# tests/api/v1/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_valid(client: AsyncClient):
    """Test creating user with valid data."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "password": "SecurePass123",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "password" not in data  # Password should not be returned

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    """Test rejecting duplicate email address."""
    # Create first user
    await client.post(
        "/api/v1/users",
        json={
            "email": "existing@example.com",
            "password": "SecurePass123",
            "name": "First User"
        }
    )

    # Try to create second user with same email
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "existing@example.com",
            "password": "SecurePass123",
            "name": "Second User"
        }
    )
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient):
    """Test rejecting invalid email format."""
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "not-an-email",
            "password": "SecurePass123",
            "name": "Test User"
        }
    )
    assert response.status_code == 422  # Validation error
```

Write tests for ALL test cases defined in feature_list.json for this endpoint.

### STEP 7: RUN TESTS AND VERIFY

Run the tests you just wrote:

```bash
# Run specific test file
pytest tests/api/v1/test_users.py -v

# Run with detailed output
pytest tests/api/v1/test_users.py -v -s

# Run with coverage
pytest tests/api/v1/test_users.py -v --cov=app.routers.v1.users --cov-report=term-missing
```

**Verification criteria:**
- ✅ All new tests pass (green)
- ✅ No existing tests broken (regression check: `pytest -v`)
- ✅ Coverage for new code > 80%
- ✅ No database errors or connection issues
- ✅ Response schemas match what's documented
- ✅ HTTP status codes are correct
- ✅ Error messages are clear and helpful

**DO:**
- Test through the actual FastAPI TestClient (simulates HTTP requests)
- Test both happy paths AND error cases
- Verify database state after operations
- Check that validation works correctly
- Test authentication/authorization (if applicable)
- Verify response schemas match expectations

**DON'T:**
- Skip error case testing
- Only test happy paths
- Mark tests passing without running them
- Ignore test failures
- Skip database cleanup between tests

### STEP 8: UPDATE feature_list.json (CAREFULLY!)

**YOU CAN ONLY MODIFY ONE FIELD: "passes"**

After ALL test cases for an endpoint pass, change:
```json
"passes": false
```
to:
```json
"passes": true
```

**ONLY mark as passing if:**
- All test_cases for that endpoint have passing pytest tests
- You ran pytest and confirmed all tests pass
- No regressions introduced (full test suite still passes)

**NEVER:**
- Remove tests from feature_list.json
- Edit test_cases array
- Modify request_schema or response_schema
- Combine or consolidate features
- Reorder features
- Mark as passing without running tests

**ONLY CHANGE "passes" FIELD AFTER VERIFICATION WITH PYTEST.**

### STEP 9: COMMIT YOUR PROGRESS

Make a descriptive git commit:

```bash
git add .
git commit -m "Implement POST /api/v1/users endpoint

- Added User model with email uniqueness constraint
- Created UserCreate and UserResponse schemas
- Implemented user_service.create_user with validation
- Added /api/v1/users POST endpoint
- Wrote 5 pytest test cases covering:
  * Valid user creation
  * Duplicate email rejection
  * Invalid email format
  * Weak password rejection
  * Missing required fields
- All tests passing
- Updated feature_list.json: marked feature #5 as passing
- Test coverage: 95%
"
```

### STEP 10: UPDATE PROGRESS NOTES

Update `claude-progress.txt` with:
- What you accomplished this session
- Which endpoint(s) you completed
- How many test cases are now passing
- Any issues discovered or fixed
- What should be worked on next
- Current completion status (e.g., "5/150 endpoints complete, 25/200 tests passing")

Example:
```
Session 3 - 2024-01-15
========================

Completed:
- Implemented POST /api/v1/users endpoint (feature #5)
- All 5 test cases passing
- Added User model, schemas, service, and router
- Database migration created and applied

Test Status: 25/200 tests passing (12.5%)
Endpoints Complete: 5/150 (3.3%)

Issues Fixed:
- None

Next Steps:
- Implement GET /api/v1/users/{id} (feature #6)
- Implement GET /api/v1/users (list with pagination) (feature #7)
- Begin task resource endpoints (features #20-30)

Notes:
- Mock authentication working correctly
- PostgreSQL database healthy
- All dependencies installed
```

### STEP 11: END SESSION CLEANLY

Before context fills up:
1. Commit all working code
2. Update claude-progress.txt
3. Update feature_list.json (only "passes" field!)
4. Ensure no uncommitted changes: `git status`
5. Leave app in working state (all tests passing)
6. Stop background processes if any (`pkill uvicorn`)

---

## TESTING REQUIREMENTS

**ALL testing must use pytest with FastAPI TestClient.**

Test fixtures are defined in `tests/conftest.py`:
- `client` - AsyncClient for making HTTP requests to the API
- `db` - Test database session
- `test_user` - Mock authenticated user

Example test structure:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_endpoint_name(client: AsyncClient):
    """Test description."""
    response = await client.get("/api/v1/endpoint")
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```

**Common assertions:**
- `assert response.status_code == 200` (or 201, 404, 422, etc.)
- `assert "key" in response.json()`
- `assert response.json()["field"] == expected_value`
- `assert len(response.json()) == expected_count`

**Database testing:**
```python
@pytest.mark.asyncio
async def test_creates_database_record(client: AsyncClient, db: AsyncSession):
    """Test that endpoint creates record in database."""
    response = await client.post("/api/v1/users", json={...})
    assert response.status_code == 201

    # Verify database state
    result = await db.execute(select(User).where(User.email == "test@example.com"))
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.name == "Test User"
```

---

## IMPORTANT REMINDERS

**Your Goal:** Production-quality FastAPI backend with all 100-200 tests passing

**This Session's Goal:** Complete at least one endpoint perfectly with all its test cases

**Priority:** Fix broken tests before implementing new features

**Quality Bar:**
- Zero test failures
- Clean pytest output with all tests passing
- Proper error handling (400s, 404s, 422s, 500s)
- Database migrations applied correctly
- All features work end-to-end through HTTP API
- Fast, efficient, professional code
- Test coverage > 80%

**Implementation Pattern:**
1. Model → Schema → Service → Router → Tests
2. One endpoint at a time
3. All test cases for that endpoint
4. Verify with pytest
5. Mark as passing
6. Commit
7. Move to next endpoint

**You have unlimited time.** Take as long as needed to get it right. The most important thing is that you
leave the code base in a clean state before terminating the session (Step 11).

---

Begin by running Step 1 (Get Your Bearings).
