<div align="center">

# Autonomous Backend API Generator

**Production-ready FastAPI backends built by AI agents**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Claude Agent SDK](https://img.shields.io/badge/Claude-Agent%20SDK-orange.svg)](https://github.com/anthropics/anthropic-sdk-python)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*An autonomous coding harness that generates complete FastAPI backends with PostgreSQL, comprehensive tests, database migrations, **and complete Figma Make integration**—all from a simple specification.*

[Quick Start](#-quick-start) • [Features](#-what-you-get) • [How It Works](#-how-it-works) • [Figma Make](#-figma-make-integration) • [Logging](#-debugging--logging)

</div>

---

## What You Get

<table>
<tr>
<td width="33%" valign="top">

### **Backend Core**
- RESTful API with full CRUD
- PostgreSQL + Docker setup
- Async SQLAlchemy ORM
- Pydantic schemas (v2)
- Alembic migrations
- Auto-generated OpenAPI docs
- Mock auth (JWT-ready)

</td>
<td width="33%" valign="top">

### **Quality & Testing**
- Comprehensive pytest suite (>80% coverage)
- TestClient-based API tests
- Auto-verification of endpoints
- Test-driven development
- Database fixtures
- Coverage reporting
- CI/CD ready

</td>
<td width="33%" valign="top">

### **Frontend Handoff**
- **Lean, non-redundant handoff package**
- Business context (app_spec.txt)
- Simple integration guide (QUICKSTART.md)
- Realistic mock data (JSON)
- Production-grade OpenAPI spec
- TypeScript type generation ready
- Complete Figma Make integration

</td>
</tr>
</table>

### **Developer Experience**

- **Live Dashboard**: Real-time visualization with progress bars, token tracking, and file activity
- **OpenAPI Excellence**: Enforces 8 best practices (security schemes, servers, error handling, pagination)
- **Lean Frontend Handoff**: app_spec.txt + openapi.json + mock data (no duplication)
- **Multi-API Support**: Works with Anthropic API or Azure Foundry
- **Comprehensive Logging**: Detailed session logs with powerful analysis tools
- **Configurable Sizes**: Test (5-10 tests), Small (20-30), Medium (100-200), Large (300-500)
- **Auto-completion**: Stops automatically when all tests pass
- **Rich Console**: Beautiful terminal output with animations and real-time updates
- **OpenAPI Validator**: Automated spec validation with 8 quality checks

> **Perfect for:** Building production backends with enterprise-grade OpenAPI specs and handing them off to Figma Make, v0, Cursor, or any frontend tool. Frontend teams get app_spec.txt (business context), openapi.json (complete API docs), and realistic mock data—everything they need with zero redundancy.

---

## Quick Start

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API access (choose ONE option)

# Option 1: Direct Anthropic API (Recommended)
export ANTHROPIC_API_KEY='your-key-here'
# or create .env file with: ANTHROPIC_API_KEY=your-key-here

# Option 2: Azure Foundry
export AZURE_FOUNDRY_API_KEY='your-azure-key'
export AZURE_FOUNDRY_BASE_URL='https://your-endpoint.inference.ai.azure.com'
export AZURE_FOUNDRY_MODEL_NAME='claude-sonnet-4-5'  # optional
# or add to .env file
```

### Generate Your API

```bash
# Production-ready API (100-200 tests, 2-4 hours)
python autonomous_agent_demo.py --project-dir ./my_api

# Quick test (5-10 tests, 3-5 minutes, perfect for CI/CD validation)
python autonomous_agent_demo.py --project-dir ./test_run --config test --max-iterations 2

# Small project (20-30 tests, 30-60 minutes)
python autonomous_agent_demo.py --project-dir ./small_api --config small

# Large enterprise project (300-500 tests, 6-12+ hours)
python autonomous_agent_demo.py --project-dir ./enterprise_api --config large
```

### Configuration Options

```bash
python autonomous_agent_demo.py \
  --project-dir ./my_api \              # Output directory
  --config medium \                     # Size: test|small|medium|large
  --max-iterations 10 \                 # Limit iterations (optional)
  --model claude-sonnet-4-5-20250929 \  # Claude model (optional)
  --verbose \                           # Show detailed output
  --quiet \                             # Minimal output
  --no-git                              # Skip git commits
```

### Run the Generated API

```bash
cd my_api

# Setup (creates venv, installs deps, starts DB, runs migrations)
./init.sh          # Unix/Linux/macOS/Git Bash
./init.ps1         # Windows PowerShell

# Start server
source .venv/bin/activate    # or .\.venv\Scripts\Activate.ps1 on Windows
uvicorn app.main:app --reload --port 8000
```

**Done!** Visit http://localhost:8000/docs for interactive API documentation.

---

## How It Works

### Two-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Session 1: Initializer Agent                                   │
├─────────────────────────────────────────────────────────────────┤
│  • Reads your app_spec.txt                                       │
│  • Generates test specifications (5-500 based on config)         │
│  • Creates FastAPI project structure                             │
│  • Sets up PostgreSQL + Docker + Alembic                         │
│  • Generates lean frontend handoff (app_spec + mock data)        │
│  • Creates QUICKSTART.md integration guide                       │
│  • Enforces OpenAPI best practices (8 standards)                 │
│  • Initializes git repository with .gitignore                    │
│  • Outputs: feature_list.json (source of truth)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Sessions 2+: Coding Agent (autonomous iterations)              │
├─────────────────────────────────────────────────────────────────┤
│  • Fresh context each session                                    │
│  • Implements endpoints: Model → Schema → Service → Router       │
│  • Writes & runs pytest tests with TestClient                    │
│  • Updates feature_list.json on test pass                        │
│  • Commits progress to git with descriptive messages             │
│  • Auto-continues after 3 seconds (Ctrl+C to pause)              │
│  • Auto-stops when all tests pass (100% completion)              │
└─────────────────────────────────────────────────────────────────┘
```

### Live Dashboard **NEW**

Watch your API being built in real-time with:

- **Progress bar** showing test completion percentage
- **Current activity** (currently editing `app/models/user.py`)
- **Agent reasoning** (live thoughts and planning)
- **Token usage** (real-time input/output tracking per message)
- **Session stats** (duration, iteration count, total tokens)
- **File visibility** (see exactly which files are being modified)

The live dashboard updates in real-time with smooth animations and provides complete visibility into the agent's work.

<details>
<summary><b>Timing Expectations</b> (click to expand)</summary>

| Config | Tests | First Session | Total Duration | Use Case |
|--------|-------|--------------|----------------|----------|
| **test** | 5-10 | 1-2 min | 3-5 min | CI/CD validation, quick demos |
| **small** | 20-30 | 2-4 min | 30-60 min | Prototypes, MVPs |
| **medium** | 100-200 | 5-10 min | 2-4 hours | Production apps |
| **large** | 300-500 | 15-30 min | 6-12+ hours | Enterprise systems |

**Tips:**
- First session generates all test specs (watch the live dashboard for progress)
- Use `--config test` for rapid iteration during development
- Sessions auto-continue every 3 seconds (pause anytime with Ctrl+C)
- Resume by running the same command—progress persists via git + feature_list.json

</details>

---

## Lean Frontend Handoff & Figma Make Integration

**The agents automatically generate a lean, non-redundant handoff package** optimized for frontend development. No duplication, no sync issues—just the essentials.

### What's Auto-Generated

Every file below is **automatically created by the agents** in your generated project:

| File (in my_api/) | Purpose | Source |
|-------------------|---------|--------|
| **docs/app_spec.txt** | Business requirements, workflows, feature priorities | Copied from prompts/ (your original spec) |
| **docs/QUICKSTART.md** | Simple 1-page integration guide | Generated using template |
| **docs/mock-data/*.json** | Realistic sample data matching API schemas exactly | Generated with Faker |
| **openapi.json** | Complete API specification with best practices | Auto-generated by FastAPI |

### Why This Approach is Better

**Old approach (redundant):**
- ❌ APP_OVERVIEW.md reformatted app_spec.txt
- ❌ FRONTEND_HANDOFF.md reformatted openapi.json
- ❌ Duplication led to sync issues
- ❌ More files to read and maintain

**New approach (lean):**
- ✅ Use app_spec.txt directly (business context already there)
- ✅ Use openapi.json directly (auto-generated, always accurate)
- ✅ QUICKSTART.md ties it together (1-page guide)
- ✅ No duplication, no sync issues, less to read

### Complete Workflow

**Phase 1: Run Command (Agents Do Everything)**

```bash
# 1. Edit your API specification first
vim prompts/app_spec.txt

# 2. Run the autonomous agent
python autonomous_agent_demo.py --project-dir ./my_api

# 3. Wait for agents to complete (3min - 12hrs depending on size)
# Watch the live dashboard for progress
```

**The agents automatically:**
- Generate entire FastAPI backend with comprehensive tests
- Create lean handoff package (app_spec.txt + QUICKSTART.md + mock data + openapi.json)
- Enforce OpenAPI best practices (8 standards for production-quality specs)
- Generate realistic mock data matching your schemas exactly

**Phase 2: Frontend Development (After Agents Finish)**

```bash
# 1. Understand the business requirements
cat my_api/docs/app_spec.txt  # Business context, workflows, feature priorities

# 2. Explore the API
# Option A: Interactive docs
cd my_api && ./init.sh && uvicorn app.main:app --reload
# Visit http://localhost:8000/docs

# Option B: Generate TypeScript types
npx openapi-typescript my_api/openapi.json -o types.ts

# 3. Build UI with mock data (no backend needed)
import users from './my_api/docs/mock-data/users.json';
import tasks from './my_api/docs/mock-data/tasks.json';

# 4. Read integration guide
cat my_api/docs/QUICKSTART.md  # 5-minute read with all patterns
```

**Phase 3: API Integration (When Ready)**

```typescript
// Before (mock data)
import tasks from './docs/mock-data/tasks.json';

// After (real API)
const response = await fetch('http://localhost:8000/api/v1/tasks');
const data = await response.json();
const tasks = data.items;  // Paginated response
```

### Key Features

**Lean & Non-Redundant**: No reformatted docs. Use app_spec.txt (your original spec) and openapi.json (auto-generated) directly.

**OpenAPI Excellence**: Generated specs follow 8 best practices:
1. ✅ Security schemes (HTTPBearer)
2. ✅ Servers configuration
3. ✅ Standardized error responses
4. ✅ Human-readable operation IDs
5. ✅ Consistent pagination (limit/offset)
6. ✅ No empty response schemas
7. ✅ Privacy & security schemas
8. ✅ Path naming conventions

**TypeScript-Ready**: Generate types with `npx openapi-typescript openapi.json -o types.ts`

**Localhost Constraint Solved**: Mock data development patterns in QUICKSTART.md (Figma Make can't access localhost)

**Auto-Validation**: Run `python openapi_validator.py my_api/` to verify generated spec quality

---

## OpenAPI Validator

Validate generated OpenAPI specifications against production best practices:

```bash
# Validate a generated project
python openapi_validator.py ./my_api

# Validate specific openapi.json
python openapi_validator.py ./my_api/openapi.json

# Verbose output (show passed checks)
python openapi_validator.py ./my_api --verbose
```

**8 Validation Checks:**

1. ✅ **Security Schemes** - HTTPBearer authentication properly defined
2. ✅ **Servers Configuration** - Multiple environment URLs (dev/staging/prod)
3. ✅ **Response Schemas** - No empty schemas `{}`
4. ✅ **Error Response Consistency** - ErrorResponse schema with code/message/details
5. ✅ **Path Conventions** - No trailing slashes
6. ✅ **Operation IDs** - Human-readable (not auto-generated)
7. ✅ **Pagination Pattern** - PaginatedResponse with limit/offset/total/count
8. ✅ **Error Coverage** - Common errors documented (401/403/404/409/422)

**Output Example:**

```
OpenAPI Validation Results
======================================================================

Total checks: 8
  ✓ Passed:   7
  ⚠ Warnings: 1
  ✗ Errors:   0

⚠️  WARNINGS
----------------------------------------------------------------------

  Operation IDs: 2 endpoint(s) missing human-readable operationId
    GET /api/v1/health (auto-generated: health_check_api_v1_health_get)
    POST /api/v1/users

✓ Validation passed with warnings
======================================================================
```

**Exit Codes:**
- `0` - All checks passed
- `1` - Validation errors found
- `2` - File not found or invalid JSON

**When to Use:**
- After initial generation (quality gate)
- Before deploying to production
- In CI/CD pipelines for automated checks
- When debugging OpenAPI import issues

---

## Debugging & Logging

### Comprehensive Session Logs

Every run automatically creates detailed logs for debugging and optimization analysis:

```bash
project_dir/
  logs/
    run_20231219_103045/        # Timestamped run directory
      session_001.json          # Full session trace
      session_002.json
      session_003.json
      timeline.jsonl            # Streaming event log
      run_summary.json          # Aggregated statistics
```

**What's logged:**
- Every tool call with input/output and precise timing
- Agent reasoning and decision-making thoughts
- Token usage (per-message and cumulative)
- All errors with full context
- Security blocks with detailed reasons
- Progress checkpoints
- **Automatic sensitive data filtering** (API keys, credentials)

### Analyzing Sessions with `analyze_logs.py`

If a session takes unexpectedly long or you want to optimize performance:

```bash
# Analyze specific session for bottlenecks
python analyze_logs.py project/logs/run_20231219_103045/session_003.json

# Compare all sessions in a run
python analyze_logs.py project/logs/run_20231219_103045 --compare

# View detailed event timeline
python analyze_logs.py project/logs/run_20231219_103045/session_003.json --timeline
```

**The analyzer identifies:**
- **Slowest tool calls** (pinpoints bottlenecks)
- **Repeated operations** (detects stuck loops, e.g., same file edited 20+ times)
- **Anomalies** (long gaps, high error rates, excessive security blocks)
- **Token usage breakdown** (by tool, by phase)
- **Most used tools** (understand agent behavior)
- **All errors** with context

**Example output:**
```
⏱️  Slowest Tool Calls
┌──────────┬──────────┬────────────────────────┐
│ Tool     │ Duration │ Input Preview          │
├──────────┼──────────┼────────────────────────┤
│ Bash     │ 45.2m    │ pytest tests/          │
│ Read     │ 12.1m    │ app/models/user.py     │
│ Edit     │ 8.5m     │ app/routers/v1/tasks.py│
└──────────┴──────────┴────────────────────────┘

🚨 Potential Issues
  • File 'task_service.py' modified 23 times (possible stuck loop)
  • Tool 'Bash' failed 5 times (investigate command issues)
  • Gap of 15.2 minutes after 'pytest' command (slow test execution)
```

This analysis is invaluable for:
- Debugging sessions that take 380+ minutes
- Optimizing your `app_spec.txt` for faster generation
- Understanding agent decision patterns
- Identifying infrastructure bottlenecks (e.g., slow Docker startup)

See **[LOGGING.md](LOGGING.md)** for complete documentation.

---

## Security Model

Defense-in-depth approach with three layers of protection:

1. **Sandbox**: OS-level isolation for bash commands (prevents filesystem escape)
2. **Filesystem Guard**: File operations restricted to project directory only
3. **Command Allowlist**: Only pre-approved commands can execute (validated by 116 test cases)

<details>
<summary><b>Allowed Commands</b> (click to expand)</summary>

- **File Operations**: `ls`, `cat`, `head`, `tail`, `wc`, `grep`, `cp`, `mkdir`
- **Python Development**: `python`, `python3`, `pip`, `pytest`, `coverage`
- **FastAPI Server**: `uvicorn`
- **Database**: `alembic`, `docker`, `docker-compose` (compose v2)
- **Code Quality**: `ruff`, `black`, `mypy`
- **Version Control**: `git`
- **Process Management**: `ps`, `lsof`, `sleep`, `pkill` (dev processes only)
- **Init Scripts**: `chmod +x`, `./init.sh`, `./init.ps1`

**Modify:** Edit `ALLOWED_COMMANDS` in `security.py`
**Validate:** Run `python test/test_security.py` (116 tests should pass)

</details>

Commands blocked by the security hook are logged with detailed explanations. If you need to add a command:
1. Review its safety implications
2. Add to `ALLOWED_COMMANDS` in `security.py`
3. If it needs validation (like `pkill`, `chmod`), add to `COMMANDS_NEEDING_EXTRA_VALIDATION`
4. Run `python test/test_security.py` to verify

---

## Project Structure

<details>
<summary><b>Generated FastAPI Project</b> (click to expand)</summary>

```
my_api/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Async SQLAlchemy
│   ├── models/              # ORM models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/v1/          # API endpoints
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── tasks.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── task_service.py
│   └── dependencies/        # DI (auth, DB session)
│       ├── __init__.py
│       ├── auth.py
│       └── database.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (client, db, auth)
│   └── api/v1/
│       ├── test_users.py
│       └── test_tasks.py
├── alembic/                 # DB migrations
│   ├── env.py
│   └── versions/
├── docs/                    # Lean frontend handoff ⭐ Updated
│   ├── app_spec.txt         # Business requirements (copied from prompts/)
│   ├── QUICKSTART.md        # 1-page integration guide
│   └── mock-data/
│       ├── README.md
│       ├── users.json       # 15-20 sample users
│       ├── tasks.json       # 40-50 sample tasks
│       ├── tags.json        # 8-10 sample tags
│       └── comments.json    # 25-30 sample comments
├── guidelines/              # Figma Make integration
│   └── guideline.md         # Universal coding standards
├── scripts/
│   └── generate_mock_data.py
├── logs/                    # ⭐ Enhanced - Session logs (auto-generated)
│   └── run_TIMESTAMP/
│       ├── session_001.json # Full trace with timing
│       ├── session_002.json
│       ├── timeline.jsonl   # Streaming events
│       └── run_summary.json # Aggregated stats
├── docker-compose.yml       # PostgreSQL service
├── alembic.ini
├── pyproject.toml           # Dependencies
├── .env.example             # Environment template
├── .gitignore
├── feature_list.json        # Test specifications (source of truth)
├── app_spec.txt             # Original specification (user-provided)
├── init.sh / init.ps1       # Cross-platform setup scripts
├── openapi.json             # ⭐ Production-grade API spec (8 best practices)
└── README.md
```

</details>

<details>
<summary><b>Harness Structure</b> (click to expand)</summary>

```
backend-harness/
├── autonomous_agent_demo.py # Main entry point
├── agent.py                 # Session orchestration
├── client.py                # Claude SDK configuration (multi-API support)
├── security.py              # Bash command validation
├── logger.py                # Comprehensive logging system
├── analyze_logs.py          # Log analysis tool
├── openapi_validator.py     # ⭐ NEW - OpenAPI spec validator (8 checks)
├── prompts.py               # Prompt loading utilities
├── progress.py              # Progress tracking
├── console_output.py        # Rich terminal UI (live dashboard!)
├── prompts/
│   ├── app_spec.txt         # API specification (edit this!)
│   ├── app_spec_test.txt    # Minimal spec for testing
│   ├── initializer_prompt.md # ⭐ Updated - Lean handoff + OpenAPI best practices
│   ├── coding_prompt.md      # ⭐ Updated - Enhanced with OpenAPI examples
│   └── templates/            # Frontend handoff templates
│       ├── QUICKSTART_TEMPLATE.md        # ⭐ Lean integration guide
│       └── MOCK_DATA_README_TEMPLATE.md  # Mock data documentation
├── configs/                 # Size configurations
│   ├── test.json            # 5-10 tests
│   ├── small.json           # 20-30 tests
│   ├── medium.json          # 100-200 tests
│   └── large.json           # 300-500 tests
├── test/                    # Test suite
│   ├── test_security.py     # Security validation (116 tests)
│   ├── test_foundry_connection.py  # ⭐ NEW - Azure Foundry tests
│   ├── test_live_dashboard_tokens.py  # ⭐ NEW
│   └── ...
├── example_specs/           # Example specifications
├── CLAUDE.md                # Project documentation (for Claude Code)
├── LOGGING.md               # Logging system guide
├── QUICK_START.md           # Quick start guide
├── README.md                # This file
└── requirements.txt
```

</details>

---

## Use Cases

This harness can generate production-ready backends for:

- **Task/Project Management** (Users, Tasks, Projects, Comments)
- **E-commerce & Inventory** (Products, Orders, Cart, Payments, Reviews)
- **Blog/CMS Platforms** (Posts, Authors, Categories, Tags, Media)
- **User Management Systems** (Auth, Roles, Permissions, Profiles)
- **Booking/Reservation** (Appointments, Resources, Calendar, Availability)
- **Authentication Services** (OAuth, JWT, SSO, 2FA)
- **Analytics Dashboards** (Metrics, Reports, Visualizations, Exports)
- **Healthcare Systems** (Patients, Appointments, Records, Prescriptions)
- **Education Platforms** (Courses, Students, Assignments, Grades)
- **Social Networks** (Posts, Friends, Messages, Feeds)
- **Financial Systems** (Transactions, Accounts, Budgets, Reports)
- ...any RESTful API with CRUD operations

**Customize:** Edit `prompts/app_spec.txt` with your specific requirements.

---

## Advanced Configuration

### Project Size Configurations

| Config | Tests | Endpoints | Mock Data | Duration | Best For |
|--------|-------|-----------|-----------|----------|----------|
| **test** | 5-10 | 2-3 | Minimal | 3-5 min | CI/CD, demos, rapid validation |
| **small** | 20-30 | 4-6 | Light | 30-60 min | MVPs, prototypes, quick testing |
| **medium** | 100-200 | 15-25 | Realistic | 2-4 hrs | Production apps, standard projects |
| **large** | 300-500 | 40-60 | Comprehensive | 6-12+ hrs | Enterprise systems, complex domains |

Edit configs in `configs/*.json` to customize test counts, endpoint counts, and mock data quantities.

### API Provider Configuration

**Anthropic API (Default)**
```bash
# .env file
ANTHROPIC_API_KEY=your-key-here

# Optional: specify model
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

**Azure Foundry**
```bash
# .env file
AZURE_FOUNDRY_API_KEY=your-azure-key
AZURE_FOUNDRY_BASE_URL=https://your-endpoint.inference.ai.azure.com
AZURE_FOUNDRY_MODEL_NAME=claude-sonnet-4-5  # optional

# Test connection
python test/test_foundry_connection.py
```

The system auto-detects which API to use based on environment variables. Azure Foundry support includes full token tracking and logging.

### Custom API Specification

<details>
<summary><b>Modify API Specification</b></summary>

Edit `prompts/app_spec.txt` with your backend requirements:

```
Task Management API

Core Features:
- User authentication (mock, JWT-ready)
- CRUD operations for Tasks
- Task assignment to users
- Task status tracking (todo, in_progress, done)
- Comments on tasks
- Tags/labels for organization

Database Models:
- User (id, email, name, created_at)
- Task (id, title, description, status, user_id, created_at)
- Comment (id, content, task_id, user_id, created_at)
- Tag (id, name, color)

API Endpoints:
- POST /api/v1/users - Create user
- GET /api/v1/users/{id} - Get user
- POST /api/v1/tasks - Create task
- GET /api/v1/tasks - List tasks (with filters)
- PUT /api/v1/tasks/{id} - Update task
- DELETE /api/v1/tasks/{id} - Delete task
...
```

Current example: **Task Management API** (Users, Tasks, Tags, Comments)

See `example_specs/` for more examples.

</details>

### Modify Security Allowlist

<details>
<summary><b>Add Allowed Commands</b></summary>

1. Edit `ALLOWED_COMMANDS` in `security.py`:
```python
ALLOWED_COMMANDS = {
    # Add your command
    "mycmd",
    ...
}
```

2. For commands needing validation (like `chmod`, `pkill`):
```python
COMMANDS_NEEDING_EXTRA_VALIDATION = {"mycmd"}

def validate_mycmd_command(command_string: str) -> tuple[bool, str]:
    # Implement validation logic
    if not is_safe(command_string):
        return False, "Reason why it's not safe"
    return True, ""
```

3. Validate changes:
```bash
python test/test_security.py  # All 116 tests should pass
```

</details>

---

## Troubleshooting

<details>
<summary><b>"Appears to hang on first run"</b></summary>

**Normal behavior.** The initializer is generating test specifications. Watch the live dashboard for activity:
- Progress bar shows "Initializing project structure..."
- Tool calls visible (e.g., `Writing feature_list.json`)
- File activity updates in real-time

First session takes 1-10 minutes depending on config size (test: 1-2min, medium: 5-10min, large: 15-30min).

</details>

<details>
<summary><b>"Session took 380 minutes—why?"</b></summary>

Use the log analyzer to identify bottlenecks:
```bash
python analyze_logs.py project/logs/run_XXXXX/session_NNN.json
```

**Common causes:**
- Long-running pytest execution (many tests)
- Slow database migrations
- Agent stuck in error loop (same file edited 20+ times)
- Large file reads/writes
- Docker startup delays

The analyzer shows:
- Slowest tool calls (e.g., "pytest took 45 minutes")
- Repeated operations (e.g., "task_service.py edited 23 times")
- Long gaps (e.g., "15 minute gap after pytest command")
- Error patterns (e.g., "5 bash failures")

See **[LOGGING.md](LOGGING.md)** for optimization strategies.

</details>

<details>
<summary><b>"Command blocked by security hook"</b></summary>

**Security working as intended.** The agent attempted a command not in the allowlist.

**To permit it:**
1. Review in logs: `project/logs/run_XXXXX/session_NNN.json`
2. Assess safety implications
3. If safe, add to `ALLOWED_COMMANDS` in `security.py`
4. Run `python test/test_security.py` to validate
5. Restart agent—it will retry the command

</details>

<details>
<summary><b>"Can't access http://localhost:8000/docs"</b></summary>

Init scripts don't start the server (they only set up the environment). Manually start:

```bash
cd my_api
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Then visit http://localhost:8000/docs

</details>

<details>
<summary><b>"PostgreSQL connection failed"</b></summary>

Ensure Docker is running:
```bash
# Check Docker status
docker ps

# Start PostgreSQL
cd my_api
docker compose up -d postgres

# Verify running
docker compose ps

# Check logs if still failing
docker compose logs postgres
```

</details>

<details>
<summary><b>"API key not set"</b></summary>

**Option 1 - Anthropic API:**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Or export
export ANTHROPIC_API_KEY='your-key-here'
```

**Option 2 - Azure Foundry:**
```bash
# Create .env file with all required variables
cat > .env << EOF
AZURE_FOUNDRY_API_KEY=your-azure-key
AZURE_FOUNDRY_BASE_URL=https://your-endpoint.inference.ai.azure.com
AZURE_FOUNDRY_MODEL_NAME=claude-sonnet-4-5
EOF

# Test connection
python test/test_foundry_connection.py
```

</details>

<details>
<summary><b>"How do I pause and resume?"</b></summary>

**Pause:** Press `Ctrl+C` during execution (safe, won't corrupt state)

**Resume:** Run the exact same command:
```bash
python autonomous_agent_demo.py --project-dir ./my_api
```

Progress persists via:
- `feature_list.json` (tracks test completion)
- Git commits (all code changes)
- `logs/` directory (complete session history)
- `claude-progress.txt` (session notes)

The agent picks up exactly where it left off.

</details>

<details>
<summary><b>"Tests are failing but agent continues?"</b></summary>

**Normal iterative behavior.** The agent follows a TDD approach:
1. Write test
2. Run test
3. If fails → analyze error → fix code → rerun
4. Repeat until passing
5. Mark as passing in `feature_list.json` only when verified

Monitor progress:
```bash
# Compare all sessions to see improvement
python analyze_logs.py project/logs/run_XXXXX --compare

# View feature_list.json to see which tests pass
cat my_api/feature_list.json | grep '"passes": true' | wc -l
```

Expected behavior: Early sessions have many failures, later sessions have fewer as bugs are fixed.

</details>

<details>
<summary><b>"Live dashboard not updating?"</b></summary>

**Ensure terminal supports ANSI escape codes:**
- Windows: Use Windows Terminal (not CMD)
- macOS/Linux: Any modern terminal works
- CI/CD: Use `--quiet` flag for plain text output

**Check console_output.py issues:**
```bash
# Test dashboard directly
python test/test_live_dashboard_tokens.py
```

If issues persist, use `--verbose` for traditional line-by-line output.

</details>

---

## Technology Stack

### Harness (Agent System)

<table>
<tr>
<td><b>Agent Framework</b></td>
<td>Claude Agent SDK (Anthropic)</td>
</tr>
<tr>
<td><b>API Support</b></td>
<td>Anthropic API, Azure Foundry (auto-detected)</td>
</tr>
<tr>
<td><b>Console UI</b></td>
<td>Rich (Python terminal formatting with live updates)</td>
</tr>
<tr>
<td><b>Logging</b></td>
<td>JSON + JSONL (custom comprehensive system)</td>
</tr>
<tr>
<td><b>Security</b></td>
<td>Multi-layer (Sandbox + Permissions + Allowlist)</td>
</tr>
</table>

### Generated Backend

<table>
<tr>
<td><b>Framework</b></td>
<td>FastAPI (Python 3.11+)</td>
</tr>
<tr>
<td><b>Database</b></td>
<td>PostgreSQL 15+ (Docker)</td>
</tr>
<tr>
<td><b>ORM</b></td>
<td>SQLAlchemy 2.0 (async)</td>
</tr>
<tr>
<td><b>Migrations</b></td>
<td>Alembic</td>
</tr>
<tr>
<td><b>Testing</b></td>
<td>pytest + pytest-asyncio + httpx</td>
</tr>
<tr>
<td><b>Validation</b></td>
<td>Pydantic v2 + pydantic-settings</td>
</tr>
<tr>
<td><b>Docs</b></td>
<td>Auto-generated OpenAPI/Swagger</td>
</tr>
<tr>
<td><b>Mock Data</b></td>
<td>Faker library (realistic data generation)</td>
</tr>
</table>

---

## Documentation

- **[LOGGING.md](LOGGING.md)** - Comprehensive logging system and analysis tools
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide for testing the harness
- **[CLAUDE.md](CLAUDE.md)** - Complete architecture, lean handoff, and OpenAPI best practices
- **[OPENAPI_IMPROVEMENTS_PLAN.md](OPENAPI_IMPROVEMENTS_PLAN.md)** - OpenAPI best practices implementation plan
- Generated `README.md` in each project - Setup and API usage instructions

---

## Contributing

Contributions welcome! Areas for improvement:

- Additional Figma Make template variations
- More example specifications (`example_specs/`)
- Performance optimizations for large projects
- Alternative database support (MySQL, SQLite, MongoDB)
- Frontend framework integration examples (Next.js, Vue, Svelte)
- Docker deployment configurations (Docker Compose, Kubernetes)
- CI/CD pipeline templates (GitHub Actions, GitLab CI)
- Additional security validations
- Log analysis enhancements (ML-based anomaly detection)

---

## License

MIT License - see LICENSE file for details

---

<div align="center">

**Built with [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)**

**Star if this helped you build better backends faster!**

Made with by developers who love automation

---

**Ready to build production backends in hours instead of weeks?**

```bash
pip install -r requirements.txt
python autonomous_agent_demo.py --project-dir ./my_awesome_api
```

</div>
