import random
import time
from typing import Dict, Any


class TrafficSimulator:
    def __init__(self):
        self.device_ips = [
            ("192.168.10.101", "DEV-ICU-101", "ICU Telemetry Station A", "ICU Wing B - Room 301"),
            ("192.168.10.102", "DEV-PUMP-204", "Alaris Infusion Pump #4", "Pediatrics - Room 104"),
            ("192.168.10.103", "DEV-VENT-301", "Puritan Bennett Ventilator", "ICU Wing A - Room 102"),
            ("192.168.10.104", "DEV-RAD-405", "Siemens DICOM Radiology Workstation", "Radiology Imaging Bay 2"),
            ("192.168.10.105", "DEV-SYRINGE-12", "Baxter Smart Syringe Driver", "Oncology Ward - Room 208")
        ]
        self.attacker_ips = [
            "10.0.4.88",
            "172.16.8.204",
            "192.168.10.250",
            "10.0.12.15"
        ]

    def generate_packet(self, force_attack: str = None) -> Dict[str, Any]:
        """
        Generates a synthetic network packet header & telemetry dictionary.
        Can be forced to generate a specific attack type or random realistic baseline.
        """
        target = random.choice(self.device_ips)
        dst_ip, device_id, device_name, location = target
        
        # Decide attack vs normal (85% normal baseline, 15% attack anomalies)
        attack_types = [
            "DICOM Ransomware",
            "MQTT Flood DoS",
            "Modbus Command Injection",
            "ARP Spoofing MITM",
            "Port Scan Reconnaissance"
        ]
        
        if force_attack:
            attack = force_attack
        else:
            is_attack = random.random() < 0.18
            attack = random.choice(attack_types) if is_attack else "Normal"

        src_ip = random.choice(self.attacker_ips) if attack != "Normal" else f"192.168.10.{random.randint(10, 90)}"

        if attack == "Normal":
            packet_len = random.normalvariate(350, 40)
            flow_dur = random.uniform(0.1, 4.0)
            header_len = 32
            byte_rate = random.normalvariate(500, 80)
            packet_rate = random.normalvariate(6, 2)
            tcp_syn = 0
            mqtt_rate = random.uniform(1.0, 5.0)
            modbus_code = random.choice([1, 2, 3, 4])
            entropy = random.normalvariate(3.8, 0.2)
            protocol = "MQTT" if "Pump" in device_name else ("DICOM" if "Radiology" in device_name else "Modbus")

        elif attack == "DICOM Ransomware":
            packet_len = random.normalvariate(1420, 50)
            flow_dur = random.uniform(15.0, 45.0)
            header_len = 40
            byte_rate = random.normalvariate(28000, 3000)
            packet_rate = random.normalvariate(85, 10)
            tcp_syn = 0
            mqtt_rate = 0.0
            modbus_code = 0
            entropy = random.normalvariate(7.85, 0.1)
            protocol = "DICOM"
            dst_ip = "192.168.10.104"  # Radiology Workstation
            device_id = "DEV-RAD-405"
            device_name = "Siemens DICOM Radiology Workstation"

        elif attack == "MQTT Flood DoS":
            packet_len = random.normalvariate(110, 15)
            flow_dur = random.uniform(0.01, 0.5)
            header_len = 20
            byte_rate = random.normalvariate(42000, 5000)
            packet_rate = random.normalvariate(380, 40)
            tcp_syn = 0
            mqtt_rate = random.normalvariate(420, 30)
            modbus_code = 0
            entropy = random.normalvariate(4.1, 0.2)
            protocol = "MQTT"
            dst_ip = "192.168.10.102"
            device_id = "DEV-PUMP-204"
            device_name = "Alaris Infusion Pump #4"

        elif attack == "Modbus Command Injection":
            packet_len = random.normalvariate(88, 10)
            flow_dur = random.uniform(0.05, 0.4)
            header_len = 20
            byte_rate = random.normalvariate(1250, 150)
            packet_rate = random.normalvariate(14, 2)
            tcp_syn = 0
            mqtt_rate = 0.0
            modbus_code = random.choice([5, 6, 16])
            entropy = random.normalvariate(2.85, 0.3)
            protocol = "Modbus"
            dst_ip = "192.168.10.103"
            device_id = "DEV-VENT-301"
            device_name = "Puritan Bennett Ventilator"

        elif attack == "ARP Spoofing MITM":
            packet_len = random.normalvariate(60, 5)
            flow_dur = random.uniform(0.02, 0.15)
            header_len = 14
            byte_rate = random.normalvariate(8500, 1000)
            packet_rate = random.normalvariate(130, 15)
            tcp_syn = 0
            mqtt_rate = 0.0
            modbus_code = 0
            entropy = random.normalvariate(2.1, 0.2)
            protocol = "ARP"

        else:  # Port Scan Reconnaissance
            packet_len = random.normalvariate(54, 2)
            flow_dur = random.uniform(0.001, 0.02)
            header_len = 40
            byte_rate = random.normalvariate(16000, 2000)
            packet_rate = random.normalvariate(260, 30)
            tcp_syn = 1
            mqtt_rate = 0.0
            modbus_code = 0
            entropy = random.normalvariate(1.8, 0.1)
            protocol = "TCP"

        return {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": random.randint(1024, 65535),
            "dst_port": 104 if protocol == "DICOM" else (1883 if protocol == "MQTT" else 502),
            "protocol": protocol,
            "packet_length": round(max(20.0, float(packet_len)), 2),
            "flow_duration": round(max(0.001, float(flow_dur)), 4),
            "header_length": max(14, int(header_len)),
            "byte_rate": round(max(0.0, float(byte_rate)), 2),
            "packet_rate": round(max(0.0, float(packet_rate)), 2),
            "tcp_syn_flag": int(tcp_syn),
            "mqtt_msg_rate": round(max(0.0, float(mqtt_rate)), 2),
            "modbus_fn_code": int(modbus_code),
            "entropy": round(min(8.0, max(0.0, float(entropy))), 2),
            "device_id": device_id,
            "device_name": device_name,
            "location": location
        }


traffic_simulator = TrafficSimulator()
