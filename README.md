# Autonomous Backend API Generator

A harness demonstrating long-running autonomous backend development with the Claude Agent SDK. This system implements a two-agent pattern (initializer + coding agent) that builds production-ready **FastAPI backends** with comprehensive **pytest** test coverage over multiple autonomous sessions.

## What It Generates

Complete FastAPI applications with:
- RESTful API endpoints with full CRUD operations
- PostgreSQL database (via Docker)
- Async SQLAlchemy ORM models
- Pydantic request/response schemas
- Comprehensive pytest test suites (>80% coverage)
- Database migrations (Alembic)
- Auto-generated OpenAPI documentation
- Mock authentication (swappable for JWT)
- **Frontend handoff documentation** (APP_OVERVIEW.md, FRONTEND_HANDOFF.md)
- **Realistic mock data files** (JSON) perfectly aligned with backend schemas
- **OpenAPI specification export** (openapi.json)

**Perfect for:** Generating backends to hand off to Figma Make or similar frontend tools.

## Frontend Handoff Package

The generated backend includes comprehensive handoff documentation perfect for Figma Make or other frontend tools:

### 📋 APP_OVERVIEW.md
Business context, user workflows, and suggested screen structure. Helps UI designers understand what they're building and why.

**Contains:**
- Application purpose and goals
- User roles and permissions
- Step-by-step user workflows (5-10 key journeys)
- Suggested screens organized by role
- Navigation structure
- Feature priorities (MVP vs nice-to-have)
- Design considerations

### 🔌 FRONTEND_HANDOFF.md
Technical integration guide with quick start instructions, data models (TypeScript interfaces), endpoint summaries, and code examples.

**Contains:**
- Quick start guide (how to run the backend)
- Authentication setup (current mock auth + future JWT)
- Data models as TypeScript interfaces
- API endpoint summaries by resource
- Common patterns (pagination, errors, timestamps)
- Integration code examples
- Testing instructions (Swagger UI, cURL)

### 🎨 Mock Data Files
Realistic JSON data files (`docs/mock-data/`) that perfectly mirror the backend schemas:
- Ready to import in frontend code
- Includes relationships between entities (foreign keys reference existing records)
- Contains realistic data patterns using Faker library (not "test1", "test2")
- Easy to swap for real API calls later (simple toggle)

**Files generated:**
- `users.json` - 15-20 sample users with various roles
- `tasks.json` - 40-50 sample tasks with assignments, statuses, priorities
- `tags.json` - 8-10 sample tags with colors
- `comments.json` - 25-30 sample comments
- `README.md` - Complete usage guide with code examples

### 📖 OpenAPI Specification
Machine-readable `openapi.json` file with complete API documentation, exportable to Postman or other API tools.

---

**Why This Matters:**
- Frontend development can start immediately using mock data (no backend dependency)
- Mock data perfectly matches API response schemas
- Clear documentation of user workflows guides UI design decisions
- Easy integration phase with comprehensive technical docs

**Location:** All handoff files are in the generated project's `docs/` directory and root.

## Prerequisites

**Required:** Install the latest versions of both Claude Code and the Claude Agent SDK:

```bash
# Install Claude Code CLI (latest version required)
npm install -g @anthropic-ai/claude-code

# Install Python dependencies
pip install -r requirements.txt
```

Verify your installations:
```bash
claude --version  # Should be latest version
pip show claude-code-sdk  # Check SDK is installed
```

