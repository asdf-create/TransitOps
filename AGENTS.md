# AGENTS.md
# TransitOps Development Instructions
This document contains the mandatory development rules for every coding agent working on this repository.
## Project Goal
Build a showcase-quality offline Smart Transport Operations Platform for macOS.
Primary objective: Win the hackathon.
Secondary objective: Release a production-quality open-source portfolio project.
All code should prioritize:
- Simplicity
- Readability
- Maintainability
- Native performance
- Beautiful UI
- Enterprise architecture
- Minimal dependencies
Follow Ponytail principles whenever possible.
---
# Technology Stack
## Desktop
Tauri v2
## Frontend
- TanStack Start
- React
- TypeScript
- Bun
- TailwindCSS
- shadcn/ui
## Backend
- FastAPI
- Python 3.12+
- uv
- SQLModel
- SQLite
## AI
llama.cpp
## ML
- LightGBM
- XGBoost
- Scikit-Learn
## Maps
MapLibre GL JS
## Charts
Apache ECharts
---
# General Rules
Never rewrite an entire file unless absolutely necessary.
Prefer modifying existing code.
Preserve existing architecture.
Keep implementations simple.
Avoid overengineering.
Avoid unnecessary abstractions.
Avoid unnecessary dependencies.
Prefer standard library whenever practical.
Follow feature-based architecture.
Never duplicate business logic.
Never leave dead code.
Remove unused imports.
Never hardcode secrets.
Never hardcode file paths.
Never commit generated artifacts unless explicitly required.
---
# File Size
Target maximum:
- Python: 400 lines
- TypeScript: 400 lines
If a file exceeds this, split it into smaller modules.
---
# Function Size
Target:
< 50 lines
If longer, consider extracting helper functions.
---
# Class Design
Prefer composition.
Avoid inheritance unless there is a clear benefit.
Avoid God classes.
Single Responsibility Principle should guide design without introducing unnecessary complexity.
---
# Architecture Rules
Routes should:
- Validate input
- Call services
- Return responses
Routes must not contain business logic.
Business logic belongs inside services.
Database access belongs inside repositories.
SQLModel models must not contain business logic.
---
# Database Rules
Always use SQLModel.
Avoid raw SQL.
Use transactions where appropriate.
Create indexes for frequently queried fields.
Never bypass repositories.
---
# Business Rules
Every mandatory business rule from the hackathon must be enforced by the backend.
Additional enterprise rules must also be enforced.
Backend validation is the source of truth.
Never rely on frontend validation alone.
---
# API Rules
REST only.
Consistent JSON responses.
Proper HTTP status codes.
Meaningful error messages.
Never expose stack traces.
---
# Frontend Rules
Use shadcn components whenever possible.
Avoid creating custom components if a high-quality community component already exists.
Prefer composition over deeply nested component trees.
Maintain consistent spacing.
Maintain consistent typography.
Support dark mode.
Animations should enhance usability, not distract.
---
# UI Design
Design language:
Apple-inspired + Modern AI dashboard.
Use:
- Glass effects where appropriate
- Smooth animations
- Rounded corners
- Consistent spacing
- Large whitespace
- Beautiful empty states
- Skeleton loading
- Animated transitions
Avoid excessive gradients.
Avoid flashy neon effects.
Professional appearance takes priority.
---
# Component Libraries
Preferred order:
1. shadcn/ui
2. shadcn Blocks
3. Origin UI
4. Motion Primitives
5. Magic UI
6. ReactBits
7. Aceternity UI (only if necessary)
Avoid introducing another UI library without justification.
---
# Icons
Primary:
HugeIcons
Fallback:
Lucide
---
# Maps
Always use:
MapLibre GL JS
Never use Google Maps.
Use OpenStreetMap.
Vehicle movement should interpolate smoothly along route geometry.
---
# Charts
Always use Apache ECharts.
Charts should support:
- Zoom
- Tooltips
- Animations
- Export
Dashboard should feel interactive.
---
# AI
Use llama.cpp.
Inference only.
No online APIs.
Keep prompts modular.
Future model replacement should require minimal code changes.
---
# Machine Learning
Models are trained before deployment.
Application performs inference only.
Keep preprocessing identical to training pipeline.
Never retrain during normal application usage.
---
# Logging
Use centralized logging.
No print() debugging.
Log meaningful events.
Do not log sensitive information.
---
# Error Handling
Never silently ignore exceptions.
Return actionable errors.
Provide fallback behavior where appropriate.
---
# Testing
Every feature must include tests.
Test:
- Happy paths
- Invalid inputs
- Edge cases
- Permission checks
- Business rules
- Regression cases
Backend modules should include approximately 15–20 meaningful tests where practical.
Tests must pass before marking a task complete.
---
# Git
Commit frequently.
Small commits.
Descriptive commit messages.
Examples:
feat(tracking): add live vehicle interpolation
fix(dispatch): prevent assigning suspended drivers
Avoid generic commit messages.
---
# Documentation
Whenever a feature is completed:
- Update TASK.md
- Update relevant documentation
- Update README if user-visible behavior changes
Never leave documentation outdated.
---
# Performance
Optimize for clarity first.
Then optimize hotspots.
Avoid premature optimization.
Application should remain responsive with:
- 500 vehicles
- 2,000 trips
- Live tracking
- Analytics dashboard
---
# Completion Criteria
A task is complete only when:
- Feature implemented
- UI polished
- Animations complete
- Business rules enforced
- Tests written
- Tests passing
- Documentation updated
- No lint errors
- No unused imports
- No duplicated logic
- Git commit created
Do not consider partially implemented features complete.