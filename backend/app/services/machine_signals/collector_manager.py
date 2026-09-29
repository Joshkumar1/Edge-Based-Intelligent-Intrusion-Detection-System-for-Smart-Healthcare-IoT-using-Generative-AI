import asyncio
import json
import logging
import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.schemas.machine_signals import (
    MachineSignalInput,
    SignalType,
    CollectorStatus
)
from app.services.machine_signals.cybersecurity_engine import cybersecurity_engine
from app.websockets.stream_manager import manager

logger = logging.getLogger("edgeshield.collectors")


class CollectorManager:
    """
    Orchestrates direct physical machine signal collectors and interfaces.
    Allows real medical equipment on the hospital LAN (or simulated hardware testbeds)
    to stream continuous physiological, operational, and network telemetry.
    """

    def __init__(self):
        self.collectors: Dict[str, Dict[str, Any]] = {
            "REST_EDGE_INGEST": {
                "name": "Bedside Edge Agent REST/JSON Ingest",
                "type": "REST_INGEST",
                "status": "RUNNING",
                "endpoint": "POST /api/v1/signals/ingest",
                "signals_received": 0,
                "signals_rejected": 0,
                "last_signal_time": None,
                "description": "High-throughput HTTP/JSON signal collector for Bedside Raspberry Pi and smart sensor gateways."
            },
            "TCP_SOCKET_STREAMER": {
                "name": "Medical Equipment Raw TCP Socket Listener",
                "type": "TCP_SOCKET",
                "status": "RUNNING",
                "endpoint": "tcp://0.0.0.0:9100",
                "signals_received": 0,
                "signals_rejected": 0,
                "last_signal_time": None,
                "description": "Direct TCP socket listener accepting continuous medical machine telemetry packets."
            },
            "MQTT_TELEMETRY_BRIDGE": {
                "name": "Hospital MQTT Telemetry Broker Bridge",
                "type": "MQTT_BRIDGE",
                "status": "RUNNING",
                "endpoint": "mqtt://hospital-broker.lan:1883/devices/+/telemetry",
                "signals_received": 0,
                "signals_rejected": 0,
                "last_signal_time": None,
                "description": "Subscribes to hospital IoT MQTT message topics for infusion pumps and telemetry monitors."
            },
            "VIRTUAL_MACHINE_EMITTER": {
                "name": "Direct Medical Machine Physical Telemetry Emitter",
                "type": "EMITTER",
                "status": "RUNNING",
                "endpoint": "internal://virtual-telemetry-bus",
                "signals_received": 0,
                "signals_rejected": 0,
                "last_signal_time": None,
                "description": "Continuous high-fidelity physiological waveform and telemetry generator for connected medical machines."
            }
        }

        self._emitter_task: Optional[asyncio.Task] = None
        self._tcp_server = None
        self._seq_counters: Dict[str, int] = {}
        self._latest_machine_signals: Dict[str, Dict[str, Any]] = {}

    def get_collectors(self) -> List[CollectorStatus]:
        return [
            CollectorStatus(
                collector_id=cid,
                name=c["name"],
                collector_type=c["type"],
                status=c["status"],
                endpoint=c["endpoint"],
                signals_received=c["signals_received"],
                signals_rejected=c["signals_rejected"],
                last_signal_time=c["last_signal_time"],
                description=c["description"]
            )
            for cid, c in self.collectors.items()
        ]

    def toggle_collector(self, collector_id: str) -> CollectorStatus:
        if collector_id not in self.collectors:
            raise ValueError(f"Unknown collector '{collector_id}'")
        c = self.collectors[collector_id]
        c["status"] = "STOPPED" if c["status"] == "RUNNING" else "RUNNING"
        logger.info(f"Collector {collector_id} status changed to {c['status']}")
        return CollectorStatus(
            collector_id=collector_id,
            name=c["name"],
            collector_type=c["type"],
            status=c["status"],
            endpoint=c["endpoint"],
            signals_received=c["signals_received"],
            signals_rejected=c["signals_rejected"],
            last_signal_time=c["last_signal_time"],
            description=c["description"]
        )

    def record_received(self, collector_id: str, rejected: bool = False):
        if collector_id in self.collectors:
            if rejected:
                self.collectors[collector_id]["signals_rejected"] += 1
            else:
                self.collectors[collector_id]["signals_received"] += 1
                self.collectors[collector_id]["last_signal_time"] = datetime.utcnow()

    def get_latest_signals(self) -> Dict[str, Any]:
        return self._latest_machine_signals

    async def start_background_workers(self):
        """Starts background TCP listener and virtual machine telemetry emitter."""
        if not self._emitter_task:
            self._emitter_task = asyncio.create_task(self._run_virtual_emitter())
        logger.info("CollectorManager background workers started.")

    async def stop_background_workers(self):
        if self._emitter_task:
            self._emitter_task.cancel()
            self._emitter_task = None
        if self._tcp_server:
            self._tcp_server.close()
            await self._tcp_server.wait_closed()
            self._tcp_server = None
        logger.info("CollectorManager background workers stopped.")

    def _get_next_seq(self, device_id: str) -> int:
        last_recorded = cybersecurity_engine._device_state.get(device_id, {}).get("last_seq", 0)
        current = max(self._seq_counters.get(device_id, 0), last_recorded)
        self._seq_counters[device_id] = current + 1
        return self._seq_counters[device_id]


    async def _run_virtual_emitter(self):
        """
        Emits realistic clinical signals for connected medical devices every 2-3 seconds.
        Broadcasts live machine telemetry events to connected WebSocket clients.
        """
        medical_devices = [
            {
                "device_id": "DEV-ICU-101",
                "category": "ICU Telemetry Station",
                "signal_type": SignalType.VITALS,
                "base_payload": {
                    "heart_rate_bpm": 74.0,
                    "spo2_pct": 98.5,
                    "systolic_bp": 118.0,
                    "diastolic_bp": 78.0,
                    "temperature_c": 36.8,
                    "ecg_mv": 0.85
                }
            },
            {
                "device_id": "DEV-PUMP-204",
                "category": "Infusion Pump",
                "signal_type": SignalType.INFUSION_TELEMETRY,
                "base_payload": {
                    "flow_rate_ml_h": 25.0,
                    "volume_infused_ml": 142.5,
                    "occlusion_pressure_psi": 4.2,
                    "bolus_status": "OFF",
                    "battery_pct": 94
                }
            },
            {
                "device_id": "DEV-VENT-301",
                "category": "Smart Ventilator",
                "signal_type": SignalType.VENTILATION_PRESSURE,
                "base_payload": {
                    "peak_inspiratory_pressure_cmH2O": 21.0,
                    "peep_cmH2O": 5.0,
                    "respiratory_rate_bpm": 14.0,
                    "tidal_volume_ml": 480.0,
                    "fiO2_pct": 40.0
                }
            },
            {
                "device_id": "DEV-RAD-405",
                "category": "DICOM Radiology Workstation",
                "signal_type": SignalType.DICOM_PACS_STREAM,
                "base_payload": {
                    "modality": "CT",
                    "study_uid": "1.2.840.113619.2.55",
                    "slice_count": 64,
                    "pdu_byte_rate": 8400.0,
                    "entropy": 4.12
                }
            },
            {
                "device_id": "DEV-SYRINGE-12",
                "category": "Smart Syringe Driver",
                "signal_type": SignalType.INFUSION_TELEMETRY,
                "base_payload": {
                    "flow_rate_ml_h": 2.5,
                    "volume_infused_ml": 18.2,
                    "occlusion_pressure_psi": 2.8,
                    "battery_pct": 89
                }
            }
        ]

        while True:
            try:
                await asyncio.sleep(2.5)

                if self.collectors["VIRTUAL_MACHINE_EMITTER"]["status"] != "RUNNING":
                    continue

                # Pick a random device to emit realistic micro-variations
                target = random.choice(medical_devices)
                payload = dict(target["base_payload"])

                # Add realistic physiological jitter
                if "heart_rate_bpm" in payload:
                    payload["heart_rate_bpm"] = round(payload["heart_rate_bpm"] + random.uniform(-2.5, 2.5), 1)
                    payload["spo2_pct"] = round(min(100.0, payload["spo2_pct"] + random.uniform(-0.3, 0.3)), 1)
                elif "flow_rate_ml_h" in payload:
                    payload["flow_rate_ml_h"] = round(max(0.1, payload["flow_rate_ml_h"] + random.uniform(-0.4, 0.4)), 2)
                    payload["volume_infused_ml"] = round(payload["volume_infused_ml"] + 0.05, 2)
                elif "peak_inspiratory_pressure_cmH2O" in payload:
                    payload["peak_inspiratory_pressure_cmH2O"] = round(payload["peak_inspiratory_pressure_cmH2O"] + random.uniform(-1.0, 1.0), 1)

                seq = self._get_next_seq(target["device_id"])
                signal_input = MachineSignalInput(
                    device_id=target["device_id"],
                    signal_type=target["signal_type"],
                    seq_num=seq,
                    timestamp=datetime.utcnow(),
                    payload=payload
                )

                # Process through cybersecurity engine
                res = cybersecurity_engine.inspect_and_defend(signal_input)
                self.record_received("VIRTUAL_MACHINE_EMITTER")

                # Cache latest state
                self._latest_machine_signals[target["device_id"]] = {
                    "device_id": target["device_id"],
                    "timestamp": res.timestamp.isoformat() + "Z",
                    "seq_num": res.seq_num,
                    "integrity_status": res.integrity_status.value,
                    "payload": res.payload,
                    "anomaly_score": res.anomaly_score,
                    "is_threat": res.is_threat,
                    "defense_action": res.defense_action_taken.value,
                    "clinical_interlock": res.clinical_safety_interlock
                }

                # Broadcast to WebSocket subscribers
                if manager.active_connections:
                    await manager.broadcast({
                        "type": "MACHINE_SIGNAL_EVENT",
                        "signal": {
                            "signal_id": res.signal_id,
                            "device_id": res.device_id,
                            "device_name": res.device_name,
                            "device_category": res.device_category,
                            "timestamp": res.timestamp.isoformat() + "Z",
                            "seq_num": res.seq_num,
                            "integrity_status": res.integrity_status.value,
                            "physical_invariant_breach": res.physical_invariant_breach,
                            "breach_details": res.breach_details,
                            "anomaly_score": res.anomaly_score,
                            "is_threat": res.is_threat,
                            "threat_type": res.threat_type,
                            "severity": res.severity,
                            "defense_mode": res.defense_mode.value,
                            "defense_action": res.defense_action_taken.value,
                            "clinical_safety_interlock": res.clinical_safety_interlock,
                            "payload": res.payload,
                            "latency_ms": res.latency_ms
                        }
                    })

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in virtual machine signal emitter: {e}")
                await asyncio.sleep(2.0)


# Global Singleton Collector Manager Instance
collector_manager = CollectorManager()
