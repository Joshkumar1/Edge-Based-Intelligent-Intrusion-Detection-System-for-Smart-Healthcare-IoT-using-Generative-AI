from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogOut
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[AuditLogOut])
def get_audit_logs(
    action_type: Optional[str] = None,
    target_device_id: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieves immutable security audit logs.
    Accessible to authenticated operators and auditors.
    """
    query = db.query(AuditLog)
    if action_type:
        query = query.filter(AuditLog.action_type == action_type)
    if target_device_id:
        query = query.filter(AuditLog.target_device_id == target_device_id)
    return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
