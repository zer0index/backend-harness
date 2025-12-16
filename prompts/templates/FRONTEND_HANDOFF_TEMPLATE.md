# Frontend Integration Guide

> **Quick Links:**
> - Business Context: See `APP_OVERVIEW.md`
> - Mock Data: See `docs/mock-data/`
> - Full API Spec: See `openapi.json`

## Quick Start

### 1. Start the Backend

```bash
# Navigate to project directory
cd [project-name]

# Run setup script
./init.sh

# Or manually:
docker-compose up -d postgres
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 2. Access API Documentation

- **Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### 3. Frontend Development with Mock Data

**IMPORTANT:** For UI design and development, use the mock data files in `docs/mock-data/`:
- ✅ Matches backend schemas exactly
- ✅ Includes realistic relationships
- ✅ Ready for immediate use
- ✅ Easy to swap for real API later

See `docs/mock-data/README.md` for details.

---

## Authentication

**Current Implementation:** Mock authentication (development only)

All requests are automatically authenticated. The backend currently uses a mock authentication system that always returns a test user. No `Authorization` header is required during development.

**Mock User:**
```json
{
  "id": 1,
  "email": "test@example.com",
  "name": "Test User",
  "role": "admin"
}
```

**Future Implementation:** JWT tokens

The authentication system is designed to be easily swapped with JWT tokens for production use. The structure is already in place at `app/dependencies/auth.py`.

**Production Usage (Future):**
```javascript
const response = await fetch('http://localhost:8000/api/v1/endpoint', {
  headers: {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json'
  }
});
```

---

## Data Models

[This section will be populated by the agent based on Pydantic schemas]

### User

```typescript
interface User {
  id: number;
  email: string;
  name: string;
  role: "admin" | "manager" | "user";
  is_active: boolean;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
}
```

**Relationships:**
- Has many: Tasks (as creator), Tasks (as assignee), Comments
- Belongs to: None

**Business Rules:**
- Email must be unique
- Only admins can create/delete users
- Cannot delete user with active assigned tasks
- Role changes require admin permission

**Validation:**
- Email: valid format, max 255 chars
- Name: 1-100 characters
- Role: must be one of ["admin", "manager", "user"]

**Mock Data:** `docs/mock-data/users.json` (20 sample users)

[Repeat for each entity - Task, Tag, Comment, etc.]

---

## API Endpoints

[This section will be populated by the agent based on implemented endpoints]

### Users

#### List Users
`GET /api/v1/users`

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `page_size` (integer, default: 20, max: 100) - Items per page
- `role` (string, optional) - Filter by role ("admin", "manager", "user")
- `is_active` (boolean, optional) - Filter by active status

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

**Errors:**
- `401` - Unauthorized (missing/invalid auth)
- `403` - Forbidden (insufficient permissions)

#### Create User
`POST /api/v1/users`

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "role": "user"
}
```

**Response (201):** User object

**Errors:**
- `409` - Conflict (email already exists)
- `422` - Validation error (invalid email format, etc.)
- `403` - Forbidden (only admins can create users)

#### Get User
`GET /api/v1/users/{id}`

**Path Parameters:**
- `id` (integer) - User ID

**Response (200):** User object

**Errors:**
- `404` - User not found

#### Update User
`PUT /api/v1/users/{id}`

**Request Body:** User object (partial updates allowed)

**Response (200):** Updated user object

**Errors:**
- `404` - User not found
- `409` - Email already exists (if changing email)
- `403` - Forbidden (insufficient permissions)

#### Delete User
`DELETE /api/v1/users/{id}`

**Response (204):** No content

**Errors:**
- `404` - User not found
- `403` - Forbidden (only admins can delete users)
- `400` - Cannot delete user with active tasks

[Repeat for each resource group]

---

## Common Patterns

### Pagination

All list endpoints return paginated results in this format:

```json
{
  "items": [/* array of objects */],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

**Query Parameters:**
- `page` - Page number (1-indexed, default: 1)
- `page_size` - Items per page (default: 20, max: 100)

**Example:**
```javascript
const response = await fetch('/api/v1/tasks?page=2&page_size=50');
const data = await response.json();
console.log(`Showing ${data.items.length} of ${data.total} tasks`);
```

### Error Responses

All errors follow this consistent format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "ERROR_TYPE",
  "field_errors": {
    "field_name": ["Error description"]
  }
}
```

