from sqlmodel import Session, select
from typing import List, Optional
from database.models import Notification, Priority
from notifications.models import NotificationCreate

class NotificationService:
    def __init__(self, session: Session):
        self.session = session

    def create_notification(self, notification_data: NotificationCreate) -> Notification:
        db_notification = Notification.model_validate(notification_data)
        self.session.add(db_notification)
        self.session.commit()
        self.session.refresh(db_notification)
        return db_notification

    def get_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Notification]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.read == False)
        
        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        return self.session.exec(query).all()

    def mark_read(self, notification_id: int) -> Optional[Notification]:
        notification = self.session.get(Notification, notification_id)
        if not notification:
            return None
        
        notification.read = True
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def mark_all_read(self, user_id: int) -> int:
        notifications = self.session.exec(
            select(Notification)
            .where(Notification.user_id == user_id)
            .where(Notification.read == False)
        ).all()
        
        count = len(notifications)
        for notification in notifications:
            notification.read = True
            self.session.add(notification)
        
        if count > 0:
            self.session.commit()
            
        return count

    def delete_notification(self, notification_id: int) -> bool:
        notification = self.session.get(Notification, notification_id)
        if not notification:
            return False
        
        self.session.delete(notification)
        self.session.commit()
        return True

    def get_unread_count(self, user_id: int) -> int:
        notifications = self.session.exec(
            select(Notification)
            .where(Notification.user_id == user_id)
            .where(Notification.read == False)
        ).all()
        return len(notifications)
