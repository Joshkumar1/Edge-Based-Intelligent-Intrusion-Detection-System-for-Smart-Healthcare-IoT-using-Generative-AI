import pytest
import ipaddress
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.models.device import Device, DeviceStatus
from app.models.audit_log import AuditLog
from app.models.alert import Alert
from app.services.firewall_service import (
    HostFirewallAdapter,
    SimulationEnforcementAdapter,
    EnforcementResult,
    get_enforcement_adapter
)

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        # Ensure test users exist
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(
                username="admin",
                email="admin@test.lan",
                hashed_password=get_password_hash("admin123"),
                role="hospital_admin",
                is_active=True
            ))
        if not db.query(User).filter(User.username == "operator").first():
            db.add(User(
                username="operator",
                email="operator@test.lan",
                hashed_password=get_password_hash("operator123"),
                role="security_operator",
                is_active=True
            ))
        if not db.query(User).filter(User.username == "auditor").first():
            db.add(User(
                username="auditor",
                email="auditor@test.lan",
                hashed_password=get_password_hash("auditor123"),
                role="read_only_auditor",
                is_active=True
            ))
        if not db.query(User).filter(User.username == "inactive_user").first():
            db.add(User(
                username="inactive_user",
                email="inactive@test.lan",
                hashed_password=get_password_hash("inactive123"),
                role="security_operator",
                is_active=False
            ))
        db.commit()
        yield db
    finally:
        db.close()


def get_token(username: str) -> str:
    return create_access_token(subject=username)


def auth_headers(username: str) -> dict:
    return {"Authorization": f"Bearer {get_token(username)}"}


# =========================================================================
# 1. AUTHENTICATION TESTS
# =========================================================================

def test_missing_auth_header_rejected_401():
    """Unauthenticated requests to protected endpoints must return HTTP 401."""
    resp = client.post("/api/v1/devices/DEV-ICU-101/isolate")
    assert resp.status_code == 401
    assert "Authentication required" in resp.json()["detail"]


def test_malformed_auth_header_rejected_401():
    """Malformed or invalid authorization headers must return HTTP 401."""
    # Empty token after Bearer
    resp = client.post(
        "/api/v1/devices/DEV-ICU-101/isolate",
        headers={"Authorization": "Bearer "}
    )
    assert resp.status_code == 401

    # Garbage JWT string
    resp = client.post(
        "/api/v1/devices/DEV-ICU-101/isolate",
        headers={"Authorization": "Bearer not-a-valid-token-format"}
    )
    assert resp.status_code == 401


