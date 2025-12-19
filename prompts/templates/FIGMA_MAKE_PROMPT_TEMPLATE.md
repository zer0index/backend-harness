# 🎨 Frontend Development Kickoff Prompt

> **Purpose:** This prompt guides AI-assisted frontend development tools (Figma Make, v0, Lovable, etc.) to build a React/TypeScript frontend that perfectly integrates with your generated FastAPI backend.

---

## 🚀 Getting Started

I need your help building a modern, production-ready frontend for this application. **Before we start generating code**, I want us to go through a collaborative planning process to ensure we build the right thing.

### 📦 What I'm Providing You

This project includes complete backend handoff documentation:

1. **APP_OVERVIEW.md** - Business context, user workflows, and feature descriptions
2. **FRONTEND_HANDOFF.md** - Technical integration guide with TypeScript interfaces and API endpoints
3. **mock-data/** - Realistic JSON data files that match the backend schemas exactly
4. **openapi.json** - Machine-readable API specification (backend exports this)

**IMPORTANT:** These data models are final and cannot be changed. The backend is already built and deployed.

### ⚠️ CRITICAL: Development Environment Constraint

**Figma Make runs in the cloud and CANNOT access local servers!**

This means:
- ❌ You CANNOT call `http://localhost:8000` or any local API
- ❌ You CANNOT connect to services running on my computer
- ✅ You MUST use the mock data from `mock-data/*.json` files for ALL development
- ✅ Code should be structured so I can easily swap mock data for real API calls after download

**Read `guidelines/guideline.md` for detailed patterns on mock data development and API swapping.**

---

## 📋 Phase 1: Review & Understanding

**STOP - Don't generate code yet!**

First, please review the handoff documentation and provide me with:

### 1.1 File Summary

For each file, summarize:
- **APP_OVERVIEW.md**: What is this application? What problem does it solve? Who are the users?
- **FRONTEND_HANDOFF.md**: What are the main data models? What API endpoints are available?
- **mock-data/**: What entities exist? What are the relationships between them?

### 1.2 Data Model Understanding

List all primary entities (e.g., User, Task, Comment) and their key relationships. For example:
```
User
  ↓ has many
Tasks
  ↓ has many
Comments
```

### 1.3 Key Constraints

Identify any important constraints from the documentation:
- Required fields
- Enum values (status types, categories, etc.)
- Validation rules
- Privacy/permission rules

**Once you've completed this review, pause and share your understanding with me. I'll confirm before we move to brainstorming.**

---

## 💡 Phase 2: Brainstorming Frontend Features

Now that you understand the backend, let's brainstorm how to build a great user experience.

### 2.1 Core Features Review

Based on APP_OVERVIEW.md, list the **must-have features** we need to implement. Prioritize them:
- **P0 (Critical)**: Features needed for MVP
- **P1 (Important)**: Key features for full experience
- **P2 (Nice-to-have)**: Enhancements we can add later

**REQUIRED: Feature Playground Page**

Every application MUST include a dedicated **Playground/Showcase page** accessible via the main navigation:

**Purpose:**
- Test all features, components, and animations before deployment
- Demonstrate all UI patterns and interactions in one place
- Validate responsiveness and accessibility
- Provide a comprehensive testing environment

**What to include:**
- 🎨 All UI components (buttons, forms, modals, cards, etc.) with different states
- 🎭 All animations and transitions used in the app
- 📊 Sample visualizations (charts, graphs, dashboards) with realistic data
- 🔄 Interactive features (drag-and-drop, filters, search, sorting)
- ⚡ Loading states, error states, empty states
- 📱 Responsive breakpoint testing indicators
- ♿ Accessibility features (keyboard navigation, screen reader hints)

**Navigation:**
- Add a "Playground" or "🧪 Playground" tab in the main navigation
- Can be hidden in production (environment variable toggle)
- Should use mock data for all demonstrations

This page should be implemented as a **P1 feature** after core functionality is working.

### 2.2 Creative Frontend Features Using Existing Backend

**IMPORTANT:** The backend is complete and cannot be modified. Your job is to think creatively about what **frontend features** we can build using the **existing API endpoints and data**.

**❌ Wrong Approach:**
- "We could add a new analytics endpoint to the backend..."
- "The backend should calculate statistics..."
- "We need the backend to support dashboard data..."

**✅ Right Approach:**
- "Using the existing task data (with created_at, status, user_id fields), we could build:
  - 📊 Activity dashboard showing tasks created per day (calculated in frontend)
  - 📈 Progress charts by status distribution (aggregated client-side)
  - 🎯 User productivity metrics (derived from existing task data)
  - 📅 Calendar view of task deadlines (using due_date field)
  - 🔥 Streak tracking for completed tasks (calculated from timestamps)"

### Brainstorming Framework

Review the mock data files and FRONTEND_HANDOFF.md, then ask yourself:

**1. What visualizations could display this data?**
- Example: Tasks with timestamps → Timeline view, activity heatmap
- Example: Tasks with tags → Tag cloud, category breakdown chart
- Example: Comments with user IDs → User contribution graph

**2. What dashboards could provide insights?**
- Example: User data with activity timestamps → Active users dashboard, engagement metrics
- Example: Tasks with status/priority → Project health overview, bottleneck analysis

**3. What creative UI interactions are possible?**
- Example: Tasks with relationships → Kanban board, dependency graph, Gantt chart
- Example: Users with roles → Organization chart, team structure visualization
- Example: Items with hierarchy → Tree view, nested navigation

**4. What filtering & search capabilities?**
- Example: Tasks with multiple fields → Advanced multi-filter panel
- Example: Text fields → Full-text search with autocomplete
- Example: Date fields → Date range picker, "last 7 days" quick filters

**5. What bulk operations make sense?**
- Example: Multi-select tasks → Bulk status update, batch delete, export to CSV
- Example: Batch actions → Select all matching filter, bulk edit properties

**Your task:** Suggest 3-5 creative **frontend enhancements** using ONLY the existing backend endpoints and data fields. Think about what would make the user experience exceptional!

### 2.3 UX Patterns & Design System

What UI patterns would work best for this application?
- Dashboard layout vs. single-page app vs. wizard flow?
- Card-based UI, table view, or list view for main entities?
- Modal dialogs vs. slide-over panels for forms?
- Design system to use (Material UI, Chakra UI, Shadcn, Tailwind, custom)?

**Share your recommendations and reasoning. We'll discuss before finalizing.**

---

## 🏗️ Phase 3: Architecture Planning

Before writing code, let's plan the architecture.

### 3.1 Component Structure

Based on the features we agreed on, outline the main components/screens:

```
Example:
App
├── Layout
│   ├── Header (with user menu)
│   ├── Sidebar (navigation)
│   └── Main content area
├── Pages
│   ├── Dashboard
│   ├── TaskList
│   ├── TaskDetail
│   ├── UserProfile
│   ├── Settings
│   └── 🧪 Playground (REQUIRED - feature showcase/testing page)
└── Shared Components
    ├── TaskCard
    ├── UserAvatar
    ├── StatusBadge
    └── LoadingSpinner
```

**Note:** The Playground page is REQUIRED in every project. It should:
- Be accessible from the main navigation
- Showcase all components, animations, and features
- Use mock data for demonstrations
- Include a toggle to hide in production (e.g., `SHOW_PLAYGROUND` env variable)

### 3.2 State Management Strategy

How should we handle state?
- Local state (useState) for simple components
- Context API for global state (user, theme, etc.)
- React Query / SWR for server state and caching
- Zustand / Redux for complex client state (if needed)

**Recommend an approach based on the application complexity.**

### 3.3 Routing Strategy

What routes do we need? Example:
```
/ - Dashboard
/tasks - Task list
/tasks/:id - Task detail
/tasks/new - Create task
/profile - User profile
/settings - Settings
```

### 3.4 API Integration Plan

How will we connect to the backend?
- Direct fetch calls with TypeScript types from FRONTEND_HANDOFF.md
- API client wrapper (axios, fetch wrapper)
- React Query for caching and optimistic updates
- Error handling strategy (toasts, error boundaries)

**Propose an integration approach.**

---

## 🎯 Phase 4: Iterative Implementation Plan

Now we're ready to build! Let's work **one feature at a time** with your approval at each step.

### 4.1 Implementation Order

I propose we implement in this order:
1. **Setup & Infrastructure** (routing, layout, design system)
2. **Authentication & User Context** (if applicable)
3. **Core Feature 1** (most critical feature from P0)
4. **Core Feature 2**
5. **Core Feature 3**
6. **Feature Playground Page** (P1 - after core features work)
7. **Polish & Refinements**

**Note:** The Playground page should be built AFTER core features are working, so you have actual components and features to showcase.

**Does this order make sense, or should we adjust priorities?**

### 4.2 Development Workflow

For each feature:
1. **I'll describe what to build** (referencing the data models)
2. **You'll create the components** (with proper TypeScript types)
3. **We'll review together** before moving to the next feature
4. **We'll test with mock data first**, then integrate with real API

### 4.3 Data Model Adherence - CRITICAL ⚠️

**ABSOLUTE REQUIREMENT:** All frontend data structures MUST exactly match the TypeScript interfaces provided in FRONTEND_HANDOFF.md.

**DO NOT:**
- Change field names (backend uses `user_id`, not `userId`)
- Add new fields that don't exist in backend
- Change data types (if backend returns `string`, frontend expects `string`)
- Modify enum values

**DO:**
- Use the exact TypeScript interfaces from FRONTEND_HANDOFF.md
- Validate responses match expected shape
- Handle all fields, including optional ones
- Use proper types for dates, enums, and relationships

**Before generating any API-connected component, confirm:**
1. Which endpoint you're calling
2. Which TypeScript interface you're using
3. That the interface matches the backend exactly

---

## 🛠️ Development Guidelines

### Mock Data During Development

**Start with mock data** from the `mock-data/` directory:
```typescript
// Example: Using mock data during development
import mockUsers from './mock-data/users.json';

// Later, swap for API call
const users = await fetch('/api/v1/users').then(r => r.json());
```

### TypeScript Types

**Use the interfaces from FRONTEND_HANDOFF.md exactly as provided:**
```typescript
// ✅ Correct - Using provided interface
interface Task {
  id: number;
  title: string;
  status: "todo" | "in_progress" | "done";
  user_id: number;
  created_at: string;
}

// ❌ Wrong - Modified interface
interface Task {
  id: number;
  title: string;
  status: string;  // Lost type safety
  userId: number;  // Changed field name
  createdAt: Date; // Changed type
}
```

### Error Handling

Handle common scenarios:
- Network errors
- Authentication failures
- Validation errors from backend
- 404 / 500 responses

### Loading & Empty States

Design for:
- Loading spinners during API calls
- Empty states when no data
- Error states when requests fail
- Skeleton loaders for better UX

---

## ✅ Quality Checklist

Before marking a feature "complete", ensure:

- [ ] Component uses correct TypeScript interfaces from FRONTEND_HANDOFF.md
- [ ] API integration tested with real backend (or mock data)
- [ ] Error states handled gracefully
- [ ] Loading states implemented
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility basics (semantic HTML, ARIA labels, keyboard navigation)
- [ ] Code is clean and well-commented
- [ ] No console errors or warnings

---

## 🤝 Collaboration Protocol

### When I say "Review Phase 1"
You should:
- Stop and provide your understanding summary
- Wait for my confirmation before proceeding

### When I say "Let's brainstorm Feature X"
You should:
- Review relevant data models
- Suggest multiple approaches
- Explain trade-offs
- Wait for my decision

### When I say "Build Component X"
You should:
- Confirm which TypeScript interface to use
- Show me the component structure first
- Generate code after I approve
- Explain any important decisions

### When I say "This doesn't match the backend"
You should:
- Review FRONTEND_HANDOFF.md for correct interface
- Identify the mismatch
- Fix to match backend exactly
- Apologize for the confusion 😊

---

## 📝 Summary

**Our Process:**
1. ✅ Review documentation (understand domain, data models, APIs)
2. ✅ Brainstorm features (core + enhancements using existing backend)
3. ✅ Plan architecture (components, state, routing, API integration)
4. ✅ Build iteratively (one feature at a time, with approval)
5. ✅ Test thoroughly (mock data → real API)

**Key Principles:**
- **Collaborative**: We decide together, you don't build autonomously
- **Data Model Compliance**: 100% match with backend schemas
- **User-Centered**: Focus on great UX using available backend features
- **Iterative**: Build incrementally, review frequently
- **Quality**: Proper TypeScript, error handling, responsive design

---

## 🚦 Ready to Start?

**Your first task:** Review the handoff documentation and complete **Phase 1: Review & Understanding**.

Share your findings, and we'll proceed to brainstorming together!

---

## 📚 Reference Files

- **APP_OVERVIEW.md** - Business requirements and user workflows
- **FRONTEND_HANDOFF.md** - TypeScript interfaces, API endpoints, integration guide
- **mock-data/** - Realistic sample data matching backend schemas
- **openapi.json** - Machine-readable API specification

**Questions?** Ask me anytime. Let's build something great! 🚀
