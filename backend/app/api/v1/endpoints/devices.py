import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.device import Device, DeviceStatus
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.device import (
    DeviceOut,
    DeviceCreate,
    DeviceUpdate,
    DeviceIsolationRequest,
    DeviceEnforcementResponse
)
from app.api.deps import require_containment_privilege
from app.services.firewall_service import enforcement_adapter, get_enforcement_adapter

logger = logging.getLogger("edgeshield.devices")
router = APIRouter()


@router.get("/", response_model=List[DeviceOut])
def get_devices(db: Session = Depends(get_db)):
    """Lists all registered medical IoT devices in inventory."""
    return db.query(Device).all()


@router.post("/", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(
    device_in: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_containment_privilege)
):
    """Registers a new medical device in inventory. Requires operator/admin privileges."""
    existing = db.query(Device).filter(Device.device_id == device_in.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Device ID already registered.")
    
    device = Device(**device_in.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    logger.info(f"User '{current_user.username}' created device '{device.device_id}'.")
    return device


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """Retrieves metadata and current risk score for a specific medical device."""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found.")
    return device


@router.put("/{device_id}", response_model=DeviceOut)
def update_device(
    device_id: str,
    device_in: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_containment_privilege)
):
    """Updates device attributes. Requires operator/admin privileges."""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Device '{device_id}' not found.")
    
    update_data = device_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
        
    db.commit()
    db.refresh(device)
    logger.info(f"User '{current_user.username}' updated device '{device_id}'.")
    return device


@router.post("/{device_id}/isolate", response_model=DeviceEnforcementResponse)
def isolate_device(
    device_id: str,
    request: Request,
    isolation_req: Optional[DeviceIsolationRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_containment_privilege)
):
    """
    Executes network isolation containment for a medical device.
    Verifies operator authorization, runs enforcement adapter, creates immutable audit log,
    and updates device status ONLY upon successful enforcement.
    """
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Target device '{device_id}' not found.")

    prev_status = device.status
    client_ip = request.client.host if request.client else "unknown"
    audit_id = f"AUD-{uuid.uuid4().hex[:10].upper()}"
    now = datetime.now(timezone.utc)

    justification = isolation_req.justification if isolation_req else "Clinical threat mitigation"
    impact = (isolation_req.impact_assessment if isolation_req and isolation_req.impact_assessment != "Clinical telemetry isolation verified by operator"
              else justification)
    corr_id = isolation_req.correlation_id if isolation_req else None

    # Execute enforcement adapter
    enforce_res = enforcement_adapter.isolate_device(
        device_ip=device.ip_address,
        device_id=device.device_id
    )

    # If enforcement failed or unsupported, do NOT update device status to Isolated
    if not enforce_res.success:
        audit = AuditLog(
            audit_id=audit_id,
            actor_id=current_user.id,
            actor_username=current_user.username,
            actor_role=current_user.role,
            action_type="DEVICE_ISOLATION",
            target_entity_type="DEVICE",
            target_entity_id=device.device_id,
            target_device_id=device.device_id,
            previous_state=prev_status,
            new_state=prev_status,  # State unchanged
            impact_assessment=impact,
            timestamp=now,
            source_ip=client_ip,
            enforcement_mode=enforce_res.mode,
            enforcement_status=enforce_res.status,
            enforcement_result=enforce_res.details,
            success=False,
            failure_reason=enforce_res.message,
            correlation_id=corr_id
        )
        db.add(audit)
        db.commit()

        status_code = status.HTTP_502_BAD_GATEWAY
        if enforce_res.status == "UNSUPPORTED":
            status_code = status.HTTP_501_NOT_IMPLEMENTED

        raise HTTPException(
            status_code=status_code,
            detail=f"Enforcement failed: {enforce_res.message}"
        )

    # Enforcement succeeded -> update database state and create audit record atomically
    device.status = DeviceStatus.ISOLATED.value
    audit = AuditLog(
        audit_id=audit_id,
        actor_id=current_user.id,
        actor_username=current_user.username,
        actor_role=current_user.role,
        action_type="DEVICE_ISOLATION",
        target_entity_type="DEVICE",
        target_entity_id=device.device_id,
        target_device_id=device.device_id,
        previous_state=prev_status,
        new_state=DeviceStatus.ISOLATED.value,
        impact_assessment=impact,
        timestamp=now,
        source_ip=client_ip,
        enforcement_mode=enforce_res.mode,
        enforcement_status=enforce_res.status,
        enforcement_result=enforce_res.details,
        success=True,
        failure_reason=None,
        correlation_id=corr_id
    )
    db.add(audit)
    db.commit()
    db.refresh(device)
    db.refresh(audit)

    logger.info(
        f"Device '{device_id}' isolated by '{current_user.username}' "
        f"[Mode: {enforce_res.mode}, Status: {enforce_res.status}, Audit: {audit_id}]."
    )

    return DeviceEnforcementResponse(
        device_id=device.device_id,
        requested_action="isolate",
        device_status=device.status,
        status=device.status,
        enforcement_mode=enforce_res.mode,
        enforcement_status=enforce_res.status,
        enforcement_message=enforce_res.message,
        audit_log_id=audit.audit_id,
        performed_by=current_user.username,
        timestamp=now,
        device=DeviceOut.model_validate(device)
    )


@router.post("/{device_id}/reconnect", response_model=DeviceEnforcementResponse)
def reconnect_device(
    device_id: str,
    request: Request,
    reconnect_req: Optional[DeviceIsolationRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_containment_privilege)
):
    """
    Restores network communication for a previously isolated medical device.
    Verifies operator authorization, removes firewall quarantine rule, logs audit trail,
    and updates device status to Active.
    """
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Target device '{device_id}' not found.")

    prev_status = device.status
    client_ip = request.client.host if request.client else "unknown"
    audit_id = f"AUD-{uuid.uuid4().hex[:10].upper()}"
    now = datetime.now(timezone.utc)

    justification = reconnect_req.justification if reconnect_req else "Malware neutralized; restoring clinical communication"
    impact = reconnect_req.impact_assessment if reconnect_req else "Device reconnected to medical VLAN network"
    corr_id = reconnect_req.correlation_id if reconnect_req else None

    # Execute enforcement adapter
    enforce_res = enforcement_adapter.reconnect_device(
        device_ip=device.ip_address,
        device_id=device.device_id
    )

    if not enforce_res.success:
        audit = AuditLog(
            audit_id=audit_id,
            actor_id=current_user.id,
            actor_username=current_user.username,
            actor_role=current_user.role,
            action_type="DEVICE_RECONNECT",
            target_entity_type="DEVICE",
            target_entity_id=device.device_id,
            target_device_id=device.device_id,
            previous_state=prev_status,
            new_state=prev_status,
            impact_assessment=impact,
            timestamp=now,
            source_ip=client_ip,
            enforcement_mode=enforce_res.mode,
            enforcement_status=enforce_res.status,
            enforcement_result=enforce_res.details,
            success=False,
            failure_reason=enforce_res.message,
            correlation_id=corr_id
        )
        db.add(audit)
        db.commit()

        status_code = status.HTTP_502_BAD_GATEWAY
        if enforce_res.status == "UNSUPPORTED":
            status_code = status.HTTP_501_NOT_IMPLEMENTED

        raise HTTPException(
            status_code=status_code,
            detail=f"Enforcement failed: {enforce_res.message}"
        )

    # Enforcement succeeded -> update database state and create audit record atomically
    device.status = DeviceStatus.ACTIVE.value
    audit = AuditLog(
        audit_id=audit_id,
        actor_id=current_user.id,
        actor_username=current_user.username,
        actor_role=current_user.role,
        action_type="DEVICE_RECONNECT",
        target_entity_type="DEVICE",
        target_entity_id=device.device_id,
        target_device_id=device.device_id,
        previous_state=prev_status,
        new_state=DeviceStatus.ACTIVE.value,
        impact_assessment=impact,
        timestamp=now,
        source_ip=client_ip,
        enforcement_mode=enforce_res.mode,
        enforcement_status=enforce_res.status,
        enforcement_result=enforce_res.details,
        success=True,
        failure_reason=None,
        correlation_id=corr_id
    )
    db.add(audit)
    db.commit()
    db.refresh(device)
    db.refresh(audit)

    logger.info(
        f"Device '{device_id}' reconnected by '{current_user.username}' "
        f"[Mode: {enforce_res.mode}, Status: {enforce_res.status}, Audit: {audit_id}]."
    )

    return DeviceEnforcementResponse(
        device_id=device.device_id,
        requested_action="reconnect",
        device_status=device.status,
        status=device.status,
        enforcement_mode=enforce_res.mode,
        enforcement_status=enforce_res.status,
        enforcement_message=enforce_res.message,
        audit_log_id=audit.audit_id,
        performed_by=current_user.username,
        timestamp=now,
        device=DeviceOut.model_validate(device)
    )
