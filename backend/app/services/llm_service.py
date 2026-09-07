import httpx
import json
from typing import Dict, Any, Tuple
from app.core.config import settings


class LLMAssistantService:
    def __init__(self):
        self.ollama_url = settings.OLLAMA_BASE_URL
        self.model_name = settings.OLLAMA_MODEL

    async def generate_explanation(
        self,
        threat_type: str,
        severity: str,
        source_ip: str,
        target_device_name: str,
        target_device_type: str,
        location: str,
        key_features: Dict[str, float]
    ) -> Tuple[str, str, str, str]:
        """
        Generates human-readable clinical explanation, impact analysis, and mitigation steps.
        Tries local Ollama LLM first; falls back to EdgeShield Deterministic Explanation Engine if unavailable.
        Returns:
            (clinical_explanation, clinical_impact, recommended_mitigation, ai_engine_used)
        """
        prompt = self._build_prompt(
            threat_type=threat_type,
            severity=severity,
            source_ip=source_ip,
            target_device_name=target_device_name,
            target_device_type=target_device_type,
            location=location,
            key_features=key_features
        )

        try:
            async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "")
                    parsed = json.loads(response_text)
                    
                    return (
                        parsed.get("clinical_explanation", ""),
                        parsed.get("clinical_impact", ""),
                        parsed.get("recommended_mitigation", ""),
                        f"Ollama Local ({self.model_name})"
                    )
        except Exception as e:
            # Fallback to local rule engine if Ollama is not active
            pass

        # Deterministic Expert Rule Synthesis Engine
        explanation, impact, mitigation = self._deterministic_expert_rules(
            threat_type=threat_type,
            severity=severity,
            source_ip=source_ip,
            target_device_name=target_device_name,
            target_device_type=target_device_type,
            location=location,
            key_features=key_features
        )
        return explanation, impact, mitigation, "EdgeShield Local Security Expert Engine"

    def _build_prompt(
        self,
        threat_type: str,
        severity: str,
        source_ip: str,
        target_device_name: str,
        target_device_type: str,
        location: str,
        key_features: Dict[str, float]
    ) -> str:
        return f"""
System: You are EdgeShield AI, a Senior Medical IoT Cybersecurity Specialist working inside a Smart Hospital.
Explain this cyber attack clearly for hospital IT administrators and biomedical engineers.

Incident Data:
- Threat Classification: {threat_type}
- Severity Level: {severity}
- Attacker Source IP: {source_ip}
- Target Device Name: {target_device_name} ({target_device_type})
- Location: {location}
- Key Telemetry Features: {json.dumps(key_features)}

Respond STRICTLY with a valid JSON object matching this schema:
{{
  "clinical_explanation": "2-3 sentences explaining what this attack is in plain language without jargon.",
  "clinical_impact": "2-3 sentences describing potential risks to patient safety, device operation, or hospital workflow.",
  "recommended_mitigation": "Numbered step-by-step technical and operational containment instructions."
}}
"""

    def _deterministic_expert_rules(
        self,
        threat_type: str,
        severity: str,
        source_ip: str,
        target_device_name: str,
        target_device_type: str,
        location: str,
        key_features: Dict[str, float]
    ) -> Tuple[str, str, str]:
        """
        High-precision expert rules synthesized for medical IoT security.
        """
        entropy = key_features.get("entropy", 0.0)
        mqtt_rate = key_features.get("mqtt_msg_rate", 0.0)
        modbus_code = key_features.get("modbus_fn_code", 0)

        if threat_type == "DICOM Ransomware":
            explanation = (
                f"An unauthorized external host ({source_ip}) is transferring highly encrypted payload data "
                f"(Byte Entropy: {entropy:.2f}/8.0) into the {target_device_name} workstation at {location}. "
                f"This pattern matches ransomware targeting PACS radiology image repositories."
            )
            impact = (
                f"High patient care risk: Ransomware encryption could lock radiology scans (CT/MRI), "
                f"delaying emergency surgical procedures and compromising patient medical history integrity."
            )
            mitigation = (
                f"1. Instantly isolate {target_device_name} at network switch VLAN boundary.\n"
                f"2. Block TCP port 104 and incoming traffic from host {source_ip}.\n"
                f"3. Verify shadow volume backups for DICOM imaging repositories before rebooting."
            )

        elif threat_type == "MQTT Flood DoS":
            explanation = (
                f"A massive surge of telemetry messages ({mqtt_rate:.0f} msgs/sec) is flooding the MQTT broker "
                f"connected to {target_device_name} at {location}. This Denal of Service packet burst is exhausting processing bandwidth."
            )
            impact = (
                f"Operational risk: Infusion pump rate adjustments or telemetry alarm alerts may experience severe "
                f"latency, preventing nursing staff from receiving real-time patient medication updates."
            )
            mitigation = (
                f"1. Enable rate limiting on MQTT broker for IP {source_ip}.\n"
                f"2. Force re-authentication of all IoT client publish certificates.\n"
                f"3. Verify physical patient infusion pump state at {location}."
            )

        elif threat_type == "Modbus Command Injection":
            explanation = (
                f"An anomalous Modbus write command (Function Code {modbus_code}) was intercepted from {source_ip} "
                f"directed at {target_device_name} at {location}. Normal operations only execute read commands."
            )
            impact = (
                f"Critical Patient Hazard: Direct modification of ventilator parameters or telemetry alarm thresholds "
                f"could alter oxygen delivery rates or silence critical ICU alerts."
            )
            mitigation = (
                f"1. Immediately block Modbus write function codes (5, 6, 15, 16) at the industrial edge firewall.\n"
                f"2. Isolate IP {source_ip} from the medical device subnet.\n"
                f"3. Initiate immediate biomedical engineering manual verification on {target_device_name}."
            )

        elif threat_type == "ARP Spoofing MITM":
            explanation = (
                f"A host at {source_ip} is sending forged ARP broadcast packets, attempting to position itself between "
                f"{target_device_name} and the hospital central monitoring server."
            )
            impact = (
                f"Privacy & Integrity Risk: Man-in-the-Middle eavesdropping allows attackers to capture unencrypted "
                f"vitals data or manipulate telemetry values displayed on central nursing station monitors."
            )
            mitigation = (
                f"1. Enable Dynamic ARP Inspection (DAI) on switch access ports at {location}.\n"
                f"2. Clear ARP caches on central gateways and bind static MAC-to-IP pairings.\n"
                f"3. Quarantine MAC address associated with IP {source_ip}."
            )

        elif threat_type == "Port Scan Reconnaissance":
            explanation = (
                f"Automated port scanning originating from {source_ip} is probing TCP ports across the medical device subnet, "
                f"targeting {target_device_name}."
            )
            impact = (
                f"Low immediate patient risk, but indicates an active reconnaissance phase preceding a targeted attack on vulnerable IoT services."
            )
            mitigation = (
                f"1. Add IP {source_ip} to edge firewall drop list.\n"
                f"2. Audit open TCP/UDP ports on {target_device_name}.\n"
                f"3. Verify device password credentials and disable unused management protocols (e.g. Telnet, HTTP)."
            )

        else:
            explanation = f"Anomalous traffic detected targeting {target_device_name} from source {source_ip}."
            impact = f"Potential service degradation or unauthorized access risk."
            mitigation = f"1. Inspect raw packet logs.\n2. Monitor device telemetry for anomalous restarts."

        return explanation, impact, mitigation


llm_assistant = LLMAssistantService()