**Common Status Codes:**
- `200` - Success (GET, PUT)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- `400` - Bad Request (invalid data)
- `401` - Unauthorized (missing/invalid auth)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `409` - Conflict (duplicate email, etc.)
- `422` - Validation Error (Pydantic validation failures)
- `500` - Internal Server Error

**Example Error Handling:**
```javascript
try {
  const response = await fetch('/api/v1/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });

  if (!response.ok) {
    const error = await response.json();
    console.error(`Error ${response.status}:`, error.detail);

    // Handle validation errors
    if (response.status === 422 && error.field_errors) {
      Object.entries(error.field_errors).forEach(([field, errors]) => {
        console.error(`${field}: ${errors.join(', ')}`);
      });
    }

    return;
  }

  const task = await response.json();
  console.log('Task created:', task);
} catch (err) {
  console.error('Network error:', err);
}
```

### Timestamps

All timestamps are ISO 8601 format in UTC:
```
"2024-01-15T10:30:00Z"
```

**Parsing in JavaScript:**
```javascript
const date = new Date(task.created_at);
console.log(date.toLocaleDateString());  // "1/15/2024"
console.log(date.toLocaleTimeString());  // "10:30:00 AM"
```

### Filtering and Sorting

List endpoints support filtering and sorting via query parameters:

**Filtering:**
```
GET /api/v1/tasks?status=in_progress&priority=high&assignee_id=5
```

**Sorting:**
```
GET /api/v1/tasks?sort_by=due_date&sort_order=asc
```

**Combining:**
```
GET /api/v1/tasks?status=pending&sort_by=priority&sort_order=desc&page=1&page_size=20
```

### Enums

Enum fields accept specific string values only:

**Task Status:**
- `"pending"`
- `"in_progress"`
- `"completed"`
- `"cancelled"`

**Task Priority:**
- `"low"`
- `"medium"`
- `"high"`
- `"urgent"`

**User Role:**
- `"admin"`
- `"manager"`
- `"user"`

**Example:**
```javascript
await fetch('/api/v1/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'New Task',
    status: 'pending',        // Must use exact enum value
    priority: 'high',         // Case-sensitive
    assignee_id: 5
  })
});
```

---

## Example Integration

### Using Mock Data (Development)

```javascript
// Import mock data files
import users from './docs/mock-data/users.json';
import tasks from './docs/mock-data/tasks.json';
import tags from './docs/mock-data/tags.json';

// Use directly in your components
function TaskList() {
  return (
    <div>
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}

// Get related data
function getTaskWithAssignee(taskId) {
  const task = tasks.find(t => t.id === taskId);
  const assignee = users.find(u => u.id === task.assignee_id);
  return { ...task, assignee };
}
```

### Using Real API (Production)

```javascript
// Fetch tasks from API
async function fetchTasks(filters = {}) {
  const params = new URLSearchParams({
    page: filters.page || 1,
    page_size: filters.pageSize || 20,
    ...(filters.status && { status: filters.status }),
    ...(filters.priority && { priority: filters.priority })
  });

  const response = await fetch(`/api/v1/tasks?${params}`);

  if (!response.ok) {
    throw new Error('Failed to fetch tasks');
  }

  return await response.json();
}

// Create a new task
async function createTask(taskData) {
  const response = await fetch('/api/v1/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(taskData)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return await response.json();
}

// Update task status
async function updateTaskStatus(taskId, newStatus) {
  const response = await fetch(`/api/v1/tasks/${taskId}/status`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ status: newStatus })
  });

  if (!response.ok) {
    throw new Error('Failed to update task status');
  }

  return await response.json();
}
```

### Switching Between Mock and Real Data

Create an abstraction layer:

