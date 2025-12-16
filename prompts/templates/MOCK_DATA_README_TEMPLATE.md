# Mock Data for Frontend Development

## Overview

This directory contains realistic mock data that **perfectly mirrors** the backend data models. Use this data when designing and building the frontend UI without needing a running backend server.

## Why Mock Data?

- ✅ **Perfectly Aligned**: Matches Pydantic schemas and database models exactly
- ✅ **Realistic**: Contains proper relationships, enums, and data patterns
- ✅ **Ready to Use**: Import and use immediately in your frontend
- ✅ **Easy Swap**: Replace with real API calls when ready
- ✅ **No Backend Dependency**: Build UI while backend is being developed
- ✅ **Faster Development**: No need to wait for API responses during development

## Available Files

[This section will be populated by the agent based on entities]

### `users.json`
Sample user accounts with different roles (admin, manager, user).

**Count:** 20 users
**Includes:** Active and inactive users, various roles, realistic names and emails

**Example:**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "name": "Alice Admin",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### `tasks.json`
Sample tasks with various statuses, priorities, assignments, and due dates.

**Count:** 50 tasks
**Includes:** All status types, all priority levels, assigned and unassigned tasks, overdue tasks, completed tasks

**Relationships:** References users by `assignee_id` and `creator_id`

**Example:**
```json
{
  "id": 1,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "status": "in_progress",
  "priority": "high",
  "assignee_id": 5,
  "creator_id": 1,
  "due_date": "2024-02-01T00:00:00Z",
  "completed_at": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

### `tags.json`
Sample tags for categorizing tasks.

**Count:** 10 tags
**Includes:** Common tags with hex colors

**Example:**
```json
{
  "id": 1,
  "name": "Backend",
  "color": "#FF5733",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### `comments.json`
Sample comments on tasks.

**Count:** 30 comments
**Includes:** Various comment lengths, different users commenting

**Relationships:** References tasks by `task_id` and users by `user_id`

**Example:**
```json
{
  "id": 1,
  "task_id": 1,
  "user_id": 5,
  "content": "I've started working on this. Should have a PR ready by tomorrow.",
  "created_at": "2024-01-16T09:15:00Z",
  "updated_at": "2024-01-16T09:15:00Z"
}
```

---

## How to Use

### In React

```javascript
// Import the mock data
import users from './docs/mock-data/users.json';
import tasks from './docs/mock-data/tasks.json';
import tags from './docs/mock-data/tags.json';
import comments from './docs/mock-data/comments.json';

// Use in your components
function TaskList() {
  const [taskList, setTaskList] = useState(tasks);

  return (
    <div>
      {taskList.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}

// Get task with related user data
function TaskDetail({ taskId }) {
  const task = tasks.find(t => t.id === taskId);
  const assignee = users.find(u => u.id === task.assignee_id);
  const creator = users.find(u => u.id === task.creator_id);

  return (
    <div>
      <h1>{task.title}</h1>
      <p>Assigned to: {assignee?.name}</p>
      <p>Created by: {creator?.name}</p>
    </div>
  );
}
```

### In Vue

```vue
<template>
  <div>
    <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
  </div>
</template>

<script>
import tasks from './docs/mock-data/tasks.json';
import users from './docs/mock-data/users.json';

export default {
  data() {
    return {
      tasks,
      users
    };
  },
  methods: {
    getUserById(userId) {
      return this.users.find(u => u.id === userId);
    }
  }
};
</script>
```

### In Svelte

```svelte
<script>
  import tasks from './docs/mock-data/tasks.json';
  import users from './docs/mock-data/users.json';

  function getAssignee(task) {
    return users.find(u => u.id === task.assignee_id);
  }
</script>

{#each tasks as task}
  <TaskCard {task} assignee={getAssignee(task)} />
{/each}
```

---

## Common Operations

### Simulating Relationships

#### Get Task with Assignee and Creator

```javascript
function getTaskWithRelations(taskId) {
  const task = tasks.find(t => t.id === taskId);
  if (!task) return null;

  const assignee = task.assignee_id
    ? users.find(u => u.id === task.assignee_id)
    : null;
  const creator = users.find(u => u.id === task.creator_id);

  return {
    ...task,
    assignee,
    creator
  };
}
```

#### Get Task Comments with User Info

```javascript
function getTaskComments(taskId) {
  return comments
    .filter(c => c.task_id === taskId)
    .map(comment => ({
      ...comment,
      user: users.find(u => u.id === comment.user_id)
    }))
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}
```

#### Get User's Tasks

```javascript
function getUserTasks(userId) {
  return tasks.filter(t => t.assignee_id === userId);
}
```

### Filtering Examples

```javascript
// Get high priority tasks
const highPriorityTasks = tasks.filter(t => t.priority === 'high');

// Get tasks assigned to a specific user
const userTasks = tasks.filter(t => t.assignee_id === userId);

// Get overdue tasks
const now = new Date();
const overdueTasks = tasks.filter(t =>
  t.due_date &&
  new Date(t.due_date) < now &&
  t.status !== 'completed' &&
  t.status !== 'cancelled'
);

// Get tasks by status
const pendingTasks = tasks.filter(t => t.status === 'pending');
const inProgressTasks = tasks.filter(t => t.status === 'in_progress');
const completedTasks = tasks.filter(t => t.status === 'completed');

// Get unassigned tasks
const unassignedTasks = tasks.filter(t => !t.assignee_id);

// Get tasks with specific tag
function getTasksByTag(tagId) {
  // In real implementation, you'd use task_tags junction table
  // For mock data, you might include tag_ids array in tasks
  return tasks.filter(t => t.tag_ids?.includes(tagId));
}
```

### Sorting Examples

```javascript
// Sort by due date (earliest first)
const sortedByDueDate = [...tasks].sort((a, b) =>
  new Date(a.due_date) - new Date(b.due_date)
);

// Sort by priority (urgent → high → medium → low)
const priorityOrder = { urgent: 0, high: 1, medium: 2, low: 3 };
const sortedByPriority = [...tasks].sort((a, b) =>
  priorityOrder[a.priority] - priorityOrder[b.priority]
);

// Sort by created date (newest first)
const sortedByCreated = [...tasks].sort((a, b) =>
  new Date(b.created_at) - new Date(a.created_at)
);

// Sort by status
const statusOrder = { pending: 0, in_progress: 1, completed: 2, cancelled: 3 };
const sortedByStatus = [...tasks].sort((a, b) =>
  statusOrder[a.status] - statusOrder[b.status]
);
```

### Pagination Simulation

```javascript
function paginateTasks(tasks, page = 1, pageSize = 20) {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;

  return {
    items: tasks.slice(start, end),
    total: tasks.length,
    page,
    page_size: pageSize,
    total_pages: Math.ceil(tasks.length / pageSize)
  };
}

// Usage
const page1 = paginateTasks(tasks, 1, 20);
console.log(page1);
// {
//   items: [...20 tasks...],
//   total: 50,
//   page: 1,
//   page_size: 20,
//   total_pages: 3
// }
```

### Search Simulation

```javascript
function searchTasks(query) {
  const lowerQuery = query.toLowerCase();
  return tasks.filter(t =>
    t.title.toLowerCase().includes(lowerQuery) ||
    t.description?.toLowerCase().includes(lowerQuery)
  );
}

// Usage
const results = searchTasks('authentication');
```

### CRUD Simulation

For development, you can simulate CRUD operations:

```javascript
// Create (add to local state)
function createTask(taskData) {
  const newTask = {
    id: Math.max(...tasks.map(t => t.id)) + 1,
    ...taskData,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  tasks.push(newTask);
  return newTask;
}

// Update (modify local state)
function updateTask(taskId, updates) {
  const index = tasks.findIndex(t => t.id === taskId);
  if (index === -1) return null;

  tasks[index] = {
    ...tasks[index],
    ...updates,
    updated_at: new Date().toISOString()
  };
  return tasks[index];
}

// Delete (remove from local state)
function deleteTask(taskId) {
  const index = tasks.findIndex(t => t.id === taskId);
  if (index === -1) return false;

  tasks.splice(index, 1);
  return true;
}
```

---

## Switching to Real API

When you're ready to connect to the real backend, here's how to switch:

### Option 1: Environment Variable Toggle

```javascript
// api.js
const USE_MOCK_DATA = process.env.REACT_APP_USE_MOCK === 'true';

export async function getTasks(filters = {}) {
  if (USE_MOCK_DATA) {
    // Return mock data
    const { default: tasks } = await import('./docs/mock-data/tasks.json');
    return { items: tasks, total: tasks.length, page: 1, page_size: tasks.length };
  } else {
    // Fetch from real API
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/v1/tasks?${params}`);
    return await response.json();
  }
}

