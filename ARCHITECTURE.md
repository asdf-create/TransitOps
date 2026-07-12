# ARCHITECTURE.md
# TransitOps Architecture Specification
Version: 1.0
## Overview
TransitOps follows a modular, feature-based architecture. The application is designed to be offline-first, highly maintainable, AI-friendly, and easy for multiple coding agents to contribute to without causing merge conflicts.
The architecture emphasizes:
* Clear separation of responsibilities
* Thin API routes
* Centralized business logic
* Minimal dependencies
* Feature isolation
* Future extensibility
---
# High-Level Architecture
```text
┌──────────────────────────────┐
│        Tauri Desktop         │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│   TanStack Start + React UI  │
└──────────────┬───────────────┘
               │ HTTP
┌──────────────▼───────────────┐
│        FastAPI Backend       │
└──────────────┬───────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼─────┐     ┌─────▼─────┐
│  Services │     │ AI / ML   │
└─────┬─────┘     └─────┬─────┘
      │                 │
┌─────▼─────────────────▼─────┐
│       Repository Layer       │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ SQLModel + SQLite Database   │
└──────────────────────────────┘
```
---
# Architectural Principles
1. Feature-based organization.
2. Thin API routes.
3. Business logic inside services.
4. Repository layer owns database access.
5. SQLModel only represents data.
6. UI never communicates directly with SQLite.
7. AI and ML are isolated modules.
8. Every feature should be independently testable.
---
# Repository Structure
```text
TransitOps/
│
├── backend/
├── frontend/
├── database/
├── models/
├── scripts/
├── docs/
├── assets/
│
├── TASK.md
├── AGENTS.md
├── ARCHITECTURE.md
├── DATABASE.md
├── API.md
├── UI_UX.md
├── ML_AI.md
├── TESTING.md
├── RELEASE.md
├── README.md
└── LICENSE
```
---
# Backend Structure
```text
backend/
│
├── auth/
├── dashboard/
├── vehicles/
├── drivers/
├── trips/
├── maintenance/
├── expenses/
├── analytics/
├── tracking/
├── notifications/
├── ai/
├── ml/
├── customer_tracking/
├── email/
├── database/
├── core/
├── shared/
└── tests/
```
Every feature follows the same structure.
Example:
```text
vehicles/
│
├── routes.py
├── service.py
├── repository.py
├── models.py
├── schemas.py
├── validators.py
├── exceptions.py
├── constants.py
└── tests/
```
Never skip layers unless a layer would contain no logic.
---
# Frontend Structure
```text
frontend/
│
├── routes/
├── components/
├── features/
├── hooks/
├── stores/
├── services/
├── layouts/
├── providers/
├── lib/
├── types/
├── styles/
├── assets/
└── utils/
```
Feature-specific UI belongs inside `features/`.
Reusable UI belongs inside `components/`.
---
# Request Lifecycle
Every request follows the same path.
```text
Frontend
↓
API Route
↓
Validation
↓
Service
↓
Repository
↓
SQLModel
↓
SQLite
↓
Repository
↓
Service
↓
API Response
↓
Frontend Update
```
Business logic must never bypass the service layer.
---
# Service Layer Responsibilities
Responsible for:
* Business rules
* Validation
* Coordination
* Transactions
* AI calls
* ML inference
* Notifications
* Analytics updates
Not responsible for:
* HTTP handling
* SQL queries
* UI formatting
---
# Repository Layer Responsibilities
Responsible for:
* CRUD
* Query optimization
* Transactions
* Pagination
* Filtering
* Sorting
Repositories should never contain business rules.
---
# Database Layer
SQLite is the only database.
Requirements:
* Foreign keys enabled
* Proper indexes
* Transactions
* Constraints
* Automatic initialization
* Automatic demo data generation
The application should function without internet access.
---
# Authentication Flow
```text
Login
↓
Validate Credentials
↓
Verify Password
↓
Load User
↓
Load Role
↓
Create Session
↓
Return Auth State
```
RBAC checks occur before every protected operation.
---
# Dispatch Flow
```text
Create Trip
↓
Validate Vehicle
↓
Validate Driver
↓
Validate Cargo
↓
Generate Route
↓
Generate Tracking ID
↓
Reserve Resources
↓
Update Dashboard
↓
Create Notifications
↓
Return Success
```
---
# Maintenance Flow
```text
Create Maintenance Record
↓
Vehicle Status
↓
In Shop
↓
Hide From Dispatch
↓
Maintenance Complete
↓
Restore Status
↓
Update Analytics
```
---
# Live Tracking Architecture
```text
Trip
↓
Route Geometry
↓
Tracking Service
↓
Position Interpolation
↓
Tracking API
↓
MapLibre
↓
Animated Vehicle
```
Vehicle movement should follow actual road geometry.
No random straight-line movement.
---
# Customer Tracking Flow
```text
Tracking URL
↓
Tracking API
↓
SQLite
↓
Trip
↓
Vehicle Position
↓
ETA
↓
Tracking Page
```
The tracking page is read-only.
Customers never access the desktop application.
---
# Email Flow
```text
Trip Dispatched
↓
Generate Tracking URL
↓
Render Email Template
↓
Preview
↓
SMTP
↓
Customer
```
Email templates should be reusable.
---
# AI Architecture
```text
User Question
↓
Chat Service
↓
Context Builder
↓
Database Queries
↓
Prompt Builder
↓
llama.cpp
↓
Response Formatter
↓
Frontend
```
The LLM should never query SQLite directly.
All context must be provided by the backend.
---
# Machine Learning Architecture
```text
Historical Data
↓
Feature Engineering
↓
Pretrained Model
↓
Inference Service
↓
Prediction
↓
Dashboard
```
Training occurs outside the application.
Only inference is shipped.
---
# Analytics Pipeline
```text
Trip Completed
↓
Update Statistics
↓
Update KPIs
↓
Refresh Dashboard
↓
Refresh Charts
```
Analytics should update automatically after every relevant event.
---
# Notification Pipeline
```text
Business Event
↓
Notification Service
↓
Priority Assignment
↓
Notification Center
↓
UI Toast
↓
History
```
---
# Shared Module
Contains:
* Common exceptions
* Utility functions
* Constants
* Configuration
* Logging
* Date helpers
* Permission helpers
Avoid feature-specific logic here.
---
# Configuration
All configuration must be centralized.
Use environment variables.
No hardcoded:
* Passwords
* API keys
* Email credentials
* File paths
---
# Error Handling
Centralized exception handling.
Requirements:
* User-friendly messages
* Logging
* Proper HTTP status codes
* No stack traces exposed
---
# Dependency Rules
Allowed:
Feature A
↓
Shared
↓
Core
Not allowed:
Feature A
↓
Feature B
Use services or shared interfaces instead.
Avoid circular dependencies.
---
# Performance Goals
Backend startup: <2 seconds
Authentication: <100 ms
CRUD operations: <100 ms
Dashboard refresh: Instant after mutation
Tracking updates: ~1 second
AI response: <5 seconds on recommended model
Application should remain responsive with:
* 500 vehicles
* 2,000 trips
* Live tracking enabled
* Analytics dashboard open
---
# Future Extensibility
The architecture should allow future support for:
* PostgreSQL
* Cloud synchronization
* Mobile application
* Multi-company support
* Multi-region fleets
* Online tracking
* Additional ML models
These are future possibilities only and should not increase current implementation complexity.
---
# Architecture Checklist
* [ ] Feature-based organization
* [ ] Thin routes
* [ ] Service layer implemented
* [ ] Repository layer implemented
* [ ] SQLModel used consistently
* [ ] Offline-first design
* [ ] AI isolated from business logic
* [ ] ML inference isolated
* [ ] Customer tracking isolated
* [ ] Centralized configuration
* [ ] Centralized logging
* [ ] Centralized error handling
* [ ] No circular dependencies
* [ ] No duplicated business logic
* [ ] Documentation updated after architectural changes