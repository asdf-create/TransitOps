from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra='forbid')
    role: str
    content: str

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    model: str
    tokens_used: int

class FleetAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    question: str
    context: Optional[str] = None

class FleetAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    answer: str
    insights: List[str]
    recommendations: List[str]
