import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.alert import Alert
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.alert import AlertOut, AlertUpdateStatus
from app.api.deps import require_triage_privilege

router = APIRouter()


@router.get("/", response_model=List[AlertOut])
def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
        
    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.patch("/{alert_id}/status", response_model=AlertOut)
def update_alert_status(
    alert_id: str,
    update_in: AlertUpdateStatus,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_triage_privilege)
):
    """
    Updates incident alert status (e.g., NEW -> INVESTIGATING -> MITIGATED).
    Requires triage authorization and records immutable audit log entry.
    """
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    prev_status = alert.status
    resolved_by = update_in.resolved_by or current_user.username
    now = datetime.now(timezone.utc)
    
    alert.status = update_in.status
    alert.resolved_by = resolved_by
    alert.resolved_at = now
    
    # Audit log creation
    client_ip = request.client.host if request.client else "unknown"
    audit = AuditLog(
        audit_id=f"AUD-{uuid.uuid4().hex[:10].upper()}",
        actor_id=current_user.id,
        actor_username=current_user.username,
        actor_role=current_user.role,
        action_type="ALERT_STATUS_UPDATE",
        target_entity_type="ALERT",
        target_entity_id=alert.alert_id,
        target_device_id=alert.target_device_id,
        previous_state=prev_status,
        new_state=update_in.status,
        impact_assessment=f"Status transitioned from {prev_status} to {update_in.status}",
        timestamp=now,
        source_ip=client_ip,
        enforcement_mode="DATABASE_RECORD",
        enforcement_status="ENFORCED",
        enforcement_result={"resolved_by": resolved_by},
        success=True,
        failure_reason=None
    )
    db.add(audit)
    db.commit()
    db.refresh(alert)
    return alert