```javascript
// api.js
const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK === 'true';

export async function getTasks(filters = {}) {
  if (USE_MOCK_DATA) {
    // Use mock data
    const { default: tasks } = await import('./docs/mock-data/tasks.json');

    // Simulate filtering
    let filtered = tasks;
    if (filters.status) {
      filtered = filtered.filter(t => t.status === filters.status);
    }
    if (filters.assignee_id) {
      filtered = filtered.filter(t => t.assignee_id === filters.assignee_id);
    }

    // Simulate pagination
    const page = filters.page || 1;
    const pageSize = filters.pageSize || 20;
    const start = (page - 1) * pageSize;
    const end = start + pageSize;

    return {
      items: filtered.slice(start, end),
      total: filtered.length,
      page,
      page_size: pageSize,
      total_pages: Math.ceil(filtered.length / pageSize)
    };
  } else {
    // Use real API
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/v1/tasks?${params}`);
    return await response.json();
  }
}
```

---

## Testing the API

### Using Swagger UI (Recommended)

1. Navigate to **http://localhost:8000/docs**
2. Find the endpoint you want to test
3. Click on it to expand
4. Click **"Try it out"**
5. Fill in the request parameters/body
6. Click **"Execute"**
7. View the response below

**Benefits:**
- Interactive testing
- See request/response examples
- Understand parameter types
- No code needed

### Using cURL

```bash
# List tasks
curl http://localhost:8000/api/v1/tasks

# List tasks with filters
curl "http://localhost:8000/api/v1/tasks?status=in_progress&page=1&page_size=10"

# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Task description",
    "priority": "high",
    "assignee_id": 2
  }'

# Get task by ID
curl http://localhost:8000/api/v1/tasks/1

# Update task
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task",
    "status": "in_progress"
  }'

# Delete task
curl -X DELETE http://localhost:8000/api/v1/tasks/1
```

### Using Postman

1. Import the OpenAPI spec: **File → Import → `openapi.json`**
2. Postman will create a collection with all endpoints
3. Set base URL as environment variable: `http://localhost:8000`
4. Test endpoints interactively

---

## Resources

### Documentation
- **OpenAPI Spec**: `openapi.json` - Complete machine-readable API specification
- **Interactive Docs**: http://localhost:8000/docs - Try endpoints live with Swagger UI
- **Alternative Docs**: http://localhost:8000/redoc - Pretty documentation view
- **Business Context**: `APP_OVERVIEW.md` - User workflows and suggested screens
- **Mock Data**: `docs/mock-data/` - Sample data for UI development

### Source Code
- **Backend Source**: `app/` directory
- **Models**: `app/models/` - SQLAlchemy ORM models
- **Schemas**: `app/schemas/` - Pydantic request/response schemas
- **Routers**: `app/routers/v1/` - API endpoint handlers
- **Services**: `app/services/` - Business logic layer
- **Tests**: `tests/` - Pytest test suite

### Development
- **Setup Guide**: `README.md` in project root
- **Init Script**: `./init.sh` - One-command environment setup
- **Docker Compose**: `docker-compose.yml` - PostgreSQL configuration
- **Database Migrations**: `alembic/versions/` - Alembic migration files

---

## Support & Questions

**For questions about:**
- **API behavior** → Check `/docs` Swagger UI or `openapi.json`
- **Business logic** → See `APP_OVERVIEW.md` business rules section
- **Data structure** → See `docs/mock-data/` for examples
- **Setup issues** → See `README.md` or run `./init.sh`
- **Authentication** → Currently using mock auth (see Authentication section above)

**Common Issues:**
- **Database connection errors** → Make sure PostgreSQL is running: `docker-compose ps`
- **Migration errors** → Run `alembic upgrade head` to apply migrations
- **Import errors** → Reinstall dependencies: `pip install -r requirements.txt`
- **CORS errors** → CORS is enabled for development (all origins allowed)

---

## Next Steps

1. ✅ Start the backend locally (see Quick Start)
2. ✅ Explore the API in Swagger UI (http://localhost:8000/docs)
3. ✅ Import mock data files for UI development
4. ✅ Build frontend components using mock data
5. ✅ Test integration with real API
6. ✅ Replace mock data calls with real API calls
7. ✅ Deploy frontend + backend together

Happy building! 🚀
