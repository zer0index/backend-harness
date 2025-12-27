# Frontend Development Quickstart

> **TL;DR:** Use `app_spec.txt` for business context, `openapi.json` for API documentation, and `docs/mock-data/*.json` for development.

---

## 📦 What's Included

| File | Purpose | How to Use |
|------|---------|------------|
| **app_spec.txt** | Business requirements, user workflows, feature priorities | Read to understand what to build and why |
| **openapi.json** | Complete API specification (endpoints, schemas, errors) | Import into Swagger UI or auto-generate TypeScript types |
| **docs/mock-data/** | Realistic JSON sample data | Import directly in your frontend during development |

---

## 🚀 Quick Start

### 1. Understand the Business Context

Read `app_spec.txt` to learn:
- What the application does
- Who the users are (roles and permissions)
- Key user workflows and journeys
- Suggested screens and features
- Feature priorities (MVP vs. nice-to-have)

### 2. Explore the API

**Option A: Interactive Documentation (Recommended)**
```bash
# Start the backend server
cd [project-directory]
./init.sh  # or ./init.ps1 on Windows

# Open Swagger UI in your browser
http://localhost:8000/docs
```

**Option B: Generate TypeScript Types**
```bash
# Auto-generate TypeScript interfaces from OpenAPI spec
npx openapi-typescript openapi.json -o api-types.ts
```

**Option C: Import into API Testing Tool**
- Open Postman/Insomnia
- Import `openapi.json`
- Test endpoints interactively

### 3. Build UI with Mock Data

**Use the mock data files during development:**

```typescript
// Import mock data (no backend needed)
import users from './docs/mock-data/users.json';
import tasks from './docs/mock-data/tasks.json';
import tags from './docs/mock-data/tags.json';
import comments from './docs/mock-data/comments.json';

// Build your UI components
function TaskList() {
  return (
    <div>
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          assignee={users.find(u => u.id === task.assignee_id)}
          tags={task.tag_ids.map(id => tags.find(t => t.id === id))}
        />
      ))}
    </div>
  );
}
```

**Benefits:**
- ✅ No backend dependency during UI development
- ✅ Realistic data with proper relationships
- ✅ Matches backend schemas exactly
- ✅ Easy to swap for real API calls later

### 4. Swap Mock Data for Real API

**When ready to integrate with the backend:**

```typescript
// Before (mock data)
import tasks from './docs/mock-data/tasks.json';

// After (real API)
const response = await fetch('http://localhost:8000/api/v1/tasks');
const data = await response.json();
const tasks = data.items;  // Paginated response
```

**Pro tip:** Create an abstraction layer with environment toggle:

```typescript
// api.ts
const USE_MOCK = process.env.VITE_USE_MOCK === 'true';

export async function getTasks(params = {}) {
  if (USE_MOCK) {
    const { default: tasks } = await import('./docs/mock-data/tasks.json');
    return { items: tasks, total: tasks.length, limit: 20, offset: 0, count: tasks.length };
  }

  const query = new URLSearchParams(params);
  const response = await fetch(`/api/v1/tasks?${query}`);
  return response.json();
}
```

---

## 📚 Key Concepts

### Authentication

**Current:** Mock authentication (development only)
- All requests automatically authenticated
- No `Authorization` header needed locally

**Production:** JWT Bearer tokens
```typescript
fetch('/api/v1/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

### Pagination

All list endpoints use **limit/offset pagination**:

```typescript
interface PaginatedResponse<T> {
  items: T[];
  total: number;      // Total items in database
  limit: number;      // Page size
  offset: number;     // Starting position (0-indexed)
  count: number;      // Items in this response
}

// Example: Get second page (items 20-39)
const response = await fetch('/api/v1/tasks?limit=20&offset=20');
const data: PaginatedResponse<Task> = await response.json();

console.log(`Showing ${data.count} of ${data.total} tasks`);
```

### Error Handling

All errors follow a consistent format:

```typescript
interface ErrorResponse {
  code: string;           // Machine-readable code (e.g., "USER_NOT_FOUND")
  message: string;        // Human-readable message
  details?: object;       // Additional context (validation errors, etc.)
  request_id?: string;    // For tracing
}

// Example error handling
try {
  const response = await fetch('/api/v1/tasks', { method: 'POST', body: JSON.stringify(taskData) });

  if (!response.ok) {
    const error: ErrorResponse = await response.json();
    console.error(`Error ${response.status}: ${error.message} (${error.code})`);

    if (error.details) {
      console.error('Details:', error.details);
    }
  }
} catch (err) {
  console.error('Network error:', err);
}
```

**Common status codes:**
- `200` - Success (GET, PUT)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate, constraint violation)
- `422` - Validation Error

---

## 🛠️ Development Workflow

### Step 1: Design Phase (Use Mock Data)
```typescript
// 1. Import mock data
import tasks from './docs/mock-data/tasks.json';

// 2. Build UI components
function TaskDashboard() {
  const [taskList, setTaskList] = useState(tasks);
  // ... build your UI
}
```

### Step 2: Integration Phase (Connect to API)
```typescript
// 1. Generate types from OpenAPI
// npx openapi-typescript openapi.json -o api-types.ts

// 2. Create API client
import type { PaginatedResponse, Task } from './api-types';

async function fetchTasks(): Promise<PaginatedResponse<Task>> {
  const response = await fetch('/api/v1/tasks');
  return response.json();
}

// 3. Replace mock imports with API calls
function TaskDashboard() {
  const [taskList, setTaskList] = useState<Task[]>([]);

  useEffect(() => {
    fetchTasks().then(data => setTaskList(data.items));
  }, []);
}
```

### Step 3: Testing Phase
```typescript
// Test with backend running locally
// 1. Start backend: ./init.sh
// 2. Backend runs on http://localhost:8000
// 3. Frontend connects to http://localhost:8000/api/v1/*
```

---

## 📖 Reference

### Data Models

See `docs/mock-data/README.md` for:
- Complete data model descriptions
- Field types and constraints
- Relationships between entities
- Example records

### API Endpoints

See `openapi.json` or http://localhost:8000/docs for:
- All available endpoints
- Request/response schemas
- Query parameters
- Authentication requirements
- Error responses

### Business Requirements

See `app_spec.txt` for:
- Application purpose and goals
- User roles and permissions
- Business rules and validation
- User workflows and journeys
- Feature priorities

---

## ✅ Checklist for Frontend Developers

**Before starting:**
- [ ] Read `app_spec.txt` to understand business requirements
- [ ] Review `docs/mock-data/README.md` to understand data models
- [ ] Import `openapi.json` into Swagger UI or generate TypeScript types

**During development:**
- [ ] Use mock data for all UI development
- [ ] Follow the data structures exactly (field names, types, relationships)
- [ ] Handle all response states (loading, success, error, empty)
- [ ] Test with realistic data from mock files

**Before deployment:**
- [ ] Replace mock data imports with real API calls
- [ ] Test with backend running locally
- [ ] Implement error handling for all endpoints
- [ ] Add authentication headers (JWT tokens)
- [ ] Handle pagination for list endpoints

---

## 🆘 Common Questions

**Q: Can I modify the data models (add fields, change types)?**
**A:** No. The backend is complete and cannot be modified. Use the schemas exactly as provided in `openapi.json`.

**Q: How do I add a new API endpoint?**
**A:** You can't. The backend is finished. Build frontend features using the existing endpoints.

**Q: The mock data doesn't have enough records. Can I add more?**
**A:** Yes! You can add more records to the JSON files, but keep the same structure.

**Q: Can I use a different pagination format (page/page_size instead of limit/offset)?**
**A:** No. The backend uses limit/offset. Your frontend must match this format.

**Q: Where's the detailed API documentation?**
**A:** In `openapi.json`. Import it into http://localhost:8000/docs for interactive docs.

---

**Happy building! 🚀**

For questions or issues, check:
1. `app_spec.txt` - Business requirements
2. `openapi.json` - API specification
3. `docs/mock-data/README.md` - Data models
4. http://localhost:8000/docs - Interactive API docs (when backend is running)
