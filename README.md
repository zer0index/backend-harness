<div align="center">

# 🚀 Autonomous Backend API Generator

**Production-ready FastAPI backends built by AI agents**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Claude Agent SDK](https://img.shields.io/badge/Claude-Agent%20SDK-orange.svg)](https://github.com/anthropics/anthropic-sdk-python)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*An autonomous coding harness that generates complete FastAPI backends with PostgreSQL, tests, migrations, and frontend handoff docs—all from a simple specification.*

[Quick Start](#-quick-start) • [Features](#-what-you-get) • [How It Works](#-how-it-works) • [Examples](#-use-cases)

</div>

---

## ✨ What You Get

<table>
<tr>
<td width="50%" valign="top">

### 🎯 **Backend Core**
- ✅ RESTful API with full CRUD
- ✅ PostgreSQL + Docker setup
- ✅ Async SQLAlchemy ORM
- ✅ Pydantic schemas (v2)
- ✅ Alembic migrations
- ✅ Auto-generated OpenAPI docs
- ✅ Mock auth (JWT-ready)

</td>
<td width="50%" valign="top">

### 🧪 **Quality & Docs**
- ✅ Comprehensive pytest suite (>80% coverage)
- ✅ Frontend handoff docs
- ✅ TypeScript interfaces
- ✅ Realistic mock data (JSON)
- ✅ Business workflows guide
- ✅ Integration examples
- ✅ OpenAPI spec export

</td>
</tr>
</table>

> **Perfect for:** Generating backends to hand off to frontend tools like Figma Make, v0, or any TypeScript project.

---

## 🏃 Quick Start

### Prerequisites

```bash
# Install dependencies
npm install -g @anthropic-ai/claude-code
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY='your-key-here'
# or create .env file with: ANTHROPIC_API_KEY=your-key-here
```

### Generate Your API

```bash
# Full generation (production-ready)
python autonomous_agent_demo.py --project-dir ./my_api

# Quick test (minimal endpoints, 1-3 minutes)
python autonomous_agent_demo.py --project-dir ./test_run --config test --max-iterations 2
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

🎉 **Done!** Visit http://localhost:8000/docs for interactive API documentation.

---

## 🧠 How It Works

### Two-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Session 1: Initializer Agent                                   │
├─────────────────────────────────────────────────────────────────┤
│  • Reads your app_spec.txt                                       │
│  • Generates 100-200 test specifications                         │
│  • Creates FastAPI project structure                             │
│  • Sets up PostgreSQL + Docker + Alembic                         │
│  • Initializes git repository                                    │
│  • Outputs: feature_list.json (source of truth)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Sessions 2+: Coding Agent (autonomous iterations)              │
├─────────────────────────────────────────────────────────────────┤
│  • Fresh context each session                                    │
│  • Implements endpoints: Model → Schema → Service → Router       │
│  • Writes & runs pytest tests                                    │
│  • Updates feature_list.json on test pass                        │
│  • Commits progress to git                                       │
│  • Auto-continues after 3 seconds (Ctrl+C to pause)              │
└─────────────────────────────────────────────────────────────────┘
```

<details>
<summary><b>⏱️ Timing Expectations</b> (click to expand)</summary>

| Phase | Duration | Details |
|-------|----------|---------|
| **First session** | 3-10 min | Generates 100-200 test specs (may appear to hang—normal!) |
| **Per iteration** | 5-15 min | Implements endpoints + tests + git commit |
| **Full API** | Several hours | Depends on spec size (pause/resume anytime) |

💡 **Tip:** Reduce test count in `prompts/initializer_prompt.md` (e.g., 20-50) for faster demos.

</details>

---

## 📦 Frontend Handoff Package

Every generated backend includes docs perfect for frontend developers:

| Document | Purpose | Contains |
|----------|---------|----------|
| **📋 APP_OVERVIEW.md** | Business context & UX workflows | User roles, step-by-step journeys, screen suggestions, navigation |
| **🔌 FRONTEND_HANDOFF.md** | Technical integration guide | TypeScript interfaces, endpoint summaries, auth setup, code examples |
| **🎨 Mock Data (JSON)** | Realistic test data | Users, tasks, tags, comments—ready to import, matches API schemas exactly |
| **📖 openapi.json** | Machine-readable spec | Import to Postman, Insomnia, or code generators |

**Why it matters:** Frontend devs can start immediately with mock data, no backend dependency. When ready, swap for real API calls with minimal changes.

---

## 🔒 Security Model

Defense-in-depth approach with multiple layers:

1. **🏖️ Sandbox**: OS-level isolation for bash commands
2. **📁 Filesystem Guard**: File ops restricted to project directory only
3. **✅ Command Allowlist**: Only approved commands can execute

<details>
<summary><b>Allowed Commands</b> (click to expand)</summary>

- **Files**: `ls`, `cat`, `head`, `tail`, `wc`, `grep`
- **Python**: `python`, `python3`, `pip`, `pytest`, `coverage`
- **Server**: `uvicorn`
- **Database**: `alembic`, `docker`, `docker compose`
- **Quality**: `ruff`, `black`, `mypy`
- **VCS**: `git`
- **Process**: `ps`, `lsof`, `sleep`, `pkill`

Edit `security.py` to modify. Run `python test_security.py` to validate (116 tests).

</details>

---

## 🛠️ Configuration

### Command Line Options

```bash
python autonomous_agent_demo.py \
  --project-dir ./my_api \           # Output directory
  --max-iterations 10 \               # Limit iterations (optional)
  --model claude-sonnet-4-5-20250929  # Claude model (optional)
```

### Customize Your API

<details>
<summary><b>Change API Specification</b></summary>

Edit `prompts/app_spec.txt` with your backend requirements. Current example: Task Management API (Users, Tasks, Tags, Comments).

</details>

<details>
<summary><b>Adjust Test Coverage</b></summary>

Edit `prompts/initializer_prompt.md` and change `100-200 test cases` to your preferred number (e.g., 20-50 for quick demos).

</details>

<details>
<summary><b>Modify Security Allowlist</b></summary>

Edit `ALLOWED_COMMANDS` in `security.py`, then validate:
```bash
python test_security.py  # All 116 tests should pass
```

</details>

---

## 📂 Project Structure

<details>
<summary><b>Generated FastAPI Project</b> (click to expand)</summary>

```
my_api/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # Async SQLAlchemy
│   ├── models/              # ORM models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/v1/          # API endpoints
│   ├── services/            # Business logic
│   └── dependencies/        # DI (auth, DB session)
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── api/v1/              # API tests
├── alembic/                 # DB migrations
├── docs/                    # Frontend handoff
│   ├── APP_OVERVIEW.md
│   ├── FRONTEND_HANDOFF.md
│   └── mock-data/           # JSON files
├── docker-compose.yml       # PostgreSQL
├── feature_list.json        # Test specs (source of truth)
├── init.sh / init.ps1       # Setup scripts
└── README.md
```

</details>

---

## 💡 Use Cases

This harness can generate backends for:

- 📝 Task/project management
- 🛒 E-commerce & inventory
- 📰 Blog/CMS platforms
- 👥 User management systems
- 📅 Booking/reservation systems
- 🔐 Authentication services
- 📊 Analytics dashboards
- ...any RESTful API with CRUD operations

---

## 🆘 Troubleshooting

<details>
<summary><b>"Appears to hang on first run"</b></summary>

✅ **Normal behavior.** The initializer is generating 100-200 test specifications. Watch for `[Tool: ...]` output to confirm it's working. First session takes 3-10 minutes.

</details>

<details>
<summary><b>"Command blocked by security hook"</b></summary>

🔒 **Security working as intended.** The agent tried a command not in the allowlist. To permit it:
1. Add to `ALLOWED_COMMANDS` in `security.py`
2. Run `python test_security.py` to validate
3. Restart the agent

</details>

<details>
<summary><b>"Can't access http://localhost:8000/docs"</b></summary>

⚠️ **Init scripts don't start the server.** After running `init.sh`/`init.ps1`, manually start:
```bash
uvicorn app.main:app --reload --port 8000
```

</details>

<details>
<summary><b>"PostgreSQL connection failed"</b></summary>

🐳 Ensure Docker is running:
```bash
docker compose up -d postgres
```

</details>

<details>
<summary><b>"API key not set"</b></summary>

🔑 Create `.env` file:
```bash
ANTHROPIC_API_KEY=your-key-here
```
Or export as environment variable.

</details>

---

## 🎯 Technology Stack

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
<td>Pydantic v2</td>
</tr>
<tr>
<td><b>Docs</b></td>
<td>Auto-generated OpenAPI/Swagger</td>
</tr>
</table>

---

<div align="center">

**Built with [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python) | Star ⭐ if this helped you!**

</div>
