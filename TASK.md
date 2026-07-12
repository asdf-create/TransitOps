# TASK.md
> TransitOps - Smart Transport Operations Platform
>
> Master Project Specification & Development Roadmap
>
> Version: 1.0
>
> This document is the single source of truth for the project. Every implementation decision should follow this specification unless explicitly changed.
---
# 1. Project Overview
## Objective
Build a modern, offline-first Smart Transport Operations Platform for macOS that goes significantly beyond the hackathon requirements.
The application should feel like a commercial desktop application rather than a CRUD assignment.
The primary objective is to win the hackathon.
Secondary objective is to release the project publicly on GitHub as a flagship portfolio project.
---
# 2. Core Philosophy
This project should prioritize
- simplicity
- maintainability
- performance
- native UX
- beautiful UI
- smooth animations
- enterprise architecture
- AI assistance
- machine learning
- offline capability
Do NOT overengineer.
Follow Ponytail philosophy whenever possible.
Prefer native APIs over unnecessary dependencies.
---
# 3. Primary Goals
## Mandatory
Complete every requirement mentioned in the problem statement.
Nothing mandatory should be skipped.
---
## Showcase Features
Implement the following showcase features.
### Live Vehicle Tracking
Apple Maps inspired tracking.
Vehicle moves smoothly on real roads.
Uses OpenStreetMap routing.
Customer can watch delivery progress live.
---
### Analytics Dashboard
Beautiful animated dashboard.
Enterprise quality.
Discoverable charts.
Interactive filters.
Animated KPIs.
---
### macOS Feel
Desktop experience should feel native.
Keyboard shortcuts.
Native menus.
Context menus.
Window controls.
Dark mode.
---
### AI Assistant
Offline.
Powered by llama.cpp.
Answers logistics questions.
Uses database context.
Can answer
- package location
- ETA
- assigned driver
- assigned vehicle
- maintenance questions
- dispatch information
Voice assistant is NOT required.
---
### Machine Learning
Predict
- delivery delays
- ETA
- maintenance schedule
- repair duration
- best driver
- best vehicle
- dispatch optimization
Models are pre-trained before hackathon.
Only inference happens inside application.
---
### Customer Tracking
Generate tracking links.
Example
http://localhost:8080/track/TRK-XXXX
Customer page displays
- current location
- ETA
- delivery timeline
- vehicle
- driver
- progress
- package status
---
# 4. Technology Stack
## Desktop
Tauri v2
---
## Frontend
TanStack Start
React
TypeScript
Bun
---
## Backend
FastAPI
Python
uv
---
## ORM
SQLModel
---
## Database
SQLite
Offline only
---
## Maps
MapLibre GL JS
OpenStreetMap
OpenRouteService / OSRM
---
## Charts
Apache ECharts
---
## AI
llama.cpp
GGUF model
Offline inference only
---
## Machine Learning
LightGBM
XGBoost
Scikit-Learn
Pandas
NumPy
---
## Components
shadcn/ui
---
## Icons
HugeIcons
Fallback
Lucide
---
## Animations
Framer Motion
Motion
---
## Styling
Tailwind CSS
shadcn theme
Hybrid Apple + AI aesthetic
---
# 5. Architecture
Desktop
↓
React Frontend
↓
FastAPI
↓
Service Layer
↓
Repository Layer
↓
SQLModel
↓
SQLite
---
Everything should follow Feature Based Architecture.
Never organize code by technical layer.
Organize by feature.
Example
backend/
auth/
drivers/
vehicles/
maintenance/
tracking/
analytics/
ai/
ml/
notifications/
expenses/
dashboard/
Each feature contains
routes
services
repository
schemas
models
tests
utils (if needed)
---
# 6. Repository Structure
/
README.md
TASK.md
AGENTS.md
ARCHITECTURE.md
DATABASE.md
API.md
UI_UX.md
ML_AI.md
TESTING.md
RELEASE.md
CONTRIBUTING.md
CHANGELOG.md
SECURITY.md
LICENSE
/docs
/backend
/frontend
/database
/models
/scripts
/assets
---
docs/
screenshots
demo
diagrams
assets
research
---
backend/
auth
dashboard
drivers
vehicles
trips
maintenance
tracking
analytics
expenses
notifications
ml
ai
database
core
tests
---
frontend/
components
routes
hooks
stores
features
styles
assets
types
utils
---
# 7. Development Standards
Python Version
3.12+
---
TypeScript
Strict Mode
---
Formatting
Black
---
Linting
Ruff
---
Dependency Management
Python
uv
Frontend
Bun
---
Never use npm.
Never use yarn.
---
Typing
Use strict typing everywhere.
Avoid Any whenever possible.
---
Imports
Never use wildcard imports.
Always use explicit imports.
---
Functions
Prefer
< 50 lines
Split if needed.
---
Files
Prefer
< 400 lines
Split into modules if necessary.
---
Comments
Explain WHY.
Avoid commenting obvious code.
---
Logging
Use centralized logging.
Never print() for debugging.
---
Configuration
Environment variables only.
No hardcoded secrets.
---
Database
Never write raw SQL unless necessary.
Use SQLModel.
---
Authentication
Local authentication only.
Passwords hashed.
Role Based Access Control.
---
# 8. Git Standards
Repository should remain clean.
Every commit should be meaningful.
Commit often.
Small commits preferred.
---
Commit Messages
Use descriptive commits.
Example
feat(tracking): implement live vehicle animation
NOT
update
fix
changes
---
Branches
main
feature/*
bugfix/*
release/*
---
.gitignore
Must be maintained properly.
Ignore
Python cache
venv
SQLite temporary files
node_modules
dist
build
logs
IDE settings
OS files
GGUF cache if needed
---
# 9. Coding Principles
Always prioritize readability.
Never duplicate logic.
Prefer composition.
Avoid inheritance unless necessary.
Avoid premature optimization.
Keep dependencies minimal.
Follow Ponytail principles.
Prefer native browser APIs.
Prefer standard library.
Document public functions.
Never leave TODOs without issue references.
---
# 10. Definition of Done
A task is complete ONLY if
✓ Feature implemented
✓ UI polished
✓ Animations added
✓ Edge cases handled
✓ Tests written
✓ Tests pass
✓ Documentation updated
✓ Git commit created
✓ No console errors
✓ No lint errors
✓ No unused code
✓ No unused dependencies
# TASK.md (Part 2)
---
# 11. Backend Development Roadmap
The backend is the heart of the application.
All business logic must live in the backend.
Routes should only:
* Validate requests
* Call services
* Return responses
Business logic must **never** be written directly inside API routes.
---
# 12. Core Backend Modules
Implement in the following order.
Priority:
1. Authentication
2. Database
3. Vehicles
4. Drivers
5. Trips
6. Maintenance
7. Fuel & Expenses
8. Dashboard
9. Analytics
10. Tracking
11. Notifications
12. AI
13. ML
Do **not** start AI before the core transport system is complete.
---
# 13. Authentication
## Features
* Local authentication only
* Email + Password
* Role Based Access Control (RBAC)
* Session persistence
* Logout
* Password hashing
* Remember me (optional)
## Roles
* Fleet Manager
* Dispatcher
* Driver
* Safety Officer
* Financial Analyst
* Administrator
## Security
* Argon2id preferred (bcrypt acceptable)
* Secure session/JWT storage
* Password complexity validation
* Login attempt throttling
* Input sanitization
## Demo Accounts
Create predefined demo users for every role.
Allow creating additional local users.
---
# 14. Database Initialization
On first startup:
* Create database automatically
* Create tables
* Seed demo data
* Seed demo users
* Seed dashboard statistics
No manual SQL execution should be required.
---
# 15. Vehicle Module
## CRUD
* Create
* Edit
* Delete (soft delete preferred)
* View
* Search
* Filter
* Sort
## Vehicle Information
* Registration Number
* Model
* Manufacturer
* Year
* Type
* Maximum Load Capacity
* Odometer
* VIN (optional)
* Acquisition Cost
* Insurance Expiry
* Registration Expiry
* Fuel Type
* Mileage
* Region
* Current Status
## Vehicle Status
* Available
* Reserved
* On Trip
* In Shop
* Retired
## Business Rules
Registration number must be unique.
Retired vehicles cannot be dispatched.
Vehicles in maintenance cannot be dispatched.
Vehicles already on trip cannot be reassigned.
Odometer cannot decrease.
Maintenance interval warnings.
Predictive maintenance warnings.
Vehicle utilization statistics.
---
# 16. Driver Module
## CRUD
* Create
* Edit
* Delete
* View
* Search
* Filter
## Driver Information
* Name
* License Number
* License Category
* License Expiry
* Contact Number
* Emergency Contact
* Safety Score
* Experience
* Assigned Region
* Current Status
## Driver Status
* Available
* On Trip
* Off Duty
* Suspended
## Business Rules
Expired license → cannot dispatch
Suspended driver → cannot dispatch
Already on trip → cannot dispatch
Driving hour limits
Mandatory rest period
Automatic safety score updates
Track completed trips
Track total mileage
Track fuel efficiency
Track incident history
---
# 17. Trip Module
Trip lifecycle
Draft
↓
Assigned
↓
Dispatched
↓
In Transit
↓
Completed
↓
Archived
Cancelled trips branch from any non-completed state.
---
## Trip Information
Trip ID
Source
Destination
Driver
Vehicle
Cargo
Weight
Estimated Distance
Estimated Duration
Actual Duration
Estimated Arrival
Actual Arrival
Revenue
Status
Tracking ID
---
## Business Rules
Maximum cargo capacity
Vehicle availability
Driver availability
License validation
Maintenance validation
Trip conflict detection
Duplicate dispatch prevention
Automatic status transitions
Automatic vehicle updates
Automatic driver updates
Automatic ETA calculation
Automatic route generation
Automatic tracking creation
---
# 18. Dispatch Module
Dispatcher can
Assign
Reassign
Cancel
Complete
Archive
---
Automatically
Reserve driver
Reserve vehicle
Generate tracking ID
Create tracking page
Create notifications
Update dashboard
Update analytics
---
Animated dispatch timeline should mirror backend state changes.
---
# 19. Maintenance Module
Create maintenance record.
Close maintenance.
Maintenance history.
Upcoming maintenance.
Predicted maintenance.
---
Maintenance Types
Oil Change
Brake Service
Tire Replacement
Engine Repair
Transmission
General Inspection
Other
---
Business Rules
Opening maintenance
↓
Vehicle automatically becomes
"In Shop"
Closing maintenance
↓
Vehicle returns
Available
unless
Retired
---
# 20. Fuel Module
Store
Fuel quantity
Fuel cost
Station
Date
Odometer
Trip
Vehicle
Driver
---
Analytics
Average mileage
Fuel efficiency
Fuel cost
Cost per kilometer
Monthly trends
---
Validation
Negative fuel prohibited
Duplicate entries
Impossible odometer values
Future dates prohibited
---
# 21. Expense Module
Support
Fuel
Maintenance
Toll
Parking
Repairs
Insurance
Registration
Miscellaneous
---
Analytics
Daily
Weekly
Monthly
Quarterly
Yearly
Vehicle
Driver
Region
---
# 22. Dashboard Module
KPIs
Active Vehicles
Available Vehicles
Vehicles in Shop
Drivers Available
Drivers On Trip
Active Trips
Pending Trips
Completed Trips
Fleet Utilization
Average ETA
Average Delay
Revenue
Operational Cost
Fuel Cost
Maintenance Cost
ROI
---
Dashboard should update automatically after every backend operation.
---
# 23. Analytics Module
Generate
Fuel Efficiency
Fleet Utilization
Vehicle ROI
Average Delivery Time
Driver Rankings
Vehicle Rankings
Trip Heatmaps
Maintenance Cost
Monthly Revenue
Delay Analysis
Repair Trends
Fuel Trends
Dispatch Statistics
---
CSV Export
Mandatory
PDF Export
Optional
---
# 24. Live Tracking Module
Tracking ID generated automatically.
Tracking URL
localhost:8080/track/<tracking-id>
Features
Live position
Animated movement
ETA
Driver
Vehicle
Progress
Timeline
Status
Delivery history
---
Backend responsibilities
Route generation
Position interpolation
ETA updates
Status updates
Tracking API
---
# 25. Email Module
Generate tracking email.
Email includes
Tracking link
ETA
Driver
Vehicle
Status
Estimated arrival
Company branding
---
Support
Preview email
Resend email
Email history
Demo SMTP configuration
---
# 26. Notifications
Upcoming maintenance
License expiry
Vehicle expiry
Trip completion
Trip cancellation
Dispatch created
Fuel anomaly
Maintenance reminder
Delivery completed
ML alerts
---
Notification Center
Unread count
Archive
Dismiss
Priority levels
---
# 27. Search
Global search.
Search across
Vehicles
Drivers
Trips
Expenses
Maintenance
Tracking IDs
---
Support
Partial matches
Fuzzy search
Filters
Sorting
Quick actions
---
# 28. API Guidelines
REST only.
JSON everywhere.
Consistent response format.
Proper HTTP status codes.
Validation errors should be human readable.
Never expose stack traces.
---
# 29. Performance Goals
Backend startup
<2 seconds
Typical API response
<100 ms
Tracking updates
~1 second
Dashboard refresh
Instant after mutations
SQLite queries indexed appropriately.
---
# 30. Backend Completion Checklist
## Authentication
* [ ] Login
* [ ] Logout
* [ ] RBAC
* [ ] Password hashing
* [ ] Demo users
* [ ] Encryption
## Vehicles
* [ ] CRUD
* [ ] Search
* [ ] Filters
* [ ] Validation
## Drivers
* [ ] CRUD
* [ ] Status management
* [ ] License validation
## Trips
* [ ] Lifecycle
* [ ] Dispatch
* [ ] Completion
* [ ] Cancellation
## Maintenance
* [ ] CRUD
* [ ] Status updates
* [ ] History
## Fuel
* [ ] Logging
* [ ] Analytics
## Expenses
* [ ] Categories
* [ ] Reports
## Dashboard
* [ ] KPIs
* [ ] Live updates
## Analytics
* [ ] Charts
* [ ] CSV export
## Tracking
* [ ] Route generation
* [ ] Animated movement
* [ ] Tracking page
## Email
* [ ] Templates
* [ ] Preview
* [ ] Tracking links
## Notifications
* [ ] Alerts
* [ ] Notification Center
## Search
* [ ] Global search
* [ ] Filters
* [ ] Sorting
**Before considering the backend complete:**
* [ ] All mandatory hackathon business rules implemented.
* [ ] Additional enterprise business rules implemented.
* [ ] No duplicated business logic.
* [ ] Services contain business logic; routes remain thin.
* [ ] All database operations go through repositories.
* [ ] Edge cases handled.
* [ ] Documentation updated.
* [ ] Tests passing.
* [ ] Clean commit created.