# [Project Name] - Application Overview

> **For Frontend Developers:** This document provides business context and user workflows for building the UI. For technical API details, see `FRONTEND_HANDOFF.md` and `openapi.json`.

## Purpose

[What problem does this application solve? Who is it for? Extract from app_spec.txt overview section.]

## User Roles & Permissions

### Admin
**Capabilities:**
- [Extract admin permissions from app_spec.txt business rules]
- Full system access
- User management
- System configuration

### Manager
**Capabilities:**
- [Extract manager permissions from app_spec.txt business rules]
- Team oversight
- Resource management

### User
**Capabilities:**
- [Extract user permissions from app_spec.txt business rules]
- Basic operations
- Personal data management

[Add additional roles as defined in the spec]

---

## Core User Workflows

### 1. [Workflow Name - e.g., "Task Creation & Assignment"]

**User Role:** [Manager/Admin/User]
**Goal:** [What the user wants to accomplish]

**Steps:**
1. [User action - e.g., "User logs in and navigates to dashboard"]
2. [User action - e.g., "Clicks 'Create Task' button"]
3. [User action - e.g., "Fills in task details (title, description, priority)"]
4. [User action - e.g., "Assigns task to team member from dropdown"]
5. [User action - e.g., "Submits form"]

**Success Criteria:** [What indicates successful completion - e.g., "Task appears in assignee's task list with 'pending' status"]

**Error Cases:**
- [Potential error and how to handle - e.g., "Cannot assign to inactive user - show validation error"]
- [Another error case]

[Repeat for 5-10 key workflows covering main use cases]

---

## Suggested Screens/Views

### Public Screens

#### Login Page
**Purpose:** Authenticate users to access the system
**Key Elements:**
- Email/username input field
- Password input field
- "Remember me" checkbox
- "Login" button
- "Forgot password?" link
**Navigation:** After login → Dashboard (role-specific)

#### Registration Page (if enabled)
**Purpose:** Allow new users to create accounts
**Key Elements:**
- Registration form (email, name, password)
- Terms acceptance checkbox
- "Create Account" button
**Navigation:** After registration → Email verification or Dashboard

### User Screens

#### Dashboard / Home
**Purpose:** Overview of user's assigned tasks and quick actions
**Shows:**
- Summary statistics (total tasks, pending, in progress, completed)
- Recently assigned tasks list
- Overdue tasks alert
- Quick action buttons
**Actions:**
- Click task to view details
- Filter by status
- Create new task (if permitted)
**Navigation:** Links to Task List, Profile Settings

#### Task List
**Purpose:** Filterable, sortable list of all user's tasks
**Shows:**
- Task title, status badge, priority badge, due date, assignee avatar
- Filter controls (status, priority, date range)
- Sort controls (due date, priority, created date)
- Search bar
**Actions:**
- Click task row to open detail view
- Change status via dropdown
- Bulk select for status updates
**Layout Pattern:** Table or card grid

#### Task Detail
**Purpose:** View and edit a single task with full information
**Shows:**
- Task title (editable if permissions allow)
- Description (editable)
- Status dropdown
- Priority dropdown
- Assignee selector
- Due date picker
- Created/updated timestamps
- Comments thread
- Activity history
**Actions:**
- Edit task fields inline
- Add comments
- Change status
- Reassign task
- Delete task (if permitted)
**Navigation:** Back to Task List

#### Profile Settings
**Purpose:** Manage user's own profile and preferences
**Shows:**
- User avatar
- Name, email (editable)
- Password change form
- Notification preferences
**Actions:**
- Update profile information
- Change password
- Save preferences

### Manager Screens

#### Team Dashboard
**Purpose:** Overview of all team tasks and resource allocation
**Shows:**
- Task distribution by user (chart/graph)
- Status breakdown (pending, in progress, completed)
- Overdue tasks by user
- Team member list with active task counts
- Filter by date range, user, status
**Actions:**
- Click user to see their tasks
- Click task to view details
- Reassign tasks
**Layout Pattern:** Dashboard with charts and lists

#### Task Board (Kanban)
**Purpose:** Visual task management with drag-and-drop
**Shows:**
- Columns for each status (Pending, In Progress, Completed)
- Task cards with title, assignee, priority, due date
**Actions:**
- Drag tasks between columns to change status
- Click card to open detail view
- Filter by assignee, priority, date
**Layout Pattern:** Kanban board

