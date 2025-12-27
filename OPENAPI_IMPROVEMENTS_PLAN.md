# OpenAPI Specification Improvements - Implementation Plan

**Created:** 2025-12-27
**Status:** Planning
**Approach:** Option A (Prompt Updates) + Option B (Validation)

---

## Overview

After generating the first real project, we identified critical OpenAPI specification improvements needed in the generated FastAPI backends. This plan outlines how to incorporate these best practices into the harness.

**Source:** `temp/temp.md` - Analysis of generated OpenAPI spec issues

---

## Implementation Strategy

### Phase 1: Update Initializer Prompt ✅ Quick Wins
Update `prompts/initializer_prompt.md` to teach the agent OpenAPI best practices from the start.

### Phase 2: Add OpenAPI Validator 🔍 Enforcement
Create validation logic to programmatically check generated specs and provide feedback.

---

## Changes Breakdown

### 1. Authentication Security Schemes (HIGH PRIORITY)

**Problem:**
```json
// Current - Suboptimal
{
  "parameters": [
    {
      "name": "authorization",
      "in": "header",
      "required": false,
      "schema": { "type": "string" }
    }
  ]
}
```

**Solution:**
```json
// Target - Best Practice
{
  "components": {
    "securitySchemes": {
      "bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    }
  },
  "security": [{ "bearerAuth": [] }],
  "paths": {
    "/api/v1/health": {
      "get": {
        "security": []  // Explicitly unauthenticated
      }
    }
  }
}
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add security scheme setup instructions
- `prompts/coding_prompt.md` - Reference security in endpoint creation

**Prompt Changes:**
```markdown
## Authentication Setup

Create a proper security scheme in your FastAPI app:

1. Define security scheme in OpenAPI components:
   - Type: HTTP Bearer (JWT)
   - Use FastAPI's `HTTPBearer` dependency

2. Apply security globally or per-endpoint:
   - Secured endpoints: Include `dependencies=[Depends(get_current_user)]`
   - Public endpoints: Explicitly mark with empty security in OpenAPI

3. Document in generated openapi.json:
   - Add `components.securitySchemes.bearerAuth`
   - Apply `security: [{ bearerAuth: [] }]` to secured endpoints
   - Apply `security: []` to public endpoints (/health, /docs)
```

---

### 2. Add Servers Configuration (HIGH PRIORITY)

**Problem:**
```json
// Current - Missing
{
  "openapi": "3.1.0",
  "info": { ... },
  "paths": { ... }
}
```

**Solution:**
```json
// Target
{
  "openapi": "3.1.0",
  "servers": [
    {
      "url": "http://localhost:8000",
      "description": "Development server"
    },
    {
      "url": "https://staging.example.com",
      "description": "Staging environment"
    },
    {
      "url": "https://api.example.com",
      "description": "Production environment"
    }
  ]
}
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add servers configuration

**Prompt Changes:**
```markdown
## OpenAPI Servers Configuration

Configure multiple server environments in your FastAPI app:

1. Add servers to the FastAPI app initialization:
   ```python
   app = FastAPI(
       title="Your API",
       version="1.0.0",
       servers=[
           {"url": "http://localhost:8000", "description": "Development"},
           {"url": "https://staging.example.com", "description": "Staging"},
           {"url": "https://api.example.com", "description": "Production"},
       ]
   )
   ```

2. This helps with:
   - Postman/Insomnia imports
   - SDK generation with correct base URLs
   - Documentation clarity
```

---

### 3. Eliminate Empty Response Schemas (HIGH PRIORITY)

**Problem:**
```json
// Current - Meaningless
{
  "responses": {
    "200": {
      "description": "Successful Response",
      "content": {
        "application/json": {
          "schema": {}  // ❌ Unknown shape
        }
      }
    }
  }
}
```

**Solution:**
```json
// Option 1: Define proper schema
{
  "responses": {
    "200": {
      "description": "Health check successful",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/HealthResponse"
          }
        }
      }
    }
  }
}

// Option 2: Use 204 No Content (no body)
{
  "responses": {
    "204": {
      "description": "Action completed successfully"
    }
  }
}
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add response schema guidelines
- `prompts/coding_prompt.md` - Enforce in endpoint creation

**Prompt Changes:**
```markdown
## Response Schema Guidelines

NEVER return `"schema": {}` in OpenAPI responses. Always:

1. **For endpoints with data:** Define explicit Pydantic response models
   ```python
   class HealthResponse(BaseModel):
       status: str
       version: str
       uptime: float

   @router.get("/health", response_model=HealthResponse)
   def health_check():
       return {"status": "ok", "version": "1.0.0", "uptime": 123.45}
   ```

