# API.md
# TransitOps API Specification
Version: 1.0
## Overview
The backend exposes a REST API exclusively for the desktop frontend and the local customer tracking website.
Goals:
* Consistent endpoint design
* Predictable responses
* Strong validation
* Thin routes
* Service-driven architecture
Base URL:
```text
http://localhost:8000
```
No API versioning is required for this hackathon.
---
# Response Format
Successful responses:
```json
{
  "success": true,
  "message": "Vehicle created successfully.",
  "data": {}
}
```
Validation errors:
```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {}
}
```
Unexpected errors:
```json
{
  "success": false,
  "message": "An unexpected error occurred."
}
```
Never expose stack traces.
---
# Authentication
## POST /auth/login
Authenticate user.
Request
* Email
* Password
Response
* User
* Role
* Authentication token/session
---
## POST /auth/logout
Terminate session.
---
## GET /auth/me
Return currently authenticated user.
---
## POST /auth/users
Create local user.
Administrator only.
---
## PATCH /auth/users/{id}
Update user.
---
## DELETE /auth/users/{id}
Deactivate user.
Prefer soft delete.
---
# Vehicles
## GET /vehicles
Supports:
* Search
* Filters
* Pagination
* Sorting
---
## GET /vehicles/{id}
Return complete vehicle details.
---
## POST /vehicles
Create vehicle.
Validation:
* Registration unique
* Positive load capacity
* Valid status
---
## PATCH /vehicles/{id}
Update vehicle.
---
## DELETE /vehicles/{id}
Soft delete preferred.
---
## GET /vehicles/statistics
Returns:
* Fleet utilization
* Active vehicles
* Maintenance count
* Average mileage
---
# Drivers
## GET /drivers
List drivers.
Supports:
* Search
* Filters
* Pagination
---
## GET /drivers/{id}
Driver profile.
---
## POST /drivers
Create driver.
Validation:
* Unique license
* Safety score
* Expiry date
---
## PATCH /drivers/{id}
Update driver.
---
## DELETE /drivers/{id}
Deactivate driver.
---
## GET /drivers/rankings
Returns ML-enhanced driver ranking.
---
# Trips
## GET /trips
List trips.
Supports:
* Search
* Status filter
* Vehicle filter
* Driver filter
* Date filter
---
## GET /trips/{id}
Trip details.
---
## POST /trips
Create draft trip.
Validates:
* Driver
* Vehicle
* Cargo
* Route
Generates:
* Tracking ID
* ETA
---
## POST /trips/{id}/dispatch
Dispatch trip.
Automatically:
* Updates statuses
* Generates tracking
* Sends notification
* Updates dashboard
---
## POST /trips/{id}/complete
Complete trip.
Automatically:
* Updates driver
* Updates vehicle
* Updates analytics
* Logs fuel
* Calculates ROI
---
## POST /trips/{id}/cancel
Cancel trip.
Restores resources.
---
# Maintenance
## GET /maintenance
List records.
---
## POST /maintenance
Create maintenance record.
Automatically:
* Changes vehicle status
* Removes vehicle from dispatch pool
---
## PATCH /maintenance/{id}
Update maintenance.
---
## POST /maintenance/{id}/complete
Close maintenance.
Restore availability.
---
# Fuel
## GET /fuel
List logs.
---
## POST /fuel
Create fuel log.
Validation:
* Positive quantity
* Valid odometer
* Duplicate detection
---
# Expenses
## GET /expenses
List expenses.
---
## POST /expenses
Create expense.
Supported categories:
* Fuel
* Maintenance
* Toll
* Parking
* Insurance
* Registration
* Repairs
* Miscellaneous
---
# Dashboard
## GET /dashboard
Returns:
* KPIs
* Fleet utilization
* Revenue
* Cost
* Active trips
* Driver availability
* Vehicle availability
Single request should populate dashboard.
---
# Analytics
## GET /analytics
Returns dashboard analytics.
---
## GET /analytics/revenue
Revenue charts.
---
## GET /analytics/fuel
Fuel efficiency.
---
## GET /analytics/drivers
Driver performance.
---
## GET /analytics/vehicles
Vehicle analytics.
---
## GET /analytics/roi
Vehicle ROI.
---
## GET /analytics/export/csv
Export analytics.
Mandatory.
---
## GET /analytics/export/pdf
Optional.
---
# Live Tracking
## GET /tracking/{tracking_id}
Returns:
* Position
* ETA
* Progress
* Status
* Driver
* Vehicle
Used by desktop app and customer tracking page.
---
## GET /tracking/{tracking_id}/history
Tracking timeline.
---
## GET /tracking/{tracking_id}/route
Returns route geometry for MapLibre.
---
# Customer Tracking Website
Base URL
```text
http://localhost:8080/track/{tracking_id}
```
Uses tracking endpoints only.
Read-only.
No authentication required.
Displays:
* Live location
* ETA
* Driver
* Vehicle
* Timeline
* Delivery progress
---
# Notifications
## GET /notifications
List notifications.
---
## PATCH /notifications/{id}/read
Mark as read.
---
## PATCH /notifications/read-all
Mark all read.
---
## DELETE /notifications/{id}
Dismiss notification.
---
# Email
## POST /email/preview
Generate preview.
---
## POST /email/send
Send tracking email.
Includes:
* Tracking link
* ETA
* Driver
* Vehicle
* Status
---
## GET /email/history
Email history.
---
# AI Assistant
## POST /ai/chat
Request
* User message
Response
* AI answer
* Sources
* Suggested actions (optional)
Questions include:
* Where is my package?
* ETA
* Assigned driver
* Assigned vehicle
* Maintenance status
* Delivery delays
Offline only.
Uses llama.cpp.
---
# Machine Learning
## GET /ml/predict-delay/{trip_id}
Returns:
* Predicted delay
* Confidence
---
## GET /ml/predict-maintenance/{vehicle_id}
Returns:
* Next maintenance estimate
* Confidence
---
## GET /ml/recommend-driver/{trip_id}
Returns ranked drivers.
---
## GET /ml/recommend-vehicle/{trip_id}
Returns ranked vehicles.
---
## GET /ml/predict-repair/{maintenance_id}
Returns:
* Estimated repair duration
* Confidence
---
# Search
## GET /search
Global search.
Supports:
* Vehicles
* Drivers
* Trips
* Tracking IDs
* Maintenance
* Expenses
---
# Health
## GET /health
Returns application status.
Used by frontend during startup.
---
# Validation Rules
Every endpoint must validate:
* Required fields
* Field lengths
* Invalid enums
* Invalid IDs
* Invalid dates
* Duplicate records
* Business rules
* Permissions
Validation belongs in the backend.
---
# Authorization
Administrator
Full access.
Fleet Manager
Fleet operations.
Dispatcher
Trips and dispatch.
Safety Officer
Drivers and maintenance.
Financial Analyst
Expenses and analytics.
Driver
Read-only access to assigned trips.
Customer tracking endpoints require no authentication.
---
# Performance Targets
Authentication: <100 ms
CRUD operations: <100 ms
Dashboard: <250 ms
Analytics: <500 ms
Tracking: ~1 second refresh
AI: <5 seconds
ML inference: <500 ms
---
# API Checklist
* [ ] Consistent response format
* [ ] RESTful naming
* [ ] Backend validation
* [ ] Permission checks
* [ ] Business rule enforcement
* [ ] Thin routes
* [ ] Service layer only
* [ ] Repository layer only accesses database
* [ ] No duplicated logic
* [ ] Meaningful error messages
* [ ] Health endpoint implemented
* [ ] Customer tracking endpoints implemented
* [ ] Documentation updated after API changes