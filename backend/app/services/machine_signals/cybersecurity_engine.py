import time
import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.device import Device, DeviceStatus
from app.models.machine_signal import MachineSignalLog, ClinicalSafetyInterlock
from app.schemas.machine_signals import (
    MachineSignalInput,
    MachineSignalAnalysisResult,
    SignalIntegrityStatus,
    CyberDefenseMode,
    DefenseActionType,
    SignalType,
)
from app.schemas.security_event import TrafficOrigin
from app.services.security_pipeline import security_pipeline
from app.services.firewall_service import enforcement_adapter

logger = logging.getLogger("edgeshield.machine_cybersecurity")


class MachineSignalCybersecurityEngine:
    """
    Inner Development Cyber-Physical Security (CPS) Engine for Smart Healthcare IoT.
    Directly inspects physical machine signals, physiological parameters, anti-replay state,
    and correlates them with ML Intrusion Detection & Zero-Trust Cyber Defense Policies.
    """

    def __init__(self):
        # Maps device_id -> {"last_seq": int, "last_timestamp": datetime, "last_flow_rate": float, "last_pressure": float, "last_hr": float}
        self._device_state: Dict[str, Dict[str, Any]] = {}

        # Default Defense Policy
        self.defense_mode: CyberDefenseMode = CyberDefenseMode.ACTIVE_PREVENTION
        self.auto_isolate_critical: bool = True
        self.engage_safety_interlocks: bool = True
        self.anti_replay_enforcement: bool = True

        # Metrics
        self.total_signals_processed: int = 0
        self.total_breaches_detected: int = 0
        self.total_replay_attacks_blocked: int = 0
        self.total_interlocks_engaged: int = 0
        self.total_quarantines_enforced: int = 0

    def set_defense_mode(self, mode: CyberDefenseMode, auto_isolate: bool = True, interlocks: bool = True):
        self.defense_mode = mode
        self.auto_isolate_critical = auto_isolate
        self.engage_safety_interlocks = interlocks
        logger.info(f"Cyber Defense Mode updated to {mode.value} (Auto-isolate={auto_isolate}, Interlocks={interlocks})")

    def inspect_and_defend(
        self,
        signal: MachineSignalInput,
        db: Optional[Session] = None
    ) -> MachineSignalAnalysisResult:
        """
        Takes direct signal from a medical machine, validates physical & protocol invariants,
        detects cyber attacks (bolus overdose, barotrauma pressure hijack, sensor spoofing, replay),
        correlates with canonical ML pipeline, and executes active cyber defense.
        """
        t0 = time.perf_counter()
        signal_id = f"SIG-{uuid.uuid4().hex[:10].upper()}"
        now = signal.timestamp or datetime.utcnow()
        device_id = signal.device_id.strip()
        payload = signal.payload or {}
        net_meta = signal.network_meta or {}

        should_close_db = False
        if db is None:
            db = SessionLocal()
            should_close_db = True

        try:
            # 1. Resolve Target Machine
            device = db.query(Device).filter(Device.device_id == device_id).first()
            device_name = device.name if device else "External Medical Gateway"
            device_category = device.category if device else "Generic IoT Machine"
            device_ip = device.ip_address if device else (net_meta.get("dst_ip") or "192.168.10.100")

            # 2. Anti-Replay & Temporal Integrity Check
            integrity_status = SignalIntegrityStatus.VERIFIED
            breach_details: Optional[str] = None
            is_threat = False
            threat_type = "Normal"
            severity = "INFORMATIONAL"

            dev_state = self._device_state.setdefault(device_id, {
                "last_seq": 0,
                "last_timestamp": now,
                "last_flow_rate": None,
                "last_pressure": None,
                "last_hr": None
            })

            # Check sequence ordering if anti-replay enforcement is enabled
            if self.anti_replay_enforcement and signal.seq_num > 0:
                if signal.seq_num <= dev_state["last_seq"]:
                    integrity_status = SignalIntegrityStatus.REPLAY_ATTACK
                    is_threat = True
                    threat_type = "Signal Replay Attack"
                    severity = "HIGH"
                    breach_details = (
                        f"Anti-replay sequence violation: Received seq_num {signal.seq_num} <= "
                        f"previous sequence {dev_state['last_seq']}. Suspected signal replay attack."
                    )
                    self.total_replay_attacks_blocked += 1
                else:
                    dev_state["last_seq"] = signal.seq_num

            # 3. Physical & Physiological Invariant Validation (IEC 60601 / ISO/IEEE 11073)
            if not is_threat:
                invariant_ok, inv_threat, inv_severity, inv_reason = self._check_physical_invariants(
                    signal_type=signal.signal_type,
                    payload=payload,
                    device_category=device_category,
                    dev_state=dev_state
                )
                if not invariant_ok:
                    integrity_status = SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH
                    is_threat = True
                    threat_type = inv_threat
                    severity = inv_severity
                    breach_details = inv_reason
                    self.total_breaches_detected += 1

            # 4. Map to Canonical 9-Feature Space for Edge ML Pipeline
            ml_features = self._synthesize_ml_features(
                signal_type=signal.signal_type,
                payload=payload,
                net_meta=net_meta,
                is_threat=is_threat,
                threat_type=threat_type
            )

            # Ingest through Canonical ML Pipeline (Dual-stage Isolation Forest + XGBoost)
            pipeline_payload = {
                "src_ip": net_meta.get("src_ip", "10.0.4.88" if is_threat else "192.168.10.50"),
                "dst_ip": device_ip,
                "src_port": int(net_meta.get("src_port", 52100 if is_threat else 49152)),
                "dst_port": int(net_meta.get("dst_port", self._get_default_port(device_category))),
                "protocol": net_meta.get("protocol", self._get_default_protocol(device_category)),
                **ml_features
            }

            event = security_pipeline.ingest(
                telemetry=pipeline_payload,
                origin=TrafficOrigin.MACHINE_DIRECT,
                db=db
            )

            # Reconcile ML Detection with Physical Invariant Threat
            anomaly_score = max(float(event.anomaly_score), 0.95 if is_threat else 0.05)
            if not is_threat and event.anomaly_detected and event.threat_type != "Normal":
                is_threat = True
                threat_type = event.threat_type
                severity = event.severity
                breach_details = f"ML Anomaly Flagged: {event.threat_type} (Score: {anomaly_score:.2f})"
                integrity_status = SignalIntegrityStatus.ANOMALOUS_VALUE

            # 5. Active Cyber Defense Execution
            defense_action = DefenseActionType.NONE
            interlock_engaged = False
            enforcement_details: Dict[str, Any] = {}

            if is_threat:
                defense_action, interlock_engaged, enforcement_details = self._execute_cyber_defense(
                    device=device,
                    device_ip=device_ip,
                    threat_type=threat_type,
                    severity=severity,
                    signal_id=signal_id,
                    breach_details=breach_details or "",
                    db=db
                )

            # 6. Record Machine Signal Log
            log_record = MachineSignalLog(
                signal_id=signal_id,
                device_id=device_id,
                timestamp=now,
                signal_type=signal.signal_type.value,
                seq_num=signal.seq_num,
                integrity_status=integrity_status.value,
                physical_invariant_breach=1 if integrity_status == SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH else 0,
                breach_details=breach_details,
                anomaly_score=anomaly_score,
                is_threat=1 if is_threat else 0,
                threat_type=threat_type,
                severity=severity,
                defense_action=defense_action.value,
                clinical_interlock=1 if interlock_engaged else 0,
                payload_json=json.dumps(payload),
                alert_id=event.alert_id
            )
            db.add(log_record)
            db.commit()

            t1 = time.perf_counter()
            latency_ms = round((t1 - t0) * 1000.0, 3)
            self.total_signals_processed += 1

            return MachineSignalAnalysisResult(
                signal_id=signal_id,
                device_id=device_id,
                device_name=device_name,
                device_category=device_category,
                timestamp=now,
                seq_num=signal.seq_num,
                integrity_status=integrity_status,
                physical_invariant_breach=integrity_status == SignalIntegrityStatus.PHYSICAL_INVARIANT_BREACH,
                breach_details=breach_details,
                anomaly_score=anomaly_score,
                is_threat=is_threat,
                threat_type=threat_type,
                severity=severity,
                defense_mode=self.defense_mode,
                defense_action_taken=defense_action,
                clinical_safety_interlock=interlock_engaged,
                enforcement_details=enforcement_details,
                alert_id=event.alert_id,
                latency_ms=latency_ms,
                payload=payload
            )

        finally:
            if should_close_db:
                db.close()

    def _check_physical_invariants(
        self,
        signal_type: SignalType,
        payload: Dict[str, Any],
        device_category: str,
        dev_state: Dict[str, Any]
    ) -> Tuple[bool, str, str, Optional[str]]:
        """
        Validates clinical invariants across device classes.
        Returns: (is_valid, threat_type, severity, reason)
        """
        # A. Infusion Pump Invariants
        if signal_type == SignalType.INFUSION_TELEMETRY or "Infusion" in device_category or "Syringe" in device_category:
            rate = payload.get("flow_rate_ml_h")
            if rate is not None:
                rate = float(rate)
                if rate < 0.0:
                    return False, "Infusion Direction Inversion", "CRITICAL", f"Physical Invariant Breach: Negative flow rate {rate} mL/h attempted (reversed infusion pump motor)."
                if rate > 300.0:
                    return False, "Lethal Bolus Overdose Attack", "CRITICAL", f"Physical Invariant Breach: Flow rate {rate} mL/h exceeds maximum life-support threshold (300 mL/h)."
                
                # Check sudden rate step
                if dev_state["last_flow_rate"] is not None:
                    delta = abs(rate - dev_state["last_flow_rate"])
                    if delta > 150.0:
                        return False, "Infusion Step Surge Tampering", "HIGH", f"Physical Invariant Breach: Instantaneous rate jump of {delta:.1f} mL/h exceeds maximum pump acceleration limit."
                dev_state["last_flow_rate"] = rate

            occlusion_psi = payload.get("occlusion_pressure_psi")
            if occlusion_psi is not None and float(occlusion_psi) > 22.0:
                return False, "Line Occlusion Pressure Tamper", "HIGH", f"Physical Invariant Breach: Catheter pressure {occlusion_psi} PSI exceeds venous safety tolerance."

        # B. Ventilator Invariants
        elif signal_type == SignalType.VENTILATION_PRESSURE or "Ventilator" in device_category:
            pip = payload.get("peak_inspiratory_pressure_cmH2O")
            if pip is not None:
                pip = float(pip)
                if pip > 40.0:
                    return False, "Ventilator Barotrauma Hijack", "CRITICAL", f"Physical Invariant Breach: Airway pressure {pip} cmH2O exceeds barotrauma safety limit (40 cmH2O)."
                if pip < 3.0:
                    return False, "Ventilator Circuit Disconnect / Apnea Sabotage", "CRITICAL", f"Physical Invariant Breach: Airway pressure collapsed to {pip} cmH2O during active ventilation cycle."

            peep = payload.get("peep_cmH2O")
            if peep is not None and float(peep) < 1.0:
                return False, "PEEP Collapse Sabotage", "HIGH", f"Physical Invariant Breach: PEEP {peep} cmH2O causes alveolar collapse."

        # C. ICU Patient Monitor / Telemetry Invariants
        elif signal_type == SignalType.VITALS or "Monitor" in device_category or "Telemetry" in device_category:
            hr = payload.get("heart_rate_bpm")
            spo2 = payload.get("spo2_pct")
            if hr is not None and spo2 is not None:
                hr = float(hr)
                spo2 = float(spo2)
                # Sensor spoofing: reporting Asystole (HR=0) while SpO2 is completely normal (98%)
                if hr == 0 and spo2 >= 90.0:
                    return False, "Patient Monitor Sensor Deception", "HIGH", "Physical Invariant Breach: Physiological paradox detected — Heart Rate is 0 BPM while SpO2 pulse oximetry is 98%."
                if hr > 240.0:
                    return False, "Physiological Spoofing Injection", "HIGH", f"Physical Invariant Breach: Heart Rate {hr} BPM exceeds biological human electrical conduction limits."

        # D. DICOM Invariants
        elif signal_type == SignalType.DICOM_PACS_STREAM or "DICOM" in device_category:
            entropy = payload.get("entropy")
            byte_rate = payload.get("pdu_byte_rate") or payload.get("byte_rate")
            if entropy is not None and float(entropy) > 7.82 and byte_rate is not None and float(byte_rate) > 20000.0:
                return False, "DICOM Ransomware Encryption Burst", "CRITICAL", f"Physical Invariant Breach: High-entropy stream ({float(entropy):.2f}/8.0) transferring at {float(byte_rate)} B/s matches PACS ransomware encryption."

        # E. Modbus / SCADA Invariants
        elif signal_type == SignalType.MODBUS_SCADA_SIGNAL:
            fn_code = payload.get("modbus_fn_code")
            reg_val = payload.get("register_val")
            if fn_code in (5, 6, 16) and reg_val in (0xDEAD, 0xFFFF, 9999):
                return False, "Modbus Command Injection", "CRITICAL", f"Physical Invariant Breach: Unauthorized Modbus function {fn_code} written to life-safety register with payload {reg_val}."

        return True, "Normal", "INFORMATIONAL", None

    def _execute_cyber_defense(
        self,
        device: Optional[Device],
        device_ip: str,
        threat_type: str,
        severity: str,
        signal_id: str,
        breach_details: str,
        db: Session
    ) -> Tuple[DefenseActionType, bool, Dict[str, Any]]:
        """
        Executes active cybersecurity countermeasures according to configured defense mode.
        """
        enforcement_details: Dict[str, Any] = {"defense_mode": self.defense_mode.value}
        interlock_engaged = False

        if self.defense_mode == CyberDefenseMode.PASSIVE_MONITOR:
            logger.info(f"[PASSIVE_MONITOR] Logged threat '{threat_type}' on {device_ip}. No actions taken.")
            return DefenseActionType.LOG_ALERT, False, enforcement_details

        # For ASSISTED_DEFENSE or ACTIVE_PREVENTION:
        # Step 1: Engage Clinical Safety Interlock on Medical Equipment
        if self.engage_safety_interlocks and device:
            interlock = db.query(ClinicalSafetyInterlock).filter(
                ClinicalSafetyInterlock.device_id == device.device_id,
                ClinicalSafetyInterlock.is_active == True
            ).first()

            if not interlock:
                interlock = ClinicalSafetyInterlock(
                    device_id=device.device_id,
                    reason=f"{threat_type}: {breach_details}",
                    trigger_signal_id=signal_id,
                    safe_state_mode="LOCAL_BEDSIDE_OVERRIDE_LOCKED",
                    is_active=True
                )
                db.add(interlock)
                db.commit()
                self.total_interlocks_engaged += 1
                interlock_engaged = True
                logger.warning(f"[SAFETY_INTERLOCK] Engaged clinical fail-safe mode for {device.device_id} ({threat_type}).")
            enforcement_details["safety_interlock"] = "ENGAGED"

        if self.defense_mode == CyberDefenseMode.ASSISTED_DEFENSE:
            logger.info(f"[ASSISTED_DEFENSE] Interlock signaled; awaiting human authorization for firewall isolation.")
            return DefenseActionType.SAFETY_INTERLOCK_ENGAGED if interlock_engaged else DefenseActionType.LOG_ALERT, interlock_engaged, enforcement_details

        # Step 2: In ACTIVE_PREVENTION mode: Autonomous Edge Quarantine for Critical / High threats
        if self.defense_mode == CyberDefenseMode.ACTIVE_PREVENTION and self.auto_isolate_critical:
            if severity in ("CRITICAL", "HIGH") and device:
                try:
                    result = enforcement_adapter.isolate_device(device_ip=device_ip, device_id=device.device_id)
                    device.status = DeviceStatus.ISOLATED.value
                    db.commit()
                    self.total_quarantines_enforced += 1
                    enforcement_details["quarantine"] = {
                        "enforced": result.success,
                        "status": result.status,
                        "mode": result.mode,
                        "message": result.message
                    }
                    logger.critical(f"[ACTIVE_PREVENTION] Autonomous firewall quarantine enforced for {device.device_id} ({device_ip})!")
                    return DefenseActionType.FIREWALL_ISOLATE, interlock_engaged, enforcement_details
                except Exception as e:
                    logger.error(f"Failed to execute autonomous firewall isolation: {e}")
                    enforcement_details["quarantine_error"] = str(e)

        return DefenseActionType.SIGNAL_DROP, interlock_engaged, enforcement_details

    def _synthesize_ml_features(
        self,
        signal_type: SignalType,
        payload: Dict[str, Any],
        net_meta: Dict[str, Any],
        is_threat: bool,
        threat_type: str
    ) -> Dict[str, float]:
        """Maps physical and network parameters into the canonical 9 ML feature set."""
        features = {
            "packet_length": float(net_meta.get("packet_length", 350.0)),
            "flow_duration": float(net_meta.get("flow_duration", 2.0)),
            "header_length": float(net_meta.get("header_length", 32.0)),
            "byte_rate": float(net_meta.get("byte_rate", 450.0)),
            "packet_rate": float(net_meta.get("packet_rate", 5.0)),
            "tcp_syn_flag": int(net_meta.get("tcp_syn_flag", 0)),
            "mqtt_msg_rate": float(net_meta.get("mqtt_msg_rate", 1.0)),
            "modbus_fn_code": int(payload.get("modbus_fn_code", net_meta.get("modbus_fn_code", 3))),
            "entropy": float(payload.get("entropy", net_meta.get("entropy", 3.2)))
        }

        if is_threat:
            if "Ransomware" in threat_type or "DICOM" in threat_type:
                features["entropy"] = 7.91
                features["byte_rate"] = 29000.0
                features["packet_length"] = 1450.0
            elif "Flood" in threat_type or "DoS" in threat_type:
                features["mqtt_msg_rate"] = 420.0
                features["packet_rate"] = 380.0
            elif "Modbus" in threat_type or "Command" in threat_type:
                features["modbus_fn_code"] = 16
            elif "Port Scan" in threat_type:
                features["tcp_syn_flag"] = 1
                features["packet_rate"] = 120.0

        return features

    def _get_default_port(self, category: str) -> int:
        if "DICOM" in category:
            return 104
        if "Ventilator" in category or "SCADA" in category:
            return 502
        if "Infusion" in category or "Syringe" in category:
            return 1883
        return 8080

    def _get_default_protocol(self, category: str) -> str:
        if "DICOM" in category:
            return "DICOM"
        if "Ventilator" in category or "SCADA" in category:
            return "MODBUS"
        if "Infusion" in category or "Syringe" in category:
            return "MQTT"
        return "TCP"


# Global Singleton Engine Instance
cybersecurity_engine = MachineSignalCybersecurityEngine()
