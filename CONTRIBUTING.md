
# CONTRIBUTING.md
# Contributing to TransitOps
Thank you for your interest in contributing to TransitOps.
This project was originally developed as a hackathon submission but is intended to grow into a polished, open-source desktop application for intelligent fleet management.
Please read this guide before making contributions.
---
# Project Goals
Every contribution should support one or more of the following goals:
* Improve code quality
* Improve user experience
* Improve maintainability
* Improve documentation
* Improve performance
* Improve accessibility
* Improve testing
* Fix bugs
Do not add unnecessary complexity.
---
# Before You Start
Please read the following documents before contributing:
* README.md
* AGENTS.md
* TASK.md
* ARCHITECTURE.md
* DATABASE.md
* API.md
* UI_UX.md
* ML_AI.md
* TESTING.md
These documents define the project architecture and coding standards.
---
# Technology Stack
## Desktop
* Tauri v2
## Frontend
* React
* TanStack Start
* TypeScript
* Bun
* Tailwind CSS
* shadcn/ui
## Backend
* FastAPI
* Python
* uv
* SQLModel
## Database
* SQLite
## AI
* llama.cpp
## Machine Learning
* Scikit-Learn
* LightGBM
* XGBoost
---
# Development Setup
## Clone the Repository
```bash
git clone <repository-url>
cd TransitOps
```
## Backend
```bash
cd backend
uv sync
uv run main.py
```
## Frontend
```bash
cd frontend
bun install
bun run dev
```
## Desktop
```bash
bun run tauri dev
```
---
# Branch Naming
Create a separate branch for every feature.
Examples:
```text
feature/dashboard
feature/tracking
feature/ml
feature/analytics
feature/maintenance
feature/notifications
fix/login
fix/tracking
docs/readme
refactor/database
```
Avoid committing directly to `main`.
---
# Commit Messages
Use Conventional Commits.
Examples:
```text
feat(dispatch): implement trip assignment
feat(ai): add offline assistant
feat(analytics): add fleet utilization dashboard
fix(vehicle): prevent duplicate registrations
fix(auth): validate password length
refactor(database): extract repository layer
docs(api): update endpoint documentation
test(trips): add dispatch edge case coverage
```
Avoid generic messages such as:
* Update
* Fix
* Changes
* Final
* Misc
---
# Pull Requests
Each pull request should:
* Solve one problem
* Be easy to review
* Include tests
* Update documentation if needed
Do not combine unrelated features into a single pull request.
---
# Coding Standards
General principles:
* Keep code readable.
* Prefer simplicity.
* Avoid premature optimization.
* Avoid unnecessary dependencies.
* Follow existing project structure.
* Keep functions focused.
* Remove dead code.
* Remove unused imports.
Business logic belongs in services.
Database access belongs in repositories.
Routes should remain thin.
---
# File Size Guidelines
Recommended maximums:
* Python: 400 lines
* TypeScript: 400 lines
If a file grows beyond this, consider splitting it into smaller modules.
---
# Code Style
Prefer:
* Small functions
* Clear naming
* Early returns
* Composition over inheritance
* Immutable data where practical
Avoid:
* Deep nesting
* Duplicate logic
* Magic numbers
* Large classes
* Global mutable state
---
# Frontend Guidelines
Use existing components whenever possible.
Preferred libraries:
1. shadcn/ui
2. shadcn Blocks
3. Origin UI
4. Motion Primitives
5. Magic UI
6. ReactBits
Maintain a consistent visual style throughout the application.
---
# Backend Guidelines
Use:
* FastAPI
* SQLModel
* Repository pattern
* Service layer
* Dependency injection where appropriate
Never:
* Execute raw SQL unless necessary
* Place business logic in routes
* Access SQLite directly from the frontend
---
# Testing Requirements
Every new feature should include appropriate tests.
Test:
* Normal behavior
* Invalid inputs
* Business rules
* Permission checks
* Edge cases
* Regression scenarios
Run all tests before opening a pull request.
---
# Documentation
Update documentation whenever you:
* Add features
* Change APIs
* Modify the database
* Introduce new business rules
* Change architecture
Documentation should never become outdated.
---
# Performance
Keep the application responsive with the demo dataset:
* 500 vehicles
* 100 drivers
* 2,000 trips
* 5,000 fuel logs
Avoid introducing unnecessary performance regressions.
---
# Security
Never commit:
* API keys
* Passwords
* Secrets
* Tokens
* Local configuration
* Personal information
Use environment variables where appropriate.
---
# Issue Reporting
When reporting a bug, include:
* Description
* Expected behavior
* Actual behavior
* Steps to reproduce
* Operating system
* Screenshots (if applicable)
* Logs (if available)
---
# Feature Requests
Feature requests should include:
* Problem statement
* Proposed solution
* Expected benefit
* Possible alternatives
Keep requests focused and actionable.
---
# Project Principles
TransitOps values:
* Simplicity
* Maintainability
* Performance
* Readability
* Accessibility
* Offline-first functionality
* High-quality documentation
* Thorough testing
If a contribution conflicts with these principles, it is unlikely to be accepted.
---
# Contributor Checklist
Before submitting a pull request, verify:
* [ ] Code follows project architecture
* [ ] Business rules implemented correctly
* [ ] Tests added
* [ ] Tests passing
* [ ] Documentation updated
* [ ] No linting errors
* [ ] No unused imports
* [ ] No dead code
* [ ] Commit messages follow Conventional Commits
* [ ] Feature has been manually verified
Thank you for contributing to TransitOps!