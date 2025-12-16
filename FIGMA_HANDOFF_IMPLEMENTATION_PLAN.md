# Figma Make Handoff Documentation - Implementation Plan

## Overview

This plan outlines the implementation of a comprehensive handoff package that enables Figma Make (or similar agentic UI tools) to build frontends for the generated FastAPI backends. The handoff package will include application context, technical specifications, and perfectly aligned mock data.

## Goals

1. ✅ Generate documentation that gives Figma Make both **business context** and **technical specs**
2. ✅ Create mock data files that **perfectly mirror** backend data models
3. ✅ Provide clear guidance to use mock data during UI design
4. ✅ Automate handoff document generation in the agent workflow
5. ✅ Maintain handoff docs as the API evolves

## The Complete Handoff Package

```
project/
├── docs/
│   ├── APP_OVERVIEW.md           # Business context & user workflows (NEW)
│   ├── FRONTEND_HANDOFF.md       # Technical integration guide (NEW)
│   └── mock-data/
│       ├── README.md             # Mock data usage guide (NEW)
│       ├── users.json            # Sample user records (NEW)
│       ├── tasks.json            # Sample task records (NEW)
│       ├── tags.json             # Sample tag records (NEW)
│       └── comments.json         # Sample comment records (NEW)
└── openapi.json                  # OpenAPI spec (exported from /openapi.json)
```

## Implementation Steps Summary

### Step 1: Enhance app_spec.txt Template
Add sections for user workflows, suggested screens, and feature priorities.

### Step 2: Create Template Files
- APP_OVERVIEW_TEMPLATE.md
- FRONTEND_HANDOFF_TEMPLATE.md
- MOCK_DATA_README_TEMPLATE.md

### Step 3: Update initializer_prompt.md
Add task to generate handoff documentation during initialization.

### Step 4: Update coding_prompt.md
Add step to maintain handoff docs as API evolves.

### Step 5: Update CLAUDE.md
Document the handoff package feature.

### Step 6: Update README.md
Mention handoff documentation in features.

## Files to Create/Modify

### New Files
- `prompts/templates/APP_OVERVIEW_TEMPLATE.md`
- `prompts/templates/FRONTEND_HANDOFF_TEMPLATE.md`
- `prompts/templates/MOCK_DATA_README_TEMPLATE.md`

### Modified Files
- `prompts/app_spec.txt`
- `prompts/initializer_prompt.md`
- `prompts/coding_prompt.md`
- `CLAUDE.md`
- `README.md`

## Next Steps

Ready to implement these changes step by step!