#### Create/Edit Task Form
**Purpose:** Form to create new tasks or edit existing ones
**Shows:**
- Title input
- Description textarea
- Priority dropdown
- Assignee selector (team members)
- Due date picker
- Tags/labels selector
**Actions:**
- Fill form fields
- Validate input
- Save task
- Cancel and return
**Navigation:** After save → Task List or Task Detail

#### Team Management
**Purpose:** View and manage team members
**Shows:**
- List of team members
- Role badges
- Active/inactive status
- Current task count per user
**Actions:**
- Filter by role or status
- View user details
- (Admin only) Edit user roles, deactivate users

### Admin Screens

#### User Management
**Purpose:** Full CRUD operations for user accounts
**Shows:**
- List of all users (paginated)
- Role, status, created date
- Filter by role, status
- Search by name/email
**Actions:**
- Create new user
- Edit user (name, email, role)
- Deactivate/activate user
- Delete user (if no active tasks)
**Layout Pattern:** Table with action buttons

#### System Settings
**Purpose:** Configure application settings
**Shows:**
- Configuration options
- System preferences
- Integration settings
**Actions:**
- Update settings
- Save changes

---

## Data Relationships & Display Patterns

### Task List View
**Displays:**
- Title (text, bold)
- Status (colored badge - pending: gray, in_progress: blue, completed: green, cancelled: red)
- Priority (icon or badge - urgent: red flag, high: orange, medium: yellow, low: gray)
- Assignee (avatar + name)
- Due date (formatted date, highlighted if overdue in red)
- Tags (colored pills)

**Interactions:**
- Click row → Open task detail
- Hover → Show quick preview
- Drag → Reorder (if sortable)
- Filter → Apply filters to list
- Sort → Change sort order

**Layout Pattern:** Responsive table or card grid

### Task Detail View
**Displays:**
- Full task information (all fields)
- Assigned user card (avatar, name, email, role)
- Creator card (avatar, name, created timestamp)
- Tags list (colored pills, clickable to filter by tag)
- Comments thread (chronological, newest first or last)
- Activity timeline (who did what when)

**Interactions:**
- Edit fields inline (if permitted)
- Add comment (textarea + submit button)
- Change status (dropdown)
- Reassign (user picker)
- Add/remove tags (tag picker)

**Layout Pattern:** Two-column layout (main content + sidebar with metadata)

### User Card (Reusable Component)
**Displays:**
- Avatar (initials or image)
- Name (text)
- Role badge (colored)
- Status indicator (active: green dot, inactive: gray)

**Used In:** Task detail, team dashboard, user list

**Interactions:**
- Click → View user profile or filter by user
- Hover → Show user details tooltip

