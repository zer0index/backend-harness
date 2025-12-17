# Quick Start Guide - Testing with Simple Apps

This guide shows you how to quickly test the handoff documentation system with a simple todo list app.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your-api-key-here
```

## Quick Test with Todo List (Recommended)

**Perfect for testing the handoff documentation in ~10 minutes!**

### Step 1: Copy the Todo List Spec

```bash
# Copy the example todo list spec to be used by the agent
cp example_specs/todo_list.txt prompts/app_spec.txt
```

### Step 2: Run with Small Configuration

```bash
python autonomous_agent_demo.py --project-dir ./test_todo --config small --max-iterations 3
```

**What this does:**
- Uses `small` config: 20-30 test cases (instead of 100-200)
- Generates 5-10 endpoints (instead of 30-50)
- Creates 5 mock users, 15 mock todos (instead of 20 users, 50 tasks)
- Should complete in 3-5 sessions (instead of 10-15)
- Perfect for quick testing!

### Step 3: Check the Generated Handoff Docs

After the agent runs, check these files:

```bash
cd generations/test_todo

# Business context & workflows
cat docs/APP_OVERVIEW.md

# Technical integration guide
cat docs/FRONTEND_HANDOFF.md

# Mock data for frontend development
cat docs/mock-data/users.json
cat docs/mock-data/todos.json

# Mock data usage guide
cat docs/mock-data/README.md

# Complete API specification
cat openapi.json
```

**Expected handoff package:**
```
generations/test_todo/
├── docs/
│   ├── APP_OVERVIEW.md           ← Business context, workflows, screens
│   ├── FRONTEND_HANDOFF.md       ← API integration guide
│   └── mock-data/
│       ├── README.md             ← How to use mock data
│       ├── users.json            ← 5 sample users
│       ├── todos.json            ← 15 sample todos
│       └── (other entities...)
├── openapi.json                  ← Complete OpenAPI spec
└── scripts/
    └── generate_mock_data.py     ← Mock data generator
```

---

## Configuration Sizes

Choose the right config for your needs:

### Small (Quick Testing)
```bash
--config small
```
- **Test cases:** 20-30
- **Endpoints:** 5-10
- **Mock users:** 5
- **Mock main entity:** 15
- **Duration:** 3-5 sessions (~10-15 minutes)
- **Best for:** Todo lists, note apps, simple CRUD apps

### Medium (Default - Standard Apps)
```bash
--config medium
```
- **Test cases:** 100-200
- **Endpoints:** 30-50
- **Mock users:** 20
- **Mock main entity:** 50
- **Duration:** 10-15 sessions (~2-4 hours)
- **Best for:** Task managers, blogs, inventory systems

### Large (Complex Apps)
```bash
--config large
```
- **Test cases:** 300-500
- **Endpoints:** 60-100
- **Mock users:** 30
- **Mock main entity:** 100
- **Duration:** 20-30 sessions (~6-10 hours)
- **Best for:** E-commerce, CRM, ERP systems

---

## Example Usage Scenarios

### Scenario 1: Test Handoff Docs Quickly
```bash
# Use small config with todo list
cp example_specs/todo_list.txt prompts/app_spec.txt
python autonomous_agent_demo.py --project-dir ./test_todo --config small --max-iterations 3
```

### Scenario 2: Build a Simple Notes App
```bash
# 1. Create your own simple spec in prompts/app_spec.txt
# 2. Run with small config
python autonomous_agent_demo.py --project-dir ./my_notes --config small
```

### Scenario 3: Build Production Task Manager
```bash
# 1. Use the default task management spec (already in prompts/app_spec.txt)
# 2. Run with medium config (default)
python autonomous_agent_demo.py --project-dir ./task_manager
```

### Scenario 4: Build Complex E-commerce Backend
```bash
# 1. Create comprehensive e-commerce spec in prompts/app_spec.txt
# 2. Run with large config
python autonomous_agent_demo.py --project-dir ./ecommerce --config large
```

---

## What Gets Generated

### Backend Code
- ✅ FastAPI application with async SQLAlchemy
- ✅ PostgreSQL database (Docker)
- ✅ Pydantic schemas (request/response validation)
- ✅ Alembic migrations
- ✅ Comprehensive pytest test suite (>80% coverage)
- ✅ Mock authentication (swappable for JWT)

### Handoff Documentation
- ✅ **APP_OVERVIEW.md** - Business context, user workflows, suggested screens
- ✅ **FRONTEND_HANDOFF.md** - Technical integration guide with code examples
- ✅ **Mock data files** - Realistic JSON data for frontend development
- ✅ **openapi.json** - Complete machine-readable API spec

---

## Verifying the Handoff Package

After generation, verify the handoff docs:

```bash
cd generations/test_todo

# 1. Check APP_OVERVIEW.md has workflows
grep -A 5 "Workflow" docs/APP_OVERVIEW.md

# 2. Check FRONTEND_HANDOFF.md has TypeScript interfaces
grep -A 10 "interface" docs/FRONTEND_HANDOFF.md

# 3. Check mock data is realistic (not "test1", "test2")
head -20 docs/mock-data/users.json

# 4. Check OpenAPI spec exists
ls -lh openapi.json

# 5. Verify mock data README has code examples
grep -A 5 "React" docs/mock-data/README.md
```

---

## Running the Generated Backend

To test the generated API:

```bash
cd generations/test_todo

# Run the init script (sets up everything)
./init.sh

# Or manually:
docker compose up -d postgres
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Access the API
open http://localhost:8000/docs  # Swagger UI
```

---

## Troubleshooting

### Issue: Config not loading
```bash
# Check configs directory exists
ls -la configs/

# Should see: small.json, medium.json, large.json
```

### Issue: Placeholders not replaced
```bash
# Check prompts.py has apply_config_to_prompt function
grep "apply_config_to_prompt" prompts.py
```

### Issue: Agent generating too many tests
```bash
# Verify you're passing --config small
python autonomous_agent_demo.py --project-dir ./test --config small

# Check which config is being used (look for this in output)
📋 Using 'small' configuration: Simple application...
```

---

## Tips

### Quick Iteration
- Use `--config small` for fast testing
- Use `--max-iterations 3` to limit runtime
- Use simple specs like `example_specs/todo_list.txt`

### Production Apps
- Use `--config medium` or `--config large`
- Don't limit iterations (let it run to completion)
- Create detailed specs in `prompts/app_spec.txt`

### Creating Custom Specs
1. Copy `example_specs/todo_list.txt` as a template
2. Update the "Core Resources" section
3. Update "User Workflows & Journeys"
4. Update "Suggested Screen Structure"
5. Save to `prompts/app_spec.txt`
6. Run the agent

---

## Next Steps

1. ✅ Test with todo list using `--config small`
2. ✅ Review generated handoff docs
3. ✅ Verify mock data is realistic
4. ✅ Check OpenAPI spec completeness
5. ✅ Try creating your own simple spec
6. ✅ Hand off docs to Figma Make for UI generation

---

## Questions?

- **Config values:** See `configs/*.json` files
- **Placeholder list:** See `prompts.py` - `apply_config_to_prompt()` function
- **Example specs:** See `example_specs/` directory
- **Full docs:** See `README.md` and `CLAUDE.md`

Happy testing! 🚀
