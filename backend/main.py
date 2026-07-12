from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database.connection import init_db
from auth.routes import router as auth_router
from vehicles.routes import router as vehicles_router
from drivers.routes import router as drivers_router
from trips.routes import router as trips_router
from maintenance.routes import router as maintenance_router
from fuel.routes import router as fuel_router
from expenses.routes import router as expenses_router
from dashboard.routes import router as dashboard_router
from analytics.routes import router as analytics_router
from tracking.routes import router as tracking_router
from ai.routes import router as ai_router
from ml.routes import router as ml_router
from notifications.routes import router as notifications_router
from email_service.routes import router as email_router
from search.routes import router as search_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="TransitOps API",
    description="Smart Transport Operations Platform API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(vehicles_router)
app.include_router(drivers_router)
app.include_router(trips_router)
app.include_router(maintenance_router)
app.include_router(fuel_router)
app.include_router(expenses_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)
app.include_router(tracking_router)
app.include_router(ai_router)
app.include_router(ml_router)
app.include_router(notifications_router)
app.include_router(email_router)
app.include_router(search_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
