# TransitOps
> **An offline-first, AI-powered Smart Transport Operations Platform built for modern fleet management.**
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TanStack Start](https://img.shields.io/badge/TanStack-Start-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Tauri](https://img.shields.io/badge/Tauri-v2-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
## Overview
TransitOps is a modern desktop fleet management platform that combines logistics management, real-time delivery tracking, predictive machine learning, and offline AI assistance into a single native desktop application.
Unlike traditional fleet management systems that rely on cloud infrastructure, TransitOps is designed to work entirely offline while still providing intelligent analytics, predictive maintenance, delivery forecasting, and an interactive operations dashboard.
This project was built as a showcase-quality hackathon submission with an emphasis on clean architecture, polished UI, and production-ready engineering practices.
---
## Key Features
### Fleet Management
* Vehicle management
* Driver management
* Trip planning
* Dispatch workflow
* Maintenance management
* Fuel logging
* Expense tracking
* Fleet analytics
### Live Delivery Tracking
* Real road routing using OpenStreetMap
* Smooth Apple Maps–style vehicle animation
* Customer tracking webpage
* Delivery progress timeline
* ETA estimation
* Live route visualization
### AI Assistant
Completely offline AI assistant powered by **llama.cpp**.
Supports questions such as:
* Where is shipment TRK-1042?
* Who is delivering my package?
* Which vehicle requires maintenance?
* Recommend the best driver.
* Explain today's fleet statistics.
* Why is this shipment delayed?
No cloud APIs are required.
---
### Machine Learning
Offline ML models provide:
* Delivery delay prediction
* ETA prediction
* Driver recommendation
* Vehicle recommendation
* Predictive maintenance
* Repair duration prediction
Models are trained before deployment and loaded locally for inference.
---
### Analytics Dashboard
Interactive dashboard featuring:
* Fleet utilization
* Revenue
* Operational cost
* Fuel efficiency
* Vehicle ROI
* Driver rankings
* Delivery trends
* Maintenance statistics
* Delay analysis
* Live tracking overview
Powered by Apache ECharts.
---
### Modern Desktop Experience
* Native desktop application
* Dark mode
* Glassmorphism UI
* Smooth animations
* Interactive charts
* Command palette
* Responsive tables
* Beautiful empty states
* Keyboard shortcuts
---
## Technology Stack
### Desktop
* Tauri v2
### Frontend
* React
* TanStack Start
* TypeScript
* Bun
* Tailwind CSS
* shadcn/ui
### Backend
* FastAPI
* Python
* uv
* SQLModel
### Database
* SQLite
### AI
* llama.cpp
### Machine Learning
* Scikit-Learn
* LightGBM
* XGBoost
### Maps
* MapLibre GL JS
* OpenStreetMap
### Charts
* Apache ECharts
---
## Screenshots
Screenshots will be added after implementation.
* Dashboard
* Live Tracking
* Analytics
* Vehicles
* Drivers
* AI Assistant
* Customer Tracking
* Maintenance
* Expenses
---
## Project Architecture
```text
                 Tauri Desktop
                       │
       ┌───────────────┴───────────────┐
       │                               │
TanStack Start + React           Customer Tracking
       │                               │
       └───────────────┬───────────────┘
                       │
                    FastAPI
                       │
        ┌──────────────┴──────────────┐
        │                             │
     Services                    AI / ML
        │                             │
        └──────────────┬──────────────┘
                       │
                 Repository Layer
                       │
               SQLModel + SQLite
```
---
## Project Structure
```text
TransitOps/
├── backend/
├── frontend/
├── models/
├── assets/
├── scripts/
├── docs/
├── AGENTS.md
├── TASK.md
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
## Core Modules
* Authentication
* Dashboard
* Vehicle Management
* Driver Management
* Trip Management
* Dispatch
* Live Tracking
* Customer Tracking
* Maintenance
* Fuel Management
* Expense Management
* Analytics
* Notifications
* AI Assistant
* Machine Learning
---
## Machine Learning Pipeline
Historical Fleet Data
↓
Feature Engineering
↓
Model Training
↓
Model Evaluation
↓
Export Models
↓
Offline Inference
↓
Dashboard Predictions
Training occurs outside the application.
The desktop application performs inference only.
---
## AI Pipeline
User Question
↓
Context Builder
↓
Database Queries
↓
Prompt Construction
↓
llama.cpp
↓
Response Formatting
↓
Desktop UI
---
## Demo Dataset
TransitOps ships with a realistic offline demo dataset containing approximately:
| Dataset             | Count |
| ------------------- | ----: |
| Vehicles            |   500 |
| Drivers             |   100 |
| Trips               | 2,000 |
| Fuel Logs           | 5,000 |
| Maintenance Records |   300 |
| Expenses            | 2,500 |
The dataset consists of approximately one-third public fleet-inspired data and two-thirds synthetically generated data.
---
## Development Setup
### Clone
```bash
git clone <repository-url>
cd TransitOps
```
### Backend
```bash
cd backend
uv sync
uv run main.py
```
### Frontend
```bash
cd frontend
bun install
bun run dev
```
### Desktop
```bash
bun run tauri dev
```
---
## Building
Development
```bash
bun run tauri dev
```
Production
```bash
bun run tauri build
```
---
## Testing
Run backend tests
```bash
pytest
```
Before every release verify:
* Business rules
* Edge cases
* Authentication
* Tracking
* AI
* Machine Learning
* Analytics
* Dashboard
* Customer tracking
* Email preview
See **TESTING.md** for the complete testing strategy.
---
## Documentation
Project documentation includes:
* TASK.md
* AGENTS.md
* ARCHITECTURE.md
* DATABASE.md
* API.md
* UI_UX.md
* ML_AI.md
* TESTING.md
* RELEASE.md
Additional documentation is available inside the `docs/` directory.
---
## Roadmap
Planned future improvements include:
* PostgreSQL support
* Cloud synchronization
* Mobile application
* Route optimization
* Fleet demand forecasting
* Driver fatigue detection
* Spare parts inventory prediction
* Multi-company support
See `docs/ROADMAP.md` for details.
---
## Contributing
Contributions are welcome.
Before opening a pull request:
* Follow `AGENTS.md`
* Write tests
* Update documentation
* Keep commits small and descriptive
* Ensure all tests pass
See `CONTRIBUTING.md` for complete guidelines.
---
## Performance Targets
* Backend startup: <2 seconds
* CRUD operations: <100 ms
* Dashboard refresh: <250 ms
* ML inference: <500 ms
* AI response: <5 seconds
* Live tracking refresh: ~1 second
---
## License
This project is licensed under the MIT License.
See `LICENSE` for details.
---
## Acknowledgements
TransitOps is built using several outstanding open-source projects, including:
* FastAPI
* SQLModel
* React
* TanStack Start
* Tauri
* Tailwind CSS
* shadcn/ui
* Apache ECharts
* MapLibre GL JS
* OpenStreetMap
* llama.cpp
* LightGBM
* XGBoost
* Scikit-Learn
Special thanks to the maintainers and contributors of these projects.
---
## Repository Status
**Under Active Development**
This project is being developed as a showcase-quality hackathon submission with the long-term goal of becoming a polished open-source desktop application for intelligent fleet management.