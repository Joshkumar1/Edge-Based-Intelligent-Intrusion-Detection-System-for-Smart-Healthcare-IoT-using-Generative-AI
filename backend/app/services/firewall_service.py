import os
import shutil
import platform
import subprocess
import ipaddress
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger("edgeshield.firewall")


@dataclass
class EnforcementResult:
    success: bool
    mode: str  # "HOST_FIREWALL" | "SIMULATION"
    status: str  # "ENFORCED" | "SIMULATED" | "FAILED" | "UNSUPPORTED"
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


class EnforcementAdapter(ABC):
    """Abstract interface for EdgeShield network isolation adapters."""

    @abstractmethod
    def isolate_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        """Applies network quarantine rule blocking device IP communication."""
        pass

    @abstractmethod
    def reconnect_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        """Removes previously applied network quarantine rule for device IP."""
        pass

    @abstractmethod
    def verify_isolated(self, device_ip: str, device_id: str) -> bool:
        """Verifies whether the quarantine rule currently exists in the firewall state."""
        pass


class HostFirewallAdapter(EnforcementAdapter):
    """
    Real OS-level Linux firewall controller (iptables / nftables).
    Applies deterministic, commented DROP rules with verification, timeouts, and idempotency.
    """

    def __init__(
        self,
        backend: str = "iptables",
        chain: str = "FORWARD",
        timeout_seconds: int = 5
    ):
        self.backend = backend.lower()
        self.chain = chain.upper()
        self.timeout = timeout_seconds
        self.is_linux = platform.system().lower() == "linux"

    def validate_ip(self, ip_str: str) -> str:
        """Validates IP format using standard ipaddress parser to prevent command injection."""
        try:
            parsed = ipaddress.ip_address(ip_str.strip())
            return str(parsed)
        except Exception as e:
            raise ValueError(f"Invalid IP address '{ip_str}': {str(e)}")

    def _validate_ip(self, ip_str: str) -> str:
        return self.validate_ip(ip_str)

    def get_rule_comment(self, device_id: str) -> str:
        safe_id = "".join(c for c in device_id if c.isalnum() or c in "-_")
        return f"edgeshield-isolated-{safe_id}"

    def _get_comment(self, device_id: str) -> str:
        return self.get_rule_comment(device_id)

    def _check_binary(self) -> Optional[str]:
        bin_path = shutil.which(self.backend)
        return bin_path

    def _build_rule_spec(self, ip: str, device_id: str) -> list[str]:
        comment = self._get_comment(device_id)
        return ["-s", ip, "-m", "comment", "--comment", comment, "-j", "DROP"]

    def isolate_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        if not self.is_linux:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="UNSUPPORTED",
                message=(
                    f"Host firewall enforcement is unsupported on platform '{platform.system()}'. "
                    f"Set EDGE_ENFORCEMENT_MODE=simulation for development."
                ),
                details={"platform": platform.system()}
            )

        bin_path = self._check_binary()
        if not bin_path:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="UNSUPPORTED",
                message=f"Firewall utility '{self.backend}' not found on PATH.",
                details={"backend": self.backend}
            )

        try:
            clean_ip = self._validate_ip(device_ip)
        except ValueError as ve:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message=str(ve),
                details={"invalid_ip": device_ip}
            )

        rule_spec = self._build_rule_spec(clean_ip, device_id)

        # Idempotency check: does rule already exist?
        check_cmd = [bin_path, "-C", self.chain] + rule_spec
        try:
            res_check = subprocess.run(
                check_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if res_check.returncode == 0:
                logger.info(f"Firewall rule for {device_id} ({clean_ip}) already active (idempotent).")
                return EnforcementResult(
                    success=True,
                    mode="HOST_FIREWALL",
                    status="ENFORCED",
                    message=f"Device {device_id} ({clean_ip}) quarantine verified active in {self.chain} chain (idempotent).",
                    details={"already_present": True, "chain": self.chain}
                )
        except Exception as e:
            logger.warning(f"Idempotency check exception: {e}")

        # Insert rule at top of chain
        insert_cmd = [bin_path, "-I", self.chain, "1"] + rule_spec
        try:
            exec_res = subprocess.run(
                insert_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            if exec_res.returncode != 0:
                logger.error(f"Firewall execution failed: {exec_res.stderr.strip()}")
                return EnforcementResult(
                    success=False,
                    mode="HOST_FIREWALL",
                    status="FAILED",
                    message=f"Host firewall rule insertion returned non-zero code {exec_res.returncode}.",
                    details={"stderr": exec_res.stderr.strip(), "stdout": exec_res.stdout.strip()}
                )
        except subprocess.TimeoutExpired:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message=f"Firewall command timed out after {self.timeout}s.",
                details={"timeout_seconds": self.timeout}
            )
        except Exception as e:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message=f"Subprocess invocation failure: {str(e)}",
                details={"error": str(e)}
            )

        # Post-condition verification
        verified = self.verify_isolated(clean_ip, device_id)
        if not verified:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message="Firewall command succeeded but post-condition check failed to verify rule existence.",
                details={"chain": self.chain}
            )

        return EnforcementResult(
            success=True,
            mode="HOST_FIREWALL",
            status="ENFORCED",
            message=f"Device {device_id} ({clean_ip}) successfully isolated via host {self.backend} in chain {self.chain}.",
            details={"chain": self.chain, "ip": clean_ip, "verified": True}
        )

    def reconnect_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        if not self.is_linux:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="UNSUPPORTED",
                message=f"Host firewall is unsupported on '{platform.system()}'.",
                details={"platform": platform.system()}
            )

        bin_path = self._check_binary()
        if not bin_path:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="UNSUPPORTED",
                message=f"Firewall utility '{self.backend}' not found on PATH.",
                details={"backend": self.backend}
            )

        try:
            clean_ip = self._validate_ip(device_ip)
        except ValueError as ve:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message=str(ve),
                details={"invalid_ip": device_ip}
            )

        rule_spec = self._build_rule_spec(clean_ip, device_id)

        # Delete rule
        del_cmd = [bin_path, "-D", self.chain] + rule_spec
        try:
            exec_res = subprocess.run(
                del_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            # Code 0 = removed, Code 1 = rule not found (idempotent success)
            if exec_res.returncode not in (0, 1):
                return EnforcementResult(
                    success=False,
                    mode="HOST_FIREWALL",
                    status="FAILED",
                    message=f"Rule removal error: {exec_res.stderr.strip()}",
                    details={"stderr": exec_res.stderr.strip()}
                )
        except Exception as e:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message=f"Subprocess deletion failure: {str(e)}",
                details={"error": str(e)}
            )

        # Verify rule is gone
        verified_removed = not self.verify_isolated(clean_ip, device_id)
        if not verified_removed:
            return EnforcementResult(
                success=False,
                mode="HOST_FIREWALL",
                status="FAILED",
                message="Post-condition verification failed: rule is still active in chain.",
                details={"chain": self.chain}
            )

        return EnforcementResult(
            success=True,
            mode="HOST_FIREWALL",
            status="ENFORCED",
            message=f"Device {device_id} ({clean_ip}) firewall quarantine rule removed from {self.chain} chain.",
            details={"chain": self.chain, "ip": clean_ip, "verified": True}
        )

    def verify_isolated(self, device_ip: str, device_id: str) -> bool:
        bin_path = self._check_binary()
        if not bin_path or not self.is_linux:
            return False

        try:
            clean_ip = self._validate_ip(device_ip)
            check_cmd = [bin_path, "-C", self.chain] + self._build_rule_spec(clean_ip, device_id)
            res = subprocess.run(
                check_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return res.returncode == 0
        except Exception:
            return False


class SimulationEnforcementAdapter(EnforcementAdapter):
    """
    Simulation enforcement adapter for development, testing, and macOS/Windows workstations.
    Transparently reports SIMULATED status without claiming real OS firewall modifications.
    """

    def __init__(self):
        self._simulated_isolated_devices: set[str] = set()

    def validate_ip(self, ip_str: str) -> str:
        try:
            parsed = ipaddress.ip_address(ip_str.strip())
            return str(parsed)
        except Exception as e:
            raise ValueError(f"Invalid IP address '{ip_str}': {str(e)}")

    def _validate_ip(self, ip_str: str) -> str:
        return self.validate_ip(ip_str)

    def isolate_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        try:
            clean_ip = self.validate_ip(device_ip)
        except ValueError as ve:
            return EnforcementResult(
                success=False,
                mode="SIMULATION",
                status="FAILED",
                message=str(ve),
                details={"invalid_ip": device_ip}
            )

        already_isolated = device_id in self._simulated_isolated_devices
        self._simulated_isolated_devices.add(device_id)

        idempotent_note = " (already isolated)" if already_isolated else ""
        return EnforcementResult(
            success=True,
            mode="SIMULATION",
            status="SIMULATED",
            message=(
                f"Device {device_id} ({clean_ip}) network isolation simulated{idempotent_note} "
                f"(EDGE_ENFORCEMENT_MODE=simulation). No OS firewall rules were modified on {platform.system()}."
            ),
            details={
                "device_id": device_id,
                "ip": clean_ip,
                "idempotent": already_isolated,
                "environment": platform.system()
            }
        )

    def reconnect_device(self, device_ip: str, device_id: str) -> EnforcementResult:
        try:
            clean_ip = self.validate_ip(device_ip)
        except ValueError as ve:
            return EnforcementResult(
                success=False,
                mode="SIMULATION",
                status="FAILED",
                message=str(ve),
                details={"invalid_ip": device_ip}
            )

        was_isolated = device_id in self._simulated_isolated_devices
        self._simulated_isolated_devices.discard(device_id)

        idempotent_note = "" if was_isolated else " (already active)"
        return EnforcementResult(
            success=True,
            mode="SIMULATION",
            status="SIMULATED",
            message=(
                f"Device {device_id} ({clean_ip}) network reconnection simulated{idempotent_note} "
                f"(EDGE_ENFORCEMENT_MODE=simulation). No OS firewall rules were modified."
            ),
            details={
                "device_id": device_id,
                "ip": clean_ip,
                "idempotent": not was_isolated,
                "environment": platform.system()
            }
        )

    def verify_isolated(self, device_ip: str, device_id: str) -> bool:
        return device_id in self._simulated_isolated_devices


def get_enforcement_adapter() -> EnforcementAdapter:
    """Factory creating the configured enforcement adapter with environment awareness."""
    mode = getattr(settings, "EDGE_ENFORCEMENT_MODE", "simulation").lower().strip()
    
    if mode == "host_firewall":
        return HostFirewallAdapter(
            backend=getattr(settings, "EDGE_FIREWALL_BACKEND", "iptables"),
            chain=getattr(settings, "EDGE_FIREWALL_CHAIN", "FORWARD"),
            timeout_seconds=getattr(settings, "EDGE_FIREWALL_TIMEOUT_SECONDS", 5)
        )
    elif mode == "simulation":
        return SimulationEnforcementAdapter()
    else:
        raise ValueError(
            f"Unsupported EDGE_ENFORCEMENT_MODE '{mode}'. Allowed options: 'simulation', 'host_firewall'."
        )


# Global singleton instance for runtime injection
enforcement_adapter = get_enforcement_adapter()
