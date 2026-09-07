from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertOut, AlertUpdateStatus

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
def update_alert_status(alert_id: str, update_in: AlertUpdateStatus, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = update_in.status
    if update_in.resolved_by:
        alert.resolved_by = update_in.resolved_by
    alert.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(alert)
    return alert
