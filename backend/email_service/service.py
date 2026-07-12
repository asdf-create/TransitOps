from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone

from database.models import Trip, Vehicle, Driver, EmailLog
from email_service.models import EmailPreviewResponse

class EmailService:
    def __init__(self, session: Session):
        self.session = session

    def generate_preview(self, trip_id: int, recipient_email: str) -> EmailPreviewResponse:
        trip = self.session.get(Trip, trip_id)
        if not trip:
            raise ValueError(f"Trip with ID {trip_id} not found")
        
        vehicle_name = trip.vehicle_name or "Assigned Vehicle"
        driver_name = trip.driver_name or "Assigned Driver"
        tracking_id = trip.tracking_id
        
        # Build nice HTML email body
        subject = f"Your shipment {tracking_id} has been dispatched!"
        tracking_url = f"http://localhost:8080/track/{tracking_id}"
        
        body_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #ffffff;">
            <div style="text-align: center; margin-bottom: 24px;">
                <h1 style="color: #1e3a8a; font-size: 24px; font-weight: 700; margin: 0;">TransitOps Tracking</h1>
                <p style="color: #64748b; font-size: 14px; margin: 4px 0 0 0;">Real-time transport intelligence</p>
            </div>
            
            <div style="background-color: #f8fafc; border-radius: 6px; padding: 16px; margin-bottom: 24px; border: 1px solid #f1f5f9;">
                <h2 style="font-size: 16px; font-weight: 600; color: #0f172a; margin: 0 0 12px 0;">Shipment Dispatched</h2>
                <p style="font-size: 14px; color: #334155; margin: 0 0 16px 0; line-height: 1.5;">
                    Your shipment from <strong>{trip.source}</strong> to <strong>{trip.destination}</strong> has been dispatched.
                </p>
                <div style="text-align: center;">
                    <a href="{tracking_url}" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 10px 20px; font-size: 14px; font-weight: 600; border-radius: 6px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);">
                        Track Shipment Live
                    </a>
                </div>
            </div>
            
            <h3 style="font-size: 14px; font-weight: 600; color: #475569; margin: 0 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">Delivery Details</h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 14px;">
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #64748b;">Tracking ID</td>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; font-weight: 500; text-align: right;">{tracking_id}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #64748b;">Driver</td>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; font-weight: 500; text-align: right;">{driver_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #64748b;">Vehicle</td>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; font-weight: 500; text-align: right;">{vehicle_name} ({trip.vehicle_registration or "N/A"})</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #64748b;">Estimated Arrival</td>
                    <td style="padding: 8px 0; border-bottom: 1px solid #f1f5f9; color: #0f172a; font-weight: 500; text-align: right;">{trip.estimated_arrival.strftime('%Y-%m-%d %H:%M') if trip.estimated_arrival else "Calculating..."}</td>
                </tr>
            </table>
            
            <div style="border-top: 1px solid #e2e8f0; padding-top: 16px; text-align: center; font-size: 12px; color: #94a3b8;">
                This is a simulated transactional email notification from your TransitOps smart logistics environment.
            </div>
        </div>
        """
        
        return EmailPreviewResponse(subject=subject, body_html=body_html)

    def send_email(self, trip_id: int, recipient_email: str) -> EmailLog:
        preview = self.generate_preview(trip_id, recipient_email)
        
        db_log = EmailLog(
            trip_id=trip_id,
            recipient_email=recipient_email,
            subject=preview.subject,
            body_html=preview.body_html,
            sent_at=datetime.now(timezone.utc)
        )
        
        self.session.add(db_log)
        self.session.commit()
        self.session.refresh(db_log)
        return db_log

    def get_history(self, skip: int = 0, limit: int = 100) -> List[EmailLog]:
        return self.session.exec(
            select(EmailLog)
            .order_by(EmailLog.sent_at.desc())
            .offset(skip)
            .limit(limit)
        ).all()