### Comment Thread
**Displays:**
- Comment content (text, markdown support)
- Author (avatar + name)
- Timestamp (relative time - "2 hours ago")
- Edit/delete buttons (if user's own comment or admin)

**Interactions:**
- Add new comment (textarea at bottom)
- Edit comment (inline editing)
- Delete comment (with confirmation)
- Mention users (@username autocomplete)

**Layout Pattern:** Vertical list, chronological

---

## Navigation Structure

```
├── Dashboard (landing page after login)
│   └── Quick actions, stats, recent tasks
├── Tasks
│   ├── My Tasks (user view)
│   ├── Team Tasks (manager view)
│   ├── Task Board (manager kanban view)
│   └── Task Detail (/:id)
│       └── Comments, activity, edit
├── Team (manager/admin only)
│   ├── Team Dashboard (overview)
│   ├── Team Members (list)
│   └── User Detail (/:id)
├── Admin (admin only)
│   ├── User Management (CRUD)
│   └── System Settings
└── Settings
    └── My Profile
        ├── Account info
        ├── Password change
        └── Preferences
```

**Access Control:**
- **Public:** Login, Registration
- **Authenticated Users:** Dashboard, My Tasks, Task Detail, My Profile
- **Managers:** Team Tasks, Task Board, Team Dashboard, Team Members
- **Admins:** All routes + User Management + System Settings

**Navigation Patterns:**
- Top navigation bar: Logo, main sections (Dashboard, Tasks, Team), user menu
- Sidebar (optional): Secondary navigation within sections
- Breadcrumbs: Show current location (Tasks > Task Detail > #123)
- User menu (top right): Profile, Settings, Logout

---

## Key Features by Priority

### Must Have (MVP)
- [ ] User authentication (login/logout)
- [ ] Task CRUD operations (create, read, update, delete)
- [ ] Task status management (pending → in_progress → completed)
- [ ] Task assignment to users
- [ ] Basic filtering (by status, assignee)
- [ ] Task list view
- [ ] Task detail view
- [ ] User profile view

### Should Have
- [ ] Task priority levels
- [ ] Due date tracking with overdue alerts
- [ ] Comments on tasks
- [ ] Tags/labels for tasks
- [ ] Advanced filtering (date ranges, multiple criteria)
- [ ] Sorting options
- [ ] Search functionality
- [ ] Team dashboard (manager view)
- [ ] Kanban board view

### Nice to Have
- [ ] File attachments on tasks
- [ ] Email notifications
- [ ] Activity timeline/audit log
- [ ] Task templates
- [ ] Bulk operations (bulk status update)
- [ ] Export tasks (CSV, PDF)
- [ ] Advanced analytics and reports
- [ ] Mobile responsive design
- [ ] Dark mode
- [ ] Keyboard shortcuts

---

## Design Considerations

### Information Hierarchy

**Primary Information:**
- Task title and status (most prominent)
- Assignee and due date (secondary)
- Priority indicator (visual cue)

**Secondary Information:**
- Task description (expandable)
- Tags and metadata
- Timestamps

**Tertiary Information:**
- Activity history
- System metadata

### Common UI Patterns

- **Status Badges** - Color-coded pills for task status (pending: gray, in_progress: blue, completed: green)
- **Priority Indicators** - Icons or flags (urgent: red, high: orange, medium: yellow, low: gray)
- **User Avatars** - Circular avatars with initials or profile images
- **Empty States** - Friendly messages when no data (e.g., "No tasks yet. Create your first task!")
- **Loading States** - Skeleton screens or spinners during data fetch
- **Error States** - Clear error messages with suggested actions
- **Confirmation Dialogs** - For destructive actions (delete task, deactivate user)
- **Toast Notifications** - Success/error feedback after actions
- **Dropdown Menus** - For actions (status change, more options)
- **Tooltips** - For icons and condensed information

### Responsive Behavior

**Desktop (1200px+):**
- Full multi-column layouts
- Side-by-side forms and previews
- Expanded navigation
- Data tables with all columns

**Tablet (768px - 1199px):**
- Reduced columns
- Collapsible sidebars
- Stacked forms
- Simplified tables (hide less important columns)

**Mobile (< 768px):**
- Single column layouts
- Card-based task lists (not tables)
- Hamburger menu navigation
- Bottom navigation bar
- Simplified filters (modal overlays)
- Swipe gestures (swipe to complete task)

**Key Mobile Priorities:**
- Quick task status updates
- View task details
- Add comments
- Create simple tasks
- View notifications

---

## Integration with Mock Data

**IMPORTANT:** Use the mock data files in `docs/mock-data/` when designing and building the UI. These files contain realistic sample data that perfectly mirrors the backend data model.

### Mock Data Files Available:
- `users.json` - 20 sample users with various roles
- `tasks.json` - 50 sample tasks with different statuses, priorities, assignments
- `tags.json` - 10 sample tags with colors
- `comments.json` - 30 sample comments on tasks

### Why Use Mock Data:
- ✅ Design and build UI without backend running
- ✅ Data structure matches API responses exactly
- ✅ Includes realistic relationships (tasks → users, comments → tasks)
- ✅ Contains edge cases (overdue tasks, unassigned tasks, etc.)
- ✅ Easy to swap with real API calls later

### How to Use:
See `docs/mock-data/README.md` for detailed usage instructions and code examples.

---

## Next Steps for Frontend Development

1. **Review this document** for business context and user workflows
2. **Read `FRONTEND_HANDOFF.md`** for technical integration details
3. **Import mock data** from `docs/mock-data/` folder
4. **Design screens** based on suggested structure above
5. **Build UI components** using mock data (no backend needed)
6. **Test user workflows** with mock data
7. **Integrate with real API** using `openapi.json` specification when backend is ready
8. **Swap mock data calls** for real API calls (simple toggle in your code)

---

## Questions or Issues?

- **API behavior questions** → Check `/docs` Swagger UI or `openapi.json`
- **Business logic questions** → Review business rules in this document
- **Data structure questions** → See `docs/mock-data/` examples
- **Setup questions** → See `README.md` in project root