// In your .env file:
// REACT_APP_USE_MOCK=true   (development with mock data)
// REACT_APP_USE_MOCK=false  (production with real API)
```

### Option 2: API Abstraction Layer

```javascript
// api/index.js
import * as mockApi from './mockApi';
import * as realApi from './realApi';

const api = process.env.NODE_ENV === 'development' ? mockApi : realApi;

export default api;

// api/mockApi.js
import tasks from '../docs/mock-data/tasks.json';
import users from '../docs/mock-data/users.json';

export async function getTasks(filters) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300));

  let filtered = tasks;
  if (filters.status) {
    filtered = filtered.filter(t => t.status === filters.status);
  }

  return { items: filtered, total: filtered.length };
}

export async function getUsers() {
  await new Promise(resolve => setTimeout(resolve, 300));
  return { items: users, total: users.length };
}

// api/realApi.js
const API_BASE = 'http://localhost:8000';

export async function getTasks(filters) {
  const params = new URLSearchParams(filters);
  const response = await fetch(`${API_BASE}/api/v1/tasks?${params}`);
  return await response.json();
}

export async function getUsers() {
  const response = await fetch(`${API_BASE}/api/v1/users`);
  return await response.json();
}

// In your components:
import api from './api';

function TaskList() {
  useEffect(() => {
    api.getTasks({ status: 'pending' }).then(data => {
      setTasks(data.items);
    });
  }, []);
}
```

### Option 3: Simple Find and Replace

Before (mock data):
```javascript
import tasks from './docs/mock-data/tasks.json';
```

After (real API):
```javascript
const response = await fetch('http://localhost:8000/api/v1/tasks');
const data = await response.json();
const tasks = data.items;
```

---

## Data Integrity

These mock files are generated to ensure data integrity:

✅ **Schema Compliance:**
- All required fields are present
- Data types match Pydantic schemas exactly
- Field lengths respect validation rules

✅ **Valid Enums:**
- Status values: only `"pending"`, `"in_progress"`, `"completed"`, `"cancelled"`
- Priority values: only `"low"`, `"medium"`, `"high"`, `"urgent"`
- Role values: only `"admin"`, `"manager"`, `"user"`

✅ **Referential Integrity:**
- All `assignee_id` values reference existing user IDs
- All `creator_id` values reference existing user IDs
- All `task_id` values in comments reference existing task IDs
- All `user_id` values in comments reference existing user IDs

✅ **Realistic Patterns:**
- Timestamps are chronologically consistent (created_at < updated_at)
- Completed tasks have `completed_at` timestamps
- Overdue tasks have past due_dates
- Active users have `is_active: true`
- Mix of assigned and unassigned tasks

✅ **Edge Cases Included:**
- Null/optional fields (unassigned tasks, null descriptions)
- Edge case values (long descriptions, special characters in names)
- Boundary values (max length strings, min/max dates)

---

## Regenerating Mock Data

If the backend schemas change, regenerate mock data:

### Method 1: Run the Generation Script

```bash
# From project root
python scripts/generate_mock_data.py
```

This will:
1. Read current Pydantic schemas
2. Generate new realistic mock data
3. Preserve referential integrity
4. Overwrite files in `docs/mock-data/`

### Method 2: Generate from Database

If you have a populated development database:

```bash
# Export from database
python scripts/export_mock_data_from_db.py
```

### Method 3: Manual Editing

You can manually edit the JSON files if you need specific test cases:

1. Open `docs/mock-data/[entity].json`
2. Add/modify records
3. Ensure IDs are unique
4. Ensure foreign keys reference existing records
5. Use valid enum values
6. Format timestamps as ISO 8601

---

## Tips & Best Practices

### 1. Don't Modify Mock Files Directly in Code

**Bad:**
```javascript
import tasks from './docs/mock-data/tasks.json';
tasks.push(newTask);  // Modifies the imported file
```

**Good:**
```javascript
import tasksData from './docs/mock-data/tasks.json';
const [tasks, setTasks] = useState([...tasksData]);  // Create a copy
setTasks([...tasks, newTask]);  // Modify the copy
```

### 2. Simulate API Delays

Add artificial delays to simulate network latency:

```javascript
async function getTasks() {
  // Simulate 300ms API delay
  await new Promise(resolve => setTimeout(resolve, 300));

  const { default: tasks } = await import('./docs/mock-data/tasks.json');
  return tasks;
}
```

### 3. Handle Relationships Consistently

Create helper functions for relationships:

```javascript
// helpers.js
export function enrichTaskWithRelations(task, users) {
  return {
    ...task,
    assignee: task.assignee_id ? users.find(u => u.id === task.assignee_id) : null,
    creator: users.find(u => u.id === task.creator_id)
  };
}