**API Key:** Create a `.env` file with your Anthropic API key:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key:
# ANTHROPIC_API_KEY=your-api-key-here
```

Alternatively, export it as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Quick Start

```bash
python autonomous_agent_demo.py --project-dir ./my_task_api
```

For testing with limited iterations:
```bash
python autonomous_agent_demo.py --project-dir ./my_task_api --max-iterations 3
```

### Development/Pipeline Testing

For rapid pipeline validation during development (minimal token usage):
```bash
python autonomous_agent_demo.py --project-dir ./test_run --config test --max-iterations 2
```

This uses a minimal Notes API spec with only 3-5 endpoints and 5-10 tests, completing in 1-3 minutes.

## Important Timing Expectations

> **Warning: This demo takes a long time to run!**

- **First session (initialization):** The agent generates a `feature_list.json` with 100-200 API test specifications. This takes several minutes and may appear to hang - this is normal. The agent is writing out all the endpoint specifications with test cases.

- **Subsequent sessions:** Each coding iteration can take **5-15 minutes** depending on complexity.

- **Full API:** Building all endpoints typically requires **many hours** of total runtime across multiple sessions.

**Tip:** The 100-200 test cases parameter in the prompts is designed for comprehensive coverage. If you want faster demos, you can modify `prompts/initializer_prompt.md` to reduce the test count (e.g., 20-50 test cases for a quicker demo).

## How It Works

### Two-Agent Pattern

1. **Initializer Agent (Session 1):**
   - Reads `app_spec.txt` backend specification
   - Creates `feature_list.json` with 100-200 API test specifications
   - Sets up FastAPI project structure (models, schemas, routers, services)
   - Configures PostgreSQL with Docker
   - Sets up Alembic migrations
   - Creates pytest test structure with fixtures
   - Initializes git repository

2. **Coding Agent (Sessions 2+):**
   - Fresh context window each session
   - Reads previous progress from git and `feature_list.json`
   - Implements API endpoints one by one
   - Follows pattern: Model → Schema → Service → Router → Tests
   - Uses pytest + TestClient for verification
   - Marks tests as passing in `feature_list.json`
   - Commits progress before session ends

### Session Management

- Each session runs with a fresh context window
- Progress persists via `feature_list.json`, git commits, and `claude-progress.txt`
- The agent auto-continues between sessions (3 second delay)
- Press `Ctrl+C` to pause; run the same command to resume

## Security Model

This harness uses a defense-in-depth security approach (see `security.py` and `client.py`):

1. **OS-level Sandbox:** Bash commands run in an isolated environment
2. **Filesystem Restrictions:** File operations restricted to the project directory only
3. **Bash Allowlist:** Only specific commands are permitted:
   - File inspection: `ls`, `cat`, `head`, `tail`, `wc`, `grep`
   - Python development: `python`, `python3`, `pip`, `pip3`
   - Testing: `pytest`, `coverage`
   - FastAPI server: `uvicorn`
   - Database tools: `alembic`, `docker` (includes `docker compose`)
   - Linting/formatting: `ruff`, `black`, `mypy`
   - Node.js (for tooling): `npm`, `node`
   - Version control: `git`
   - Process management: `ps`, `lsof`, `sleep`, `pkill` (dev processes only)

Commands not in the allowlist are blocked by the security hook.

## Project Structure

```
backend-harness/
├── autonomous_agent_demo.py  # Main entry point
├── agent.py                  # Agent session logic
├── client.py                 # Claude SDK client configuration
├── security.py               # Bash command allowlist and validation
├── progress.py               # Progress tracking utilities
├── prompts.py                # Prompt loading utilities
├── test_security.py          # Security hook tests
├── prompts/
│   ├── app_spec.txt          # Backend API specification
│   ├── initializer_prompt.md # First session prompt (FastAPI setup)
│   └── coding_prompt.md      # Continuation session prompt (pytest workflow)
└── requirements.txt          # Python dependencies
```

## Generated Project Structure

After running, your project directory will contain a production-ready FastAPI application:

```
my_task_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Async SQLAlchemy setup
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── [resource].py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── [resource].py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── [resource].py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── [resource]_service.py
│   └── dependencies/        # Dependency injection
│       ├── __init__.py
│       ├── auth.py          # Mock auth
│       └── database.py      # DB session
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (client, db, auth)
│   └── api/
│       └── v1/
│           └── test_[resource].py
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
├── docker-compose.yml       # PostgreSQL service (use with: docker compose)
├── alembic.ini
├── pyproject.toml           # Dependencies
├── .env.example             # Environment variables template
├── feature_list.json        # 100-200 test specifications (source of truth)
├── app_spec.txt             # Copied specification
├── init.sh                  # Environment setup script (Bash)
├── init.ps1                 # Environment setup script (PowerShell)
├── claude-progress.txt      # Session progress notes
├── .claude_settings.json    # Security settings
└── README.md
```

## Running the Generated Application

After the agent completes (or pauses), you can run the generated application in two steps:

### Step 1: Setup Environment

Run the init script to set up your development environment (creates virtual environment, installs dependencies, starts database, runs migrations):

**On Windows (PowerShell):**
```bash
cd generations/my_task_api
./init.ps1
```

**On Unix/Linux/macOS/Git Bash:**
```bash
cd generations/my_task_api
./init.sh
```

The init script will:
- Create a Python virtual environment (`.venv`)
- Install all dependencies from `requirements.txt`
- Start PostgreSQL database (if Docker is available)
- Run database migrations (if Alembic is configured)
- Run test suite to verify everything works

**Note:** For SQLite projects, Docker and Alembic steps are optional - the application will auto-create the database schema on first startup.

### Step 2: Start the Server

After running the init script, manually start the FastAPI development server:

```bash
# Activate virtual environment (if not already activated)
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# On Unix/Linux/macOS/Git Bash:
source .venv/bin/activate

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Important:** The init scripts only set up the environment - they do NOT start the server. You must manually run `uvicorn` as shown above to start the API.

