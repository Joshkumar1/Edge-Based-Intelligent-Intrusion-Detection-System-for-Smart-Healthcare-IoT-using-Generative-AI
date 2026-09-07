from fastapi import APIRouter
from app.schemas.llm import ExplainRequest, ExplainResponse
from app.services.llm_service import llm_assistant

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def generate_explanation(req: ExplainRequest):
    explanation, impact, mitigation, engine = await llm_assistant.generate_explanation(
        threat_type=req.threat_type,
        severity=req.severity,
        source_ip=req.source_ip,
        target_device_name=req.target_device_name,
        target_device_type=req.target_device_type,
        location=req.location,
        key_features=req.key_features
    )
    
    return ExplainResponse(
        clinical_explanation=explanation,
        clinical_impact=impact,
        recommended_mitigation=mitigation,
        ai_engine_used=engine
    )
