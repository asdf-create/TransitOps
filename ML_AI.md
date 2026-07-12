# ML_AI.md
# TransitOps AI & Machine Learning Specification
Version: 1.0
## Objective
The AI/ML system should provide genuine operational value instead of acting as a gimmick.
All inference must run completely offline.
The ML models should be trained before the hackathon and packaged with the application.
The desktop application performs inference only.
---
# AI Stack
LLM Runtime
* llama.cpp
Model Format
* GGUF
Suggested Model Size
* 2B–4B parameters
Requirements
* Offline only
* Local inference
* No API keys
* No cloud services
Design the application so models can be swapped without modifying business logic.
---
# ML Stack
Libraries
* LightGBM
* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* Joblib
Optional
* SHAP (model explainability)
Training notebooks should be kept separate from the application.
---
# Dataset Strategy
Training Data
Approximately:
* ⅓ Public fleet/logistics datasets
* ⅔ Synthetic data generated with Python
The synthetic data should resemble realistic transport operations.
Avoid obviously random values.
---
# Synthetic Data Requirements
Generate realistic:
* Vehicles
* Drivers
* Trips
* Routes
* Fuel logs
* Expenses
* Maintenance records
* Delays
* Weather labels (optional)
* Traffic labels (optional)
Ensure relationships remain internally consistent.
---
# Feature Engineering
Vehicle Features
* Vehicle age
* Vehicle type
* Fuel type
* Odometer
* Maintenance history
* Previous breakdowns
* Region
* Utilization
Driver Features
* Safety score
* Experience
* Historical delays
* Route familiarity
* Average speed
* Driving hours
* Rest periods
* Incident history
Trip Features
* Cargo weight
* Planned distance
* Estimated duration
* Departure time
* Route
* Vehicle
* Driver
* Historical route delays
Operational Features
* Fuel efficiency
* Maintenance frequency
* Average revenue
* Cost per kilometer
---
# Model 1
Delivery Delay Prediction
Purpose
Predict whether a delivery is likely to be delayed.
Inputs
* Driver
* Vehicle
* Distance
* Cargo
* Route
* Historical performance
* Time of day
Outputs
* Delay probability
* Estimated delay
* Confidence score
Display prediction on:
* Dashboard
* Dispatch page
* Tracking page
---
# Model 2
ETA Prediction
Purpose
Generate improved estimated arrival times.
Inputs
* Planned distance
* Driver
* Vehicle
* Historical route duration
* Current tracking progress
Outputs
* ETA
* Confidence
Update automatically during active deliveries.
---
# Model 3
Driver Recommendation
Purpose
Recommend the best available driver.
Ranking Factors
* Safety score
* Route familiarity
* Historical delays
* Experience
* Current workload
* Rest status
Return Top 5 recommendations.
Provide a recommendation score.
---
# Model 4
Vehicle Recommendation
Purpose
Recommend the most suitable vehicle.
Ranking Factors
* Capacity
* Fuel efficiency
* Maintenance risk
* Region
* Availability
* Historical reliability
Return ranked recommendations.
---
# Model 5
Predictive Maintenance
Purpose
Estimate when maintenance should occur.
Inputs
* Odometer
* Vehicle age
* Previous maintenance
* Fuel efficiency
* Vehicle type
Outputs
* Predicted maintenance date
* Confidence
* Risk level
Display warning badges in the dashboard.
---
# Model 6
Repair Duration Prediction
Purpose
Estimate maintenance completion time.
Inputs
* Vehicle
* Maintenance type
* Historical repairs
* Vehicle age
Outputs
* Estimated repair duration
* Confidence
* Expected completion
---
# Model Explainability
Where practical, provide simple explanations.
Examples
"Predicted delay is high because this route has historically experienced long delivery times."
"Vehicle recommendation is based on capacity, fuel efficiency, and maintenance history."
Avoid exposing raw model internals to end users.
---
# AI Assistant
Purpose
Allow users to query the transport system using natural language.
Example Questions
* Where is shipment TRK-2045?
* Who is delivering package TRK-1023?
* Which vehicles require maintenance?
* Which driver has the highest safety score?
* Why is this delivery delayed?
* Recommend the best driver.
* Recommend the best vehicle.
* Show today's active trips.
---
# AI Architecture
User Question
↓
Intent Detection
↓
Context Builder
↓
Relevant Database Queries
↓
Prompt Construction
↓
llama.cpp
↓
Response Formatter
↓
Frontend
The model must never directly access SQLite.
---
# Prompt Construction
Prompt should include:
* User role
* Current question
* Relevant database records
* ML predictions (if available)
* System instructions
Keep prompts concise.
Avoid sending unnecessary database records.
---
# Context Builder
Responsible for:
* Querying SQLite
* Selecting relevant records
* Summarizing data
* Building prompts
This module should remain independent of the LLM implementation.
---
# Chat Features
Support
* Markdown
* Tables
* Bullet lists
* Suggested follow-up questions
Do not support code generation.
Focus on logistics operations.
---
# Conversation History
Store locally.
Allow:
* View history
* Clear history
* Continue previous conversation
Never upload conversation data.
---
# Future RAG Support
Do not implement during the hackathon.
Design the architecture so future support for:
* PDFs
* Policies
* Manuals
* SOPs
can be added with minimal refactoring.
---
# Model Storage
Store trained models in:
```text
/models/
```
Recommended layout
```text
models/
├── delay_prediction.joblib
├── eta_prediction.joblib
├── driver_recommender.joblib
├── vehicle_recommender.joblib
├── maintenance_prediction.joblib
├── repair_duration.joblib
└── llama/
    └── model.gguf
```
Avoid storing training datasets inside the repository.
Provide download instructions if models exceed GitHub limits.
---
# Training Pipeline
Keep training code separate.
Suggested layout
```text
ml/
├── datasets/
├── notebooks/
├── preprocessing/
├── training/
├── evaluation/
└── export/
```
The desktop application should never contain training code.
---
# Model Evaluation
Track
* Accuracy
* Precision
* Recall
* F1 Score
* MAE
* RMSE
Maintain evaluation reports inside the `docs/` folder.
---
# Performance Targets
LLM Response
<5 seconds
ML Prediction
<500 ms
Dashboard Prediction Refresh
<1 second
Application startup should not block while loading large models.
Lazy-load models when appropriate.
---
# Future Improvements
Potential future models
* Fuel consumption prediction
* Driver fatigue detection
* Route optimization
* Fleet utilization forecasting
* Cost forecasting
* Demand forecasting
* Breakdown probability prediction
* Inventory forecasting for spare parts
These are intentionally out of scope for the hackathon.
---
# AI/ML Checklist
* [ ] Public datasets collected
* [ ] Synthetic data generated
* [ ] Feature engineering pipeline completed
* [ ] Delay model trained
* [ ] ETA model trained
* [ ] Driver recommendation model trained
* [ ] Vehicle recommendation model trained
* [ ] Maintenance model trained
* [ ] Repair duration model trained
* [ ] Models evaluated
* [ ] Models exported
* [ ] llama.cpp integrated
* [ ] Context builder implemented
* [ ] Prompt templates created
* [ ] AI assistant integrated
* [ ] Offline inference verified
* [ ] Documentation updated