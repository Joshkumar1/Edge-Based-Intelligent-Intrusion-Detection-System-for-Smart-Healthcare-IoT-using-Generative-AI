from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    devices,
    alerts,
    detection,
    dashboard,
    analytics,
    llm_assistant,
    documents,
    audit,
    signals
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(devices.router, prefix="/devices", tags=["Medical IoT Devices"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Intrusion Alerts"])
api_router.include_router(detection.router, prefix="/detection", tags=["Intrusion Detection Engine"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard Telemetry"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["ML Analytics"])
api_router.include_router(llm_assistant.router, prefix="/llm", tags=["Local LLM Assistant"])
api_router.include_router(documents.router, prefix="/documents", tags=["Research Documents & PDF RAG"])
api_router.include_router(audit.router, prefix="/audit", tags=["Security Audit Log"])
api_router.include_router(signals.router, prefix="/signals", tags=["Direct Machine Signals & Cyber Defense"])

