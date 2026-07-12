# DATABASE.md
# TransitOps Database Specification
Version: 1.0
## Overview
The database is designed for an offline-first desktop application using SQLite and SQLModel. The schema prioritizes data integrity, maintainability, analytical reporting, and future ML inference.
Design principles:
* Normalize operational data.
* Store historical snapshots where required.
* Enforce business rules with constraints whenever possible.
* Use foreign keys and indexes extensively.
* Never physically delete business-critical records unless explicitly required.
---
# Database Engine
Database: SQLite
ORM: SQLModel
Migration Tool: Alembic
Foreign Keys: Enabled
Journal Mode: WAL
Transactions: Required
Automatic initialization on first launch.
---
# Entity Relationship Diagram
```text
User
 │
 ├──────────────┐
 │              │
Trip         Notification
 │
 ├──────────────┐
 │              │
Driver      Vehicle
 │              │
 │              ├────────────┐
 │              │            │
FuelLog   MaintenanceLog  Expense
 │
TripAnalytics
Vehicle
↓
Maintenance
↓
Fuel Logs
↓
Expenses
↓
Analytics
Trip
↓
Tracking
↓
Customer Tracking
↓
Email
```
---
# Tables
1. users
2. roles
3. vehicles
4. drivers
5. trips
6. tracking
7. maintenance_logs
8. fuel_logs
9. expenses
10. notifications
11. dashboard_cache
12. analytics_cache
13. ml_predictions
14. ai_chat_history
15. application_settings
---
# Users
Purpose:
Authentication and authorization.
Columns:
* id
* full_name
* email
* password_hash
* role_id
* phone
* avatar
* created_at
* updated_at
* last_login
* is_active
Constraints:
* Email unique
* Password hash required
* Role required
Indexes:
* email
* role_id
---
# Roles
Columns:
* id
* name
* description
Seed automatically.
Roles:
* Administrator
* Fleet Manager
* Dispatcher
* Driver
* Safety Officer
* Financial Analyst
---
# Vehicles
Columns:
* id
* registration_number
* model
* manufacturer
* vehicle_type
* year
* vin
* fuel_type
* max_load_capacity
* acquisition_cost
* odometer
* insurance_expiry
* registration_expiry
* status
* mileage
* region
* notes
* created_at
* updated_at
Indexes:
* registration_number
* status
* vehicle_type
* region
Constraints:
Registration number must be unique.
Odometer ≥ 0.
Load capacity > 0.
---
# Drivers
Columns:
* id
* full_name
* license_number
* license_category
* license_expiry
* phone
* emergency_contact
* safety_score
* years_experience
* assigned_region
* status
* total_trips
* total_distance
* created_at
* updated_at
Indexes:
* license_number
* status
* assigned_region
Constraints:
License number unique.
Safety score between 0–100.
Experience ≥ 0.
---
# Trips
Trips are immutable historical records after completion.
Columns:
* id
* tracking_id
* source
* destination
* vehicle_id
* driver_id
* cargo_description
* cargo_weight
* planned_distance
* actual_distance
* planned_duration
* actual_duration
* estimated_arrival
* actual_arrival
* planned_departure
* actual_departure
* revenue
* status
* route_geometry
* created_at
* completed_at
Historical snapshot fields:
* vehicle_name
* driver_name
* vehicle_registration
* driver_license_number
These preserve history if related records change later.
Indexes:
* tracking_id
* vehicle_id
* driver_id
* status
---
# Tracking
Stores live trip progress.
Columns:
* id
* trip_id
* latitude
* longitude
* progress_percentage
* current_speed
* remaining_distance
* estimated_arrival
* current_status
* last_updated
Indexes:
* trip_id
Only active trips exist in this table.
Completed trips are archived.
---
# Maintenance Logs
Columns:
* id
* vehicle_id
* maintenance_type
* description
* scheduled_date
* started_date
* completed_date
* estimated_cost
* actual_cost
* predicted_completion
* status
* mechanic_notes
Indexes:
* vehicle_id
* status
---
# Fuel Logs
Columns:
* id
* trip_id
* vehicle_id
* driver_id
* liters
* cost
* odometer
* station
* timestamp
Indexes:
* vehicle_id
* timestamp
---
# Expenses
Columns:
* id
* vehicle_id
* trip_id
* category
* amount
* description
* expense_date
Categories:
* Fuel
* Maintenance
* Toll
* Parking
* Insurance
* Registration
* Repairs
* Miscellaneous
---
# Notifications
Columns:
* id
* user_id
* title
* message
* priority
* category
* read
* created_at
Priority:
* Low
* Medium
* High
* Critical
---
# Dashboard Cache
Stores precomputed KPIs.
Columns:
* id
* metric
* value
* updated_at
Examples:
* Active Vehicles
* Active Trips
* Fleet Utilization
* Average ETA
---
# Analytics Cache
Stores expensive calculations.
Examples:
* Monthly Revenue
* ROI
* Driver Rankings
* Fuel Efficiency
* Vehicle Rankings
Refresh automatically after relevant updates.
---
# ML Predictions
Stores latest model outputs.
Columns:
* id
* trip_id
* prediction_type
* predicted_value
* confidence
* model_version
* generated_at
Prediction Types:
* Delay
* ETA
* Driver Recommendation
* Vehicle Recommendation
* Maintenance
* Repair Duration
These values are ephemeral and may be regenerated.
---
# AI Chat History
Stores local chat history.
Columns:
* id
* user_id
* question
* response
* timestamp
No internet communication.
Entirely offline.
---
# Application Settings
Stores local preferences.
Examples:
* Theme
* Window state
* Default map zoom
* Email settings
* Demo mode
* Animation preferences
---
# Relationships
User
↓
Role
Vehicle
↓
Trips
↓
Tracking
↓
Fuel Logs
↓
Expenses
↓
Maintenance
Driver
↓
Trips
↓
Fuel Logs
Trip
↓
Tracking
↓
Analytics
↓
ML Predictions
---
# Business Rules
Vehicle registration numbers are unique.
License numbers are unique.
Suspended drivers cannot be dispatched.
Expired licenses cannot be dispatched.
Vehicles in maintenance cannot be dispatched.
Retired vehicles cannot be dispatched.
Drivers already on a trip cannot be reassigned.
Vehicles already on a trip cannot be reassigned.
Cargo weight cannot exceed maximum capacity.
Trip completion updates driver and vehicle status automatically.
Trip cancellation restores driver and vehicle availability.
Maintenance automatically changes vehicle status to "In Shop."
Closing maintenance restores vehicle status unless retired.
Odometer values may only increase.
Fuel logs cannot use future dates.
Negative fuel quantities prohibited.
Duplicate fuel logs rejected.
Mandatory driver rest period enforced.
Maximum daily driving hours enforced.
Driver safety score updated after every completed trip.
Maintenance reminders generated automatically.
Predicted maintenance generated by ML.
Fuel anomalies detected automatically.
Route deviation alerts generated when tracking diverges significantly from the planned route.
---
# Demo Dataset
Generate automatically.
Seed:
* 500 Vehicles
* 100 Drivers
* 2,000 Trips
* 300 Maintenance Records
* 5,000 Fuel Logs
* 2,500 Expenses
* Dashboard KPIs
* Analytics Cache
* Demo Users
Use approximately one-third public fleet-inspired data and two-thirds realistic synthetic data generated with Python.
---
# Index Strategy
Create indexes for:
* Email
* Registration Number
* License Number
* Tracking ID
* Vehicle Status
* Driver Status
* Trip Status
* Maintenance Status
* Region
* Created Date
* Trip Completion Date
Avoid indexing rarely queried columns.
---
# Transactions
Use transactions for:
* Dispatch
* Trip Completion
* Maintenance
* Fuel Logging
* Expense Logging
* User Creation
* Driver Assignment
Never leave partially updated business state.
---
# Backup Strategy
Provide manual backup.
Support:
* Export SQLite database
* Restore database
* Reset demo database
No cloud backup.
Offline only.
---
# Future Compatibility
Design schema to simplify migration to PostgreSQL if the project evolves.
Avoid SQLite-specific SQL unless necessary.
Use SQLModel abstractions wherever possible.
---
# Database Checklist
* [ ] Foreign keys enabled
* [ ] WAL mode enabled
* [ ] Alembic configured
* [ ] Seed data generator completed
* [ ] 500 vehicles generated
* [ ] 2,000 trips generated
* [ ] Constraints implemented
* [ ] Indexes created
* [ ] Business rules enforced
* [ ] Transactions implemented
* [ ] Backup and restore implemented
* [ ] Reset demo database implemented
* [ ] Documentation updated