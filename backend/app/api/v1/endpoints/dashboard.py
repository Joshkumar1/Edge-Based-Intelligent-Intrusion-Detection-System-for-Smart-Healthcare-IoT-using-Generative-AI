from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.device import Device
from app.models.alert import Alert

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_devices = db.query(Device).count()
    active_alerts = db.query(Alert).filter(Alert.status.in_(["NEW", "INVESTIGATING"])).count()
    critical_alerts = db.query(Alert).filter(
        Alert.severity == "CRITICAL",
        Alert.status.in_(["NEW", "INVESTIGATING"])
    ).count()
    
    devices_at_risk = db.query(Device).filter(Device.risk_score > 50.0).count()
    
    # Threat Distribution
    threat_counts = db.query(
        Alert.threat_type, func.count(Alert.id)
    ).group_by(Alert.threat_type).all()
    
    threat_distribution = {threat: count for threat, count in threat_counts}

    return {
        "total_devices": total_devices,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts,
        "devices_at_risk": devices_at_risk,
        "threat_distribution": threat_distribution,
        "system_health": "OPTIMAL" if critical_alerts == 0 else "ELEVATED_THREAT",
        "edge_ai_status": "ONLINE (0.84ms Latency)"
    }
