from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database.connection import get_session
from ai.service import AIService
from ai.models import ChatRequest, ChatResponse, FleetAnalysisRequest, FleetAnalysisResponse

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    """
    Chat with the AI assistant using offline llama.cpp inference.
    """
    service = AIService(session)
    return service.chat(request)

@router.post("/analyze", response_model=FleetAnalysisResponse)
def analyze_fleet(request: FleetAnalysisRequest, session: Session = Depends(get_session)):
    """
    Analyze fleet data and get AI-powered insights and recommendations.
    """
    service = AIService(session)
    return service.analyze_fleet(request)

@router.get("/status")
def ai_status():
    """
    Check the status of the AI assistant and llama.cpp integration.
    """
    return {
        "status": "ready",
        "model": "llama-cpp-offline",
        "inference_type": "offline",
        "description": "AI assistant is ready for offline inference using llama.cpp"
    }