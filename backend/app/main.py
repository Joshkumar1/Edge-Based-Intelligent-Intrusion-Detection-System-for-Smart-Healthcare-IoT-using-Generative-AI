import asyncio
import uuid
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.api.v1.router import api_router
from app.websockets.stream_manager import manager
from app.models.device import Device, DeviceCategory, DeviceStatus
from app.models.alert import Alert
from app.models.user import User
from app.models.audit_log import AuditLog
from app.core.security import get_password_hash
from app.services.traffic_sim import traffic_simulator
from app.services.security_pipeline import security_pipeline
from app.services.machine_signals import collector_manager
from app.schemas.security_event import TrafficOrigin



def seed_initial_data(db: Session):
    """Populates baseline hospital devices and realistic intrusion alerts if DB is empty."""
    if db.query(Device).count() == 0:
        devices = [
            Device(
                device_id="DEV-ICU-101",
                name="ICU Telemetry Station A",
                category=DeviceCategory.ICU_TELEMETRY.value,
                ip_address="192.168.10.101",
                mac_address="00:1A:2B:3C:4D:5E",
                location="ICU Wing B - Room 301",
                firmware_version="v4.2.1-sec",
                status=DeviceStatus.ACTIVE.value,
                risk_score=12.0,
                protocol="Modbus/TCP"
            ),
            Device(
                device_id="DEV-PUMP-204",
                name="Alaris Infusion Pump #4",
                category=DeviceCategory.INFUSION_PUMP.value,
                ip_address="192.168.10.102",
                mac_address="00:1A:2B:99:88:77",
                location="Pediatrics - Room 104",
                firmware_version="v2.1.0",
                status=DeviceStatus.WARNING.value,
                risk_score=68.5,
                protocol="MQTT"
            ),
            Device(
                device_id="DEV-VENT-301",
                name="Puritan Bennett Ventilator",
                category=DeviceCategory.VENTILATOR.value,
                ip_address="192.168.10.103",
                mac_address="00:1A:2B:44:55:66",
                location="ICU Wing A - Room 102",
                firmware_version="v3.0.4",
                status=DeviceStatus.ACTIVE.value,
                risk_score=5.0,
                protocol="Modbus"
            ),
            Device(
                device_id="DEV-RAD-405",
                name="Siemens DICOM Radiology Workstation",
                category=DeviceCategory.DICOM_GATEWAY.value,
                ip_address="192.168.10.104",
                mac_address="00:1A:2B:11:22:33",
                location="Radiology Imaging Bay 2",
                firmware_version="v5.1.2",
                status=DeviceStatus.CRITICAL.value,
                risk_score=94.0,
                protocol="DICOM"
            ),
            Device(
                device_id="DEV-SYRINGE-12",
                name="Baxter Smart Syringe Driver",
                category=DeviceCategory.SMART_SYRINGE.value,
                ip_address="192.168.10.105",
                mac_address="00:1A:2B:77:66:55",
                location="Oncology Ward - Room 208",
                firmware_version="v1.8.4",
                status=DeviceStatus.ACTIVE.value,
                risk_score=18.0,
                protocol="MQTT"
            )
        ]
        db.add_all(devices)
        db.commit()
        print("[+] Seeded initial hospital medical devices.")

    if db.query(Alert).count() == 0:
        sample_alerts = [
            Alert(
                alert_id="ALT-8A4F129B",
                timestamp=datetime.utcnow() - timedelta(minutes=14),
                source_ip="172.16.8.204",
                destination_ip="192.168.10.104",
                target_device_id="DEV-RAD-405",
                protocol="DICOM",
                anomaly_score=0.94,
                is_anomaly=1,
                threat_type="DICOM Ransomware",
                confidence=0.96,
                severity="CRITICAL",
                key_features={"packet_length": 1450.0, "byte_rate": 28500.0, "entropy": 7.88},
                clinical_explanation="An unauthorized external host (172.16.8.204) is transferring highly encrypted payload data (Byte Entropy: 7.88/8.0) into the Siemens DICOM Radiology Workstation at Radiology Imaging Bay 2. This pattern matches ransomware targeting PACS radiology image repositories.",
                clinical_impact="High patient care risk: Ransomware encryption could lock radiology scans (CT/MRI), delaying emergency surgical procedures and compromising patient medical history integrity.",
                recommended_mitigation="1. Instantly isolate Siemens DICOM Radiology Workstation at network switch VLAN boundary.\n2. Block TCP port 104 and incoming traffic from host 172.16.8.204.\n3. Verify shadow volume backups for DICOM imaging repositories before rebooting.",
                status="NEW"
            ),
            Alert(
                alert_id="ALT-3C9D77E1",
                timestamp=datetime.utcnow() - timedelta(minutes=42),
                source_ip="10.0.4.88",
                destination_ip="192.168.10.102",
                target_device_id="DEV-PUMP-204",
                protocol="MQTT",
                anomaly_score=0.72,
                is_anomaly=1,
                threat_type="MQTT Flood DoS",
                confidence=0.89,
                severity="HIGH",
                key_features={"mqtt_msg_rate": 415.0, "packet_rate": 370.0},
                clinical_explanation="A massive surge of telemetry messages (415 msgs/sec) is flooding the MQTT broker connected to Alaris Infusion Pump #4 at Pediatrics - Room 104. This Denial of Service packet burst is exhausting processing bandwidth.",
                clinical_impact="Operational risk: Infusion pump rate adjustments or telemetry alarm alerts may experience severe latency, preventing nursing staff from receiving real-time patient medication updates.",
                recommended_mitigation="1. Enable rate limiting on MQTT broker for IP 10.0.4.88.\n2. Force re-authentication of all IoT client publish certificates.\n3. Verify physical patient infusion pump state at Pediatrics - Room 104.",
                status="INVESTIGATING"
            )
        ]
        db.add_all(sample_alerts)
        db.commit()
        print("[+] Seeded initial baseline security alerts.")

    if db.query(User).count() == 0:
        users = [
            User(
                username="admin",
                email="admin@edgeshield.hospital.lan",
                full_name="Hospital Chief Security Admin",
                hashed_password=get_password_hash("admin123"),
                role="hospital_admin",
                is_active=True
            ),
            User(
                username="operator",
                email="operator@edgeshield.hospital.lan",
                full_name="Lead Security Operator",
                hashed_password=get_password_hash("operator123"),
                role="security_operator",
                is_active=True
            ),
            User(
                username="auditor",
                email="auditor@edgeshield.hospital.lan",
                full_name="Compliance Auditor",
                hashed_password=get_password_hash("auditor123"),
                role="read_only_auditor",
                is_active=True
            ),
        ]
        db.add_all(users)
        db.commit()
        print("[+] Seeded initial security users (admin, operator, auditor).")


async def live_telemetry_stream():
    """Background loop feeding live telemetry through the canonical security pipeline."""
    while True:
        await asyncio.sleep(2.0)
        if manager.active_connections:
            try:
                simulated = traffic_simulator.generate_packet()
                # Run through the canonical security pipeline
                security_pipeline.ingest(simulated, origin=TrafficOrigin.LIVE)
            except Exception:
                pass



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
        
    stream_task = asyncio.create_task(live_telemetry_stream())
    await collector_manager.start_background_workers()
    yield
    # Shutdown
    stream_task.cancel()
    await collector_manager.stop_background_workers()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "subtitle": "Intelligent Edge-Based Intrusion Detection for Smart Healthcare IoT",
        "status": "OPERATIONAL",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or process incoming commands if needed
            await websocket.send_json({"status": "received", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