2. **For endpoints without data:** Use `status_code=204` (No Content)
   ```python
   @router.delete("/users/{id}", status_code=204)
   def delete_user(id: int):
       # Perform deletion
       return Response(status_code=204)
   ```

3. **For simple confirmations:** Use a standard response model
   ```python
   class MessageResponse(BaseModel):
       message: str

   @router.post("/action", response_model=MessageResponse)
   def perform_action():
       return {"message": "Action completed successfully"}
   ```
```

---

### 4. Standardized Error Responses (HIGH PRIORITY)

**Problem:**
- Only 422 Validation Error is consistently defined
- Missing 401/403/404/409/429 response schemas
- Inconsistent error formats

**Solution:**
```python
# Standard error schema
class ErrorResponse(BaseModel):
    """Standardized error response"""
    code: str  # Error code (e.g., "UNAUTHORIZED", "NOT_FOUND")
    message: str  # Human-readable message
    details: dict | None = None  # Additional context
    request_id: str | None = None  # For tracing

# HTTP status code mapping
ERROR_RESPONSES = {
    401: {"model": ErrorResponse, "description": "Unauthorized - Missing or invalid authentication"},
    403: {"model": ErrorResponse, "description": "Forbidden - Insufficient permissions"},
    404: {"model": ErrorResponse, "description": "Not Found - Resource does not exist"},
    409: {"model": ErrorResponse, "description": "Conflict - Resource already exists or constraint violation"},
    422: {"model": ErrorResponse, "description": "Validation Error - Invalid request data"},
    429: {"model": ErrorResponse, "description": "Too Many Requests - Rate limit exceeded"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
}
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add error response setup
- `prompts/coding_prompt.md` - Use consistent errors in endpoints

**Prompt Changes:**
```markdown
## Standardized Error Handling

Create a common error response model and use it consistently:

1. **Define ErrorResponse schema** (in `app/schemas/common.py` or `app/schemas/error.py`):
   ```python
   from pydantic import BaseModel

   class ErrorResponse(BaseModel):
       code: str
       message: str
       details: dict | None = None
       request_id: str | None = None
   ```

2. **Define common HTTP error responses** that can be reused:
   ```python
   COMMON_RESPONSES = {
       401: {"model": ErrorResponse, "description": "Unauthorized"},
       403: {"model": ErrorResponse, "description": "Forbidden"},
       404: {"model": ErrorResponse, "description": "Not Found"},
       409: {"model": ErrorResponse, "description": "Conflict"},
       422: {"model": ErrorResponse, "description": "Validation Error"},
       429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
   }
   ```

3. **Apply to endpoints** based on their behavior:
   ```python
   @router.post(
       "/users",
       response_model=UserResponse,
       status_code=201,
       responses={
           409: COMMON_RESPONSES[409],  # Duplicate email
           422: COMMON_RESPONSES[422],  # Invalid data
       }
   )
   ```

4. **Raise consistent HTTP exceptions**:
   ```python
   from fastapi import HTTPException

   # 404 Not Found
   raise HTTPException(
       status_code=404,
       detail={"code": "USER_NOT_FOUND", "message": "User not found"}
   )

   # 409 Conflict
   raise HTTPException(
       status_code=409,
       detail={"code": "EMAIL_EXISTS", "message": "Email already registered"}
   )
   ```

5. **Use in feature_list.json test cases**:
   - Specify expected error codes in test cases
   - Include both status code and error response structure
```

---

### 5. Path Consistency - Trailing Slashes (MEDIUM PRIORITY)

**Problem:**
```
/api/v1/users      ✅
/api/v1/blocks/    ❌ Inconsistent trailing slash
/api/v1/reports/   ❌ Inconsistent trailing slash
```

**Solution:**
- Pick one convention: **No trailing slashes** (FastAPI default)
- Enforce consistently across all endpoints

**Files to Update:**
- `prompts/initializer_prompt.md` - Add path naming convention
- `prompts/coding_prompt.md` - Reinforce convention

**Prompt Changes:**
```markdown
## API Path Conventions

Follow these path naming rules consistently:

1. **NO trailing slashes**: `/api/v1/users` not `/api/v1/users/`
2. **Lowercase with hyphens**: `/api/v1/user-profiles` not `/api/v1/userProfiles`
3. **Plural nouns for resources**: `/api/v1/users` not `/api/v1/user`
4. **Use IDs in path for single resources**: `/api/v1/users/{id}`
5. **Use action verbs for non-CRUD operations**: `/api/v1/users/{id}/activate`

FastAPI treats `/users` and `/users/` as different routes, which can cause client confusion.
```

---

### 6. OperationId Naming (MEDIUM PRIORITY)

**Problem:**
```
get_current_user_profile_api_v1_me_get  ❌ Auto-generated, verbose
```

**Solution:**
```
getCurrentUser  ✅ Human-readable, stable
updateCurrentUser
listPractices
createPractice
```

**Files to Update:**
- `prompts/coding_prompt.md` - Add operationId guidelines

**Prompt Changes:**
```markdown
## OpenAPI OperationId Naming

Provide explicit, stable operation IDs for better SDK generation:

```python
@router.get(
    "/users/me",
    response_model=UserResponse,
    operation_id="getCurrentUser",  # ✅ Explicit, readable
)
def get_current_user():
    ...

@router.put(
    "/users/me",
    response_model=UserResponse,
    operation_id="updateCurrentUser",
)
def update_current_user():
    ...
```

**Naming Pattern:**
- `{verb}{Resource}` for single items: `getUser`, `updateUser`, `deleteUser`
- `{verb}{PluralResource}` for collections: `listUsers`, `createUser`
- `{verb}{Resource}{Action}` for actions: `activateUser`, `resetUserPassword`

**Benefits:**
- Stable across refactors (changing function names won't break generated clients)
- Cleaner generated SDK method names
- Easier to reference in documentation
```

---

### 7. Pagination Metadata Consistency (MEDIUM PRIORITY)

**Problem:**
- Some endpoints return `count` and `total`
- Others return only `count`
- Inconsistent query parameters (`limit`/`offset` vs missing)

**Solution:**
```python
# Standard pagination request
class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

# Standard pagination response
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int  # Total items available
    limit: int  # Requested limit
    offset: int  # Requested offset
    count: int  # Items in this response (len(items))
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add pagination pattern

**Prompt Changes:**
```markdown
## Pagination Pattern

For all list endpoints, use consistent pagination:

1. **Define reusable pagination schema** (`app/schemas/common.py`):
   ```python
   from typing import Generic, TypeVar
   from pydantic import BaseModel, Field

   T = TypeVar('T')

   class PaginatedResponse(BaseModel, Generic[T]):
       items: list[T]
       total: int  # Total count in database
       limit: int  # Requested page size
       offset: int  # Starting position
       count: int  # Actual items returned (len(items))
   ```

2. **Use in endpoints**:
   ```python
   @router.get("/users", response_model=PaginatedResponse[UserResponse])
   def list_users(
       limit: int = Query(default=20, ge=1, le=100),
       offset: int = Query(default=0, ge=0),
   ):
       total = db.query(User).count()
       users = db.query(User).offset(offset).limit(limit).all()

       return {
           "items": users,
           "total": total,
           "limit": limit,
           "offset": offset,
           "count": len(users),
       }
   ```

3. **For cursor-based pagination** (optional, for high-scale lists):
   ```python
   class CursorPaginatedResponse(BaseModel, Generic[T]):
       items: list[T]
       next_cursor: str | None  # Opaque token for next page
       has_more: bool
   ```
```

---

### 8. Privacy & Security Schema Tightening (HIGH PRIORITY)

**Problem:**
- `BuddyCard.candidate_id` exposes real user IDs (conflicts with "NO unique identifiers" claim)
- `UserResponse.privacy_settings` is `additionalProperties: true` (untyped)

**Solution:**
```python
# Option 1: Use opaque tokens instead of real IDs
class BuddyCard(BaseModel):
    card_id: str  # Opaque UUID, not the real user ID
    candidate_token: str  # Temporary token for actions
    # ... other fields

# Option 2: Explicit privacy settings schema
class PrivacySettings(BaseModel):
    profile_visible: bool = True
    show_location: bool = True
    allow_discovery: bool = True
    show_online_status: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    privacy_settings: PrivacySettings  # ✅ Strongly typed
```

**Files to Update:**
- `prompts/initializer_prompt.md` - Add privacy/security guidelines
- `prompts/coding_prompt.md` - Reinforce in endpoint development

**Prompt Changes:**
```markdown
## Privacy & Security Best Practices

1. **Never expose internal IDs in anonymous/discovery contexts**:
   - Use opaque tokens (UUIDs) instead of database IDs
   - Generate temporary tokens that expire

   ```python
   # ❌ Bad: Exposes real user ID
   class BuddyCard(BaseModel):
       candidate_id: int

   # ✅ Good: Uses opaque token
   class BuddyCard(BaseModel):
       card_token: str  # UUID that maps to user internally
   ```

2. **Strongly type all user-facing schemas**:
   - Never use `dict` or `additionalProperties: true` for structured data
   - Define explicit Pydantic models

   ```python
   # ❌ Bad: Untyped settings
   class UserResponse(BaseModel):
       privacy_settings: dict

   # ✅ Good: Explicit schema
   class PrivacySettings(BaseModel):
       profile_visible: bool = True
       show_location: bool = True

   class UserResponse(BaseModel):
       privacy_settings: PrivacySettings
   ```

3. **Separate internal and external schemas**:
   - Use different schemas for database models vs API responses
   - Never directly return ORM models in responses
```

---

### 9. Nullable Pattern Consistency (LOW PRIORITY)

**Problem:**
Current use of `anyOf` is correct for OpenAPI 3.1, but need to ensure consistency.

**Solution:**
Ensure all nullable fields consistently use:
```json
{
  "anyOf": [
    {"type": "string"},
    {"type": "null"}
  ]
}
```

**Files to Update:**
- `prompts/coding_prompt.md` - Add nullable field guidance

**Prompt Changes:**
```markdown
## Nullable Fields in Pydantic

Use consistent patterns for optional/nullable fields:

```python
from pydantic import BaseModel

class User(BaseModel):
    # Required field
    email: str

    # Optional (can be omitted from request, defaults to None)
    middle_name: str | None = None

    # Optional with default value
    role: str = "user"

    # Optional in OpenAPI 3.1 (generates anyOf pattern)
    bio: str | None = None
```

This generates proper OpenAPI 3.1 nullable syntax automatically.
```

---

## Implementation Steps

### Step 1: Update `prompts/initializer_prompt.md`

Add new sections:
- [ ] Authentication Security Schemes
- [ ] Servers Configuration
- [ ] Response Schema Guidelines
- [ ] Standardized Error Handling
- [ ] API Path Conventions
- [ ] Pagination Pattern
- [ ] Privacy & Security Best Practices

### Step 2: Update `prompts/coding_prompt.md`

Add reminders:
- [ ] Reference security in endpoint creation
- [ ] Reinforce error response usage
- [ ] Reinforce path conventions
- [ ] Add operationId naming guidelines
- [ ] Add nullable field guidance

### Step 3: Create OpenAPI Validator (Optional - Phase 2)

Create `openapi_validator.py`:
- [ ] Check for proper security schemes
- [ ] Validate servers configuration
- [ ] Detect empty response schemas
- [ ] Verify error response consistency
- [ ] Check path trailing slashes
- [ ] Validate operationId naming pattern
- [ ] Check pagination response structure

### Step 4: Update Templates (if needed)

Check if any templates in `prompts/templates/` need updates:
- [ ] Review `FRONTEND_HANDOFF_TEMPLATE.md`
- [ ] Review `FIGMA_MAKE_PROMPT_TEMPLATE.md`
- [ ] Update if they reference OpenAPI structures

### Step 5: Test with New Generation

- [ ] Create a test project with updated prompts
- [ ] Verify OpenAPI spec includes all improvements
- [ ] Check generated FastAPI code quality
- [ ] Validate error responses work correctly
- [ ] Test pagination endpoints

---

## Validation Criteria

A generated project passes if the OpenAPI spec includes:

1. ✅ `components.securitySchemes.bearerAuth` defined
2. ✅ `servers` array with at least dev/staging/prod
3. ✅ No `"schema": {}` in responses (all typed or 204)
4. ✅ `ErrorResponse` schema defined
5. ✅ Common error responses (401/403/404/409/422/429) documented
6. ✅ No trailing slashes on paths
7. ✅ Human-readable `operationId` on all operations
8. ✅ Consistent pagination response structure
9. ✅ Privacy-sensitive fields use opaque tokens
10. ✅ All user-facing schemas are strongly typed

---

## Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| `prompts/initializer_prompt.md` | Add all 9 improvement sections | HIGH |
| `prompts/coding_prompt.md` | Add reinforcement reminders | HIGH |
| `openapi_validator.py` (new) | Create validation script | MEDIUM |
| `autonomous_agent_demo.py` | Add optional validation step | LOW |
| `CLAUDE.md` | Document new OpenAPI standards | LOW |

---

## Success Metrics

**Before:**
- Empty response schemas
- Authentication as optional headers
- No servers configuration
- Only 422 errors defined
- Inconsistent paths
- Auto-generated operation IDs

**After:**
- Fully typed responses
- Proper security schemes
- Multi-environment servers
- Complete error catalog (401/403/404/409/422/429)
- Consistent path naming
- Human-readable operation IDs
- Complete, production-ready OpenAPI 3.1 specs

---

## Next Steps

1. Review this plan
2. Make any adjustments needed
3. Start with Phase 1: Update prompts
4. Test with a sample generation
5. Iterate based on results
6. Optionally implement Phase 2: Validator

---

**Status:** Ready for implementation
