from sqlalchemy.orm import Session
from datetime import datetime
from app.models.notification import Notification, NotificationType
from app.realtime.ws_manager import ws_manager

def create_notification(
        db: Session,
        student_id: str,
        teacher_id: str|None,
        assignment_id: str|None,
        title: str,
        body: str,
        metadata: dict | None = None,
        notif_type: NotificationType = NotificationType.ASSIGNMENT_STATUS
) -> Notification:
    notif = Notification(
        student_id =student_id,
        teacher_id = teacher_id,
        assignment_id = assignment_id,
        notif_type = notif_type,
        title = title,
        body = body,
        metadata = metadata or {},
        created_at = datetime.now
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    try:
        ws_manager.send_to_user(student_id,{
            "type":"notification",
            "payload":{
                "id": notif.id,
                "title":notif.title,
                "body":notif.metadata,
                "created_at": notif.created_at.isoformat()
            }
        })
    except Exception:
        pass


    return notif