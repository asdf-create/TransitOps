from sqlmodel import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from ml.models import (
    DelayPredictionRequest, DelayPredictionResponse,
    ETAEstimationRequest, ETAEstimationResponse,
    DriverRecommendationRequest, DriverRecommendationResponse,
    VehicleRecommendationRequest, VehicleRecommendationResponse
)

class MLService:
    def __init__(self, session: Session):
        self.session = session
    
    def predict_delay(self, request: DelayPredictionRequest) -> DelayPredictionResponse:
        """
        Predict trip delays using synthetic ML data.
        All predictions are based on synthetic patterns, not real training data.
        """
        # Generate synthetic delay prediction
        distance_factor = min(request.planned_distance / 100, 1.0)
        duration_factor = min(request.planned_duration / 180, 1.0)
        
        # Simulate ML model prediction with synthetic patterns
        base_delay = random.randint(5, 30)
        distance_adjustment = int(distance_factor * 15)
        duration_adjustment = int(duration_factor * 10)
        
        predicted_delay = base_delay + distance_adjustment + duration_adjustment
        delay_probability = min(0.3 + (distance_factor * 0.4) + (duration_factor * 0.2), 0.95)
        confidence = random.uniform(0.75, 0.92)
        
        # Generate synthetic delay factors
        delay_factors = []
        if distance_factor > 0.7:
            delay_factors.append("Long distance route")
        if duration_factor > 0.6:
            delay_factors.append("Extended trip duration")
        if random.random() > 0.5:
            delay_factors.append("Potential traffic congestion")
        if random.random() > 0.7:
            delay_factors.append("Weather conditions")
        if random.random() > 0.6:
            delay_factors.append("Route complexity")
        
        if not delay_factors:
            delay_factors = ["Route characteristics", "Time of day"]
        
        return DelayPredictionResponse(
            predicted_delay_minutes=predicted_delay,
            delay_probability=round(delay_probability, 2),
            delay_factors=delay_factors,
            confidence=round(confidence, 2),
            on_time_probability=round(1 - delay_probability, 2)
        )
    
    def estimate_eta(self, request: ETAEstimationRequest) -> ETAEstimationResponse:
        """
        Estimate arrival time using synthetic ML data.
        All estimations are based on synthetic patterns, not real training data.
        """
        # Calculate synthetic distance from coordinates
        lat_diff = abs(request.destination_lat - request.current_location_lat)
        lon_diff = abs(request.destination_lon - request.current_location_lon)
        distance = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111  # Rough km conversion
        
        # Generate synthetic ETA prediction
        base_speed = random.uniform(40, 60)  # km/h
        traffic_factor = random.uniform(0.8, 1.3)
        weather_factor = random.uniform(0.9, 1.1)
        
        adjusted_speed = base_speed * traffic_factor * weather_factor
        estimated_duration = int((distance / adjusted_speed) * 60)  # minutes
        
        eta = datetime.now() + timedelta(minutes=estimated_duration)
        confidence = random.uniform(0.80, 0.95)
        
        return ETAEstimationResponse(
            estimated_arrival=eta,
            estimated_duration_minutes=estimated_duration,
            confidence=round(confidence, 2),
            traffic_factor=round(traffic_factor, 2),
            weather_factor=round(weather_factor, 2)
        )
    
    def recommend_drivers(self, request: DriverRecommendationRequest) -> DriverRecommendationResponse:
        """
        Recommend drivers using synthetic ML data.
        All recommendations are based on synthetic patterns, not real training data.
        """
        # Generate synthetic driver recommendations
        num_recommendations = random.randint(3, 5)
        recommended_drivers = []
        
        for i in range(num_recommendations):
            safety_score = random.randint(85, 98)
            experience_years = random.randint(2, 15)
            total_trips = random.randint(100, 500)
            match_score = random.uniform(0.75, 0.95)
            
            driver = {
                "driver_id": random.randint(1, 50),
                "name": f"Driver {random.randint(100, 999)}",
                "safety_score": safety_score,
                "experience_years": experience_years,
                "total_trips": total_trips,
                "match_score": round(match_score, 2),
                "availability": random.choice(["Available", "Available", "Available", "On Trip", "Off Duty"]),
                "region": random.choice(["North", "South", "East", "West"]),
                "rating": round(random.uniform(4.0, 5.0), 1)
            }
            recommended_drivers.append(driver)
        
        # Sort by match score
        recommended_drivers.sort(key=lambda x: x["match_score"], reverse=True)
        
        reasoning = "Based on synthetic ML analysis considering safety scores, experience, trip history, and current availability."
        
        return DriverRecommendationResponse(
            recommended_drivers=recommended_drivers,
            reasoning=reasoning
        )
    
    def recommend_vehicles(self, request: VehicleRecommendationRequest) -> VehicleRecommendationResponse:
        """
        Recommend vehicles using synthetic ML data.
        All recommendations are based on synthetic patterns, not real training data.
        """
        # Generate synthetic vehicle recommendations
        num_recommendations = random.randint(3, 5)
        recommended_vehicles = []
        
        vehicle_types = ["Truck", "Van", "Semi-Truck", "Delivery Truck"]
        
        for i in range(num_recommendations):
            capacity = random.uniform(2000, 8000)
            fuel_efficiency = random.uniform(6, 12)
            maintenance_score = random.randint(70, 98)
            utilization_rate = random.uniform(0.4, 0.9)
            match_score = random.uniform(0.70, 0.95)
            
            vehicle = {
                "vehicle_id": random.randint(1, 30),
                "registration": f"V-{random.randint(100, 999)}",
                "type": random.choice(vehicle_types),
                "model": f"Model {random.randint(100, 999)}",
                "capacity_kg": round(capacity, 0),
                "fuel_efficiency_km_l": round(fuel_efficiency, 1),
                "maintenance_score": maintenance_score,
                "utilization_rate": round(utilization_rate, 2),
                "match_score": round(match_score, 2),
                "status": random.choice(["Available", "Available", "Available", "On Trip", "In Shop"]),
                "region": random.choice(["North", "South", "East", "West"])
            }
            recommended_vehicles.append(vehicle)
        
        # Sort by match score
        recommended_vehicles.sort(key=lambda x: x["match_score"], reverse=True)
        
        reasoning = "Based on synthetic ML analysis considering cargo capacity, fuel efficiency, maintenance status, and current availability."
        
        return VehicleRecommendationResponse(
            recommended_vehicles=recommended_vehicles,
            reasoning=reasoning
        )