### Alternative: Manual Setup

If you prefer not to use the init script:

```bash
cd generations/my_task_api

# 1. Start PostgreSQL (optional for SQLite projects)
docker compose up -d postgres

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run database migrations (optional for SQLite projects)
python -m alembic upgrade head

# 4. Start FastAPI server
uvicorn app.main:app --reload --port 8000

# 5. Run tests (optional)
pytest -v
pytest --cov=app --cov-report=term-missing
```

### Accessing the API

Once the server is running, the API will be available at:
- **API Base**: http://localhost:8000
- **Swagger UI** (interactive docs): http://localhost:8000/docs
- **ReDoc** (alternative docs): http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project-dir` | Directory for the project | `./autonomous_demo_project` |
| `--max-iterations` | Max agent iterations | Unlimited |
| `--model` | Claude model to use | `claude-sonnet-4-5-20250929` |

## Customization

### Changing the API Specification

Edit `prompts/app_spec.txt` to specify a different backend API to build. The current example is a Task Management API with Users, Tasks, Tags, and Comments.

### Adjusting Test Count

Edit `prompts/initializer_prompt.md` and change the "100-200 test cases" requirement to a smaller number for faster demos (e.g., 20-50 test cases).

### Modifying Allowed Commands

Edit `security.py` to add or remove commands from `ALLOWED_COMMANDS`. Run `python test_security.py` to validate changes.

## Testing the Security Hooks

Run the comprehensive security test suite:

```bash
python test_security.py
```

All 116 tests should pass, including tests for Python, Docker, pytest, and other backend development commands.

## Example Use Cases

This harness can generate backends for:
- Task management systems
- E-commerce APIs
- Blog/CMS backends
- User management systems
- Inventory tracking APIs
- Booking/reservation systems
- Any RESTful API with CRUD operations

## Troubleshooting

**"Appears to hang on first run"**
This is normal. The initializer agent is generating 100-200 detailed API test specifications, which takes significant time. Watch for `[Tool: ...]` output to confirm the agent is working.

**"Command blocked by security hook"**
The agent tried to run a command not in the allowlist. This is the security system working as intended. If needed, add the command to `ALLOWED_COMMANDS` in `security.py` and run `python test_security.py` to validate.

**"API key not set"**
Create a `.env` file with `ANTHROPIC_API_KEY=your-key` or export it in your shell.

**"pytest not found"**
The generated project's dependencies need to be installed. Run `pip install -r requirements.txt` in the project directory.

**"PostgreSQL connection failed"**
Ensure Docker is running and PostgreSQL is started: `docker compose up -d postgres`

**"Can't access http://localhost:8000/docs after running init script"**
The init scripts only set up the environment - they don't start the server. After running `init.sh` or `init.ps1`, you must manually start the server with: `uvicorn app.main:app --reload --port 8000`

## Technology Stack (Generated Projects)

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ (via Docker)
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Authentication**: Mock (swappable for JWT)
- **Testing**: pytest + pytest-asyncio + httpx
- **Validation**: Pydantic v2
- **Documentation**: Auto-generated OpenAPI
