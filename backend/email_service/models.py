from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmailPreviewRequest(BaseModel):
    trip_id: int
    recipient_email: str

class EmailPreviewResponse(BaseModel):
    subject: str
    body_html: str

class EmailSendRequest(BaseModel):
    trip_id: int
    recipient_email: str

class EmailLogResponse(BaseModel):
    id: int
    trip_id: int
    recipient_email: str
    subject: str
    body_html: str
    sent_at: datetime

    class Config:
        from_attributes = True
