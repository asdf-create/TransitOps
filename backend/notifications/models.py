from pydantic import BaseModel
from datetime import datetime
from database.models import Priority

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    priority: Priority = Priority.MEDIUM
    category: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    priority: Priority
    category: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UnreadCountResponse(BaseModel):
    unread_count: int
