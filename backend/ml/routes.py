from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database.connection import get_session
from ml.service import MLService
from ml.models import (
    DelayPredictionRequest, DelayPredictionResponse,
    ETAEstimationRequest, ETAEstimationResponse,
    DriverRecommendationRequest, DriverRecommendationResponse,
    VehicleRecommendationRequest, VehicleRecommendationResponse
)

router = APIRouter(prefix="/ml", tags=["ml"])

@router.post("/predict-delay", response_model=DelayPredictionResponse)
def predict_delay(request: DelayPredictionRequest, session: Session = Depends(get_session)):
    """
    Predict trip delays using ML models (synthetic data).
    """
    service = MLService(session)
    return service.predict_delay(request)

@router.post("/estimate-eta", response_model=ETAEstimationResponse)
def estimate_eta(request: ETAEstimationRequest, session: Session = Depends(get_session)):
    """
    Estimate arrival time using ML models (synthetic data).
    """
    service = MLService(session)
    return service.estimate_eta(request)

@router.post("/recommend-drivers", response_model=DriverRecommendationResponse)
def recommend_drivers(request: DriverRecommendationRequest, session: Session = Depends(get_session)):
    """
    Recommend drivers for a trip using ML models (synthetic data).
    """
    service = MLService(session)
    return service.recommend_drivers(request)

@router.post("/recommend-vehicles", response_model=VehicleRecommendationResponse)
def recommend_vehicles(request: VehicleRecommendationRequest, session: Session = Depends(get_session)):
    """
    Recommend vehicles for a trip using ML models (synthetic data).
    """
    service = MLService(session)
    return service.recommend_vehicles(request)

@router.get("/status")
def ml_status():
    """
    Check the status of ML prediction services.
    """
    return {
        "status": "ready",
        "data_source": "synthetic",
        "models": ["delay_prediction", "eta_estimation", "driver_recommendation", "vehicle_recommendation"],
        "description": "ML services running with synthetic data patterns for demonstration"
    }