// Usage
const enrichedTasks = tasks.map(task => enrichTaskWithRelations(task, users));
```

### 4. Test with Mock Data First

Before integrating with the real API:
- Build all UI components with mock data
- Test filtering, sorting, pagination
- Test CRUD operations (in local state)
- Verify all relationships work
- Test edge cases (empty states, errors, loading)

### 5. Use TypeScript for Type Safety

```typescript
// types.ts
export interface User {
  id: number;
  email: string;
  name: string;
  role: 'admin' | 'manager' | 'user';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assignee_id: number | null;
  creator_id: number;
  due_date: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

// Import with types
import tasksData from './docs/mock-data/tasks.json';
const tasks: Task[] = tasksData;
```

---

## Troubleshooting

### Issue: "Cannot find module './docs/mock-data/tasks.json'"

**Solution:** Ensure you're importing from the correct path relative to your component:
```javascript
// If your component is in src/components/
import tasks from '../../docs/mock-data/tasks.json';
```

### Issue: "Task assignee is undefined"

**Solution:** Some tasks may have `assignee_id: null` (unassigned). Always check:
```javascript
const assignee = task.assignee_id
  ? users.find(u => u.id === task.assignee_id)
  : null;
```

### Issue: "Dates are showing as strings"

**Solution:** Parse ISO 8601 timestamps to Date objects:
```javascript
const dueDate = new Date(task.due_date);
console.log(dueDate.toLocaleDateString());
```

### Issue: "Mock data doesn't update when I modify it"

**Solution:** You're likely importing a static file. Create a copy:
```javascript
const [tasks, setTasks] = useState([...tasksData]);
```

---

## Summary

**Development Workflow:**
1. ✅ Import mock data files
2. ✅ Build UI components using mock data
3. ✅ Test all features with mock data
4. ✅ Create API abstraction layer
5. ✅ Switch to real API with environment variable
6. ✅ Test with real backend
7. ✅ Deploy to production

**Benefits:**
- 🚀 Faster development (no backend dependency)
- ✅ Consistent data structure (matches API exactly)
- 🎯 Test edge cases easily
- 🔄 Simple toggle to switch to real API

Happy coding! 🎉
