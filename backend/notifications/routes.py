from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List

from database.connection import get_session
from notifications.models import NotificationCreate, NotificationResponse, UnreadCountResponse
from notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification_data: NotificationCreate,
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    return service.create_notification(notification_data)

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    user_id: int = Query(1, description="ID of the user to get notifications for"),
    unread_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    return service.get_notifications(user_id, unread_only, skip, limit)

@router.get("/count", response_model=UnreadCountResponse)
def get_unread_count(
    user_id: int = Query(1),
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    return UnreadCountResponse(unread_count=service.get_unread_count(user_id))

@router.patch("/{id}/read", response_model=NotificationResponse)
def mark_read(
    id: int,
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    notification = service.mark_read(id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification

@router.patch("/read-all")
def mark_all_read(
    user_id: int = Query(1),
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    count = service.mark_all_read(user_id)
    return {"message": f"Successfully marked {count} notifications as read"}

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_notification(
    id: int,
    session: Session = Depends(get_session)
):
    service = NotificationService(session)
    success = service.delete_notification(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return {"message": "Notification deleted successfully"}
