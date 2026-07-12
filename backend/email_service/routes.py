from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List

from database.connection import get_session
from email_service.models import EmailPreviewRequest, EmailPreviewResponse, EmailSendRequest, EmailLogResponse
from email_service.service import EmailService

router = APIRouter(prefix="/email", tags=["Email"])

@router.post("/preview", response_model=EmailPreviewResponse)
def get_email_preview(
    request: EmailPreviewRequest,
    session: Session = Depends(get_session)
):
    service = EmailService(session)
    try:
        return service.generate_preview(request.trip_id, request.recipient_email)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/send", response_model=EmailLogResponse)
def send_email(
    request: EmailSendRequest,
    session: Session = Depends(get_session)
):
    service = EmailService(session)
    try:
        return service.send_email(request.trip_id, request.recipient_email)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/history", response_model=List[EmailLogResponse])
def get_email_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    service = EmailService(session)
    return service.get_history(skip, limit)