def test_invalid_signature_rejected_401():
    """Token signed with untrusted secret key must be rejected with HTTP 401."""
    fake_token = jwt.encode(
        {"sub": "admin", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "attacker-compromised-secret-key",
        algorithm="HS256"
    )
    resp = client.post(
        "/api/v1/devices/DEV-ICU-101/isolate",
        headers={"Authorization": f"Bearer {fake_token}"}
    )
    assert resp.status_code == 401
    assert "verification failed" in resp.json()["detail"].lower() or "invalid" in resp.json()["detail"].lower()


def test_expired_token_rejected_401():
    """Expired JWT tokens must return HTTP 401 Expired."""
    past_exp = datetime.now(timezone.utc) - timedelta(hours=2)
    expired_token = jwt.encode(
        {"sub": "admin", "exp": past_exp},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    resp = client.post(
        "/api/v1/devices/DEV-ICU-101/isolate",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert resp.status_code == 401
    assert "expired" in resp.json()["detail"].lower()


def test_valid_token_resolves_authenticated_user():
    """Valid JWT resolves authenticated user identity correctly."""
    headers = auth_headers("admin")
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "admin"
    assert data["role"] == "hospital_admin"
    assert data["is_active"] is True


def test_inactive_user_rejected_401(db_session):
    """Deactivated accounts must be rejected with HTTP 401 even with a valid signed token."""
    headers = auth_headers("inactive_user")
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 401
    assert "deactivated" in resp.json()["detail"].lower()


# =========================================================================
# 2. RBAC AUTHORIZATION TESTS
# =========================================================================

def test_read_only_auditor_forbidden_from_isolation():
    """Users with read_only_auditor role must receive HTTP 403 Forbidden on isolation."""
    headers = auth_headers("auditor")
    resp = client.post("/api/v1/devices/DEV-ICU-101/isolate", headers=headers)
    assert resp.status_code == 403
    assert "Access Denied" in resp.json()["detail"]


def test_read_only_auditor_forbidden_from_alert_triage():
    """Users with read_only_auditor role must receive HTTP 403 Forbidden on alert triage."""
    headers = auth_headers("auditor")
    resp = client.patch(
        "/api/v1/alerts/ALT-8A4F129B/status",
        json={"status": "RESOLVED", "resolved_by": "Compliance Auditor"},
        headers=headers
    )
    assert resp.status_code == 403
    assert "Access Denied" in resp.json()["detail"]


def test_security_operator_and_admin_permitted_isolation():
    """Security operators and admins are authorized to perform containment."""
    op_headers = auth_headers("operator")
    resp = client.post(
        "/api/v1/devices/DEV-VENT-301/isolate",
        json={"justification": "Modbus protocol anomaly detected during shift"},
        headers=op_headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["device_id"] == "DEV-VENT-301"
    assert data["status"] == "Isolated"
    assert data["performed_by"] == "operator"

    # Reconnect device
    rec_resp = client.post(
        "/api/v1/devices/DEV-VENT-301/reconnect",
        json={"justification": "Remediation verified clean"},
        headers=op_headers
    )
    assert rec_resp.status_code == 200
    assert rec_resp.json()["status"] == "Active"


# =========================================================================
# 3. ENFORCEMENT & ISOLATION STATE TESTS
# =========================================================================

def test_isolation_unknown_device_returns_404():
    """Attempting isolation on a non-existent device returns HTTP 404."""
    headers = auth_headers("admin")
    resp = client.post("/api/v1/devices/UNKNOWN-DEV-999/isolate", headers=headers)
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_truthful_simulation_enforcement_response():
    """Simulation mode must explicitly return SIMULATION and SIMULATED status."""
    headers = auth_headers("operator")
    resp = client.post(
        "/api/v1/devices/DEV-RAD-405/isolate",
        json={"justification": "Ransomware encryption risk mitigation"},
        headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    # Must explicitly state simulation, NOT claim real network firewall
    assert data["enforcement_mode"] == "SIMULATION"
    assert data["enforcement_status"] == "SIMULATED"
    assert "simulated" in data["enforcement_message"].lower()
    assert data["device_status"] == "Isolated"
    assert data["status"] == "Isolated"
    assert "audit_log_id" in data


def test_idempotent_isolation_and_reconnect():
    """Repeated isolation or reconnection requests must succeed idempotently."""
    headers = auth_headers("operator")

    # First isolate DEV-PUMP-204
    resp1 = client.post("/api/v1/devices/DEV-PUMP-204/isolate", headers=headers)
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "Isolated"

    # Second isolate on already isolated device (idempotent)
    resp2 = client.post("/api/v1/devices/DEV-PUMP-204/isolate", headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "Isolated"
    # Idempotent note should mention "already isolated"
    assert "already isolated" in resp2.json()["enforcement_message"].lower()

    # First reconnect DEV-PUMP-204
    rec1 = client.post("/api/v1/devices/DEV-PUMP-204/reconnect", headers=headers)
    assert rec1.status_code == 200
    assert rec1.json()["status"] == "Active"

    # Second reconnect on already active device (idempotent)
    rec2 = client.post("/api/v1/devices/DEV-PUMP-204/reconnect", headers=headers)
    assert rec2.status_code == 200
    assert rec2.json()["status"] == "Active"
    assert "already active" in rec2.json()["enforcement_message"].lower()


def test_failed_enforcement_does_not_falsely_update_device_state(monkeypatch, db_session):
    """If enforcement execution fails, the device status must NOT be updated to Isolated."""
    # Ensure device is Active
    dev = db_session.query(Device).filter(Device.device_id == "DEV-SYRINGE-12").first()
    dev.status = DeviceStatus.ACTIVE.value
    db_session.commit()

    class FailingAdapter(SimulationEnforcementAdapter):
        def isolate_device(self, device_ip, device_id):
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message="Mock iptables execution failed: Permission denied by kernel",
                details={"error_code": 13}
            )

    import app.api.v1.endpoints.devices as dev_mod
    monkeypatch.setattr(dev_mod, "enforcement_adapter", FailingAdapter())

    headers = auth_headers("operator")
    resp = client.post(
        "/api/v1/devices/DEV-SYRINGE-12/isolate",
        json={"justification": "Test enforcement failure safety"},
        headers=headers
    )
    assert resp.status_code == 502  # Bad Gateway for downstream enforcement failure
    assert "Enforcement failed" in resp.json()["detail"]

    # Verify device status was NOT changed in DB
    db_session.refresh(dev)
    assert dev.status == DeviceStatus.ACTIVE.value

    # Verify failure audit record was written
    failed_audit = db_session.query(AuditLog).filter(
        AuditLog.target_device_id == "DEV-SYRINGE-12",
        AuditLog.success == False
    ).order_by(AuditLog.id.desc()).first()
    assert failed_audit is not None
    assert failed_audit.enforcement_status == "FAILED"
    assert "Permission denied" in failed_audit.failure_reason


# =========================================================================
# 4. AUDIT LOGGING INTEGRITY TESTS
# =========================================================================

def test_audit_records_contain_full_context_and_no_secrets(db_session):
    """AuditLog records must capture actor, entity, states, and zero secrets."""
    headers = auth_headers("operator")
    client.post(
        "/api/v1/devices/DEV-ICU-101/isolate",
        json={"justification": "Routine isolation audit check"},
        headers=headers
    )

    audit_entry = db_session.query(AuditLog).filter(
        AuditLog.target_device_id == "DEV-ICU-101",
        AuditLog.action_type == "DEVICE_ISOLATION",
        AuditLog.success == True
    ).order_by(AuditLog.id.desc()).first()

    assert audit_entry is not None
    assert audit_entry.actor_username == "operator"
    assert audit_entry.actor_role == "security_operator"
    assert audit_entry.target_entity_type == "DEVICE"
    assert audit_entry.target_entity_id == "DEV-ICU-101"
    assert audit_entry.target_device_id == "DEV-ICU-101"
    assert audit_entry.new_state == "Isolated"
    assert audit_entry.timestamp is not None
    assert audit_entry.enforcement_mode == "SIMULATION"
    assert audit_entry.enforcement_status == "SIMULATED"
    assert audit_entry.impact_assessment == "Routine isolation audit check"

    # Security Verification: Ensure no passwords or raw JWTs are in the audit record
    all_audit_text = (
        f"{audit_entry.impact_assessment or ''} "
        f"{str(audit_entry.enforcement_result or '')} "
        f"{audit_entry.failure_reason or ''}"
    )
    assert "Bearer" not in all_audit_text
    assert "admin123" not in all_audit_text
    assert "operator123" not in all_audit_text
    assert settings.SECRET_KEY not in all_audit_text


def test_audit_log_query_endpoint():
    """Authorized operators can inspect audit logs via GET /api/v1/audit/."""
    headers = auth_headers("operator")
    resp = client.get("/api/v1/audit/?limit=10", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first = data[0]
    assert "audit_id" in first
    assert "actor_username" in first
    assert "action_type" in first


# =========================================================================
# 5. HOST FIREWALL ADAPTER SAFETY & VALIDATION TESTS
# =========================================================================

def test_host_firewall_adapter_ip_validation():
    """HostFirewallAdapter must validate IP format and reject injection payloads."""
    adapter = HostFirewallAdapter()

    # Valid IP format
    parsed = adapter.validate_ip("192.168.10.101")
    assert str(parsed) == "192.168.10.101"

    # Malformed IPs or shell injection attempts must raise ValueError
    with pytest.raises(ValueError, match="Invalid IP"):
        adapter.validate_ip("192.168.10.101; rm -rf /")

    with pytest.raises(ValueError, match="Invalid IP"):
        adapter.validate_ip("`reboot`")

    with pytest.raises(ValueError, match="Invalid IP"):
        adapter.validate_ip("999.999.999.999")


def test_host_firewall_adapter_deterministic_comment():
    """Comment tag must be deterministic and uniquely identify EdgeShield rules."""
    adapter = HostFirewallAdapter()
    comment = adapter.get_rule_comment("DEV-ICU-101")
    assert comment == "edgeshield-isolated-DEV-ICU-101"
    assert " " not in comment
