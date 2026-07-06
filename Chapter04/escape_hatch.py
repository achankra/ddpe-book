# escape_hatch.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import logging

@dataclass
class DeviationRequest:
    service_name: str
    team_name: str
    deviation_type: str
    justification: str
    requested_by: str
    expires: Optional[datetime] = None

class EscapeHatchRegistry:
    """Tracks and governs deviations from golden paths."""

    BLOCKED_DEVIATIONS = [
        "disable_encryption",
        "disable_authentication",
        "public_network_exposure",
        "skip_vulnerability_scanning"
    ]

    SELF_SERVICE_DEVIATIONS = [
        "custom_resource_limits",
        "additional_environment_variables",
        "custom_health_check_paths",
        "non_standard_ports"
    ]

    APPROVAL_REQUIRED_DEVIATIONS = [
        "custom_database_engine",
        "external_service_integration",
        "non_standard_runtime",
        "elevated_permissions"
    ]

    def request_deviation(self, request: DeviationRequest) -> str:
        if request.deviation_type in self.BLOCKED_DEVIATIONS:
            raise ValueError(
                f"Deviation '{request.deviation_type}' is not permitted. "
                f"Contact platform-security@ for exceptions."
            )

        if request.deviation_type in self.SELF_SERVICE_DEVIATIONS:
            self._log_deviation(request)
            return "APPROVED_SELF_SERVICE"

        if request.deviation_type in self.APPROVAL_REQUIRED_DEVIATIONS:
            return self._submit_for_approval(request)

        return "UNKNOWN_DEVIATION_TYPE"
    
    def _log_deviation(self, request: DeviationRequest):
        logging.info(
            f"Deviation logged: {request.service_name} - "
            f"{request.deviation_type} by {request.requested_by}"
        )
    
    def _submit_for_approval(self, request: DeviationRequest) -> str:
        # Create approval ticket in workflow system
        return "PENDING_APPROVAL"


if __name__ == "__main__":
    print("=" * 62)
    print("  Escape-Hatch Registry — Deviation Tier Demo")
    print("=" * 62)

    registry = EscapeHatchRegistry()

    requests = [
        DeviationRequest("cart-svc", "Commerce", "custom_resource_limits",
                         "Need 4GB RAM for image processing", "alice"),
        DeviationRequest("auth-svc", "Identity", "non_standard_ports",
                         "Legacy client requires port 8443", "bob"),
        DeviationRequest("data-svc", "Analytics", "custom_database_engine",
                         "Team needs TimescaleDB for time-series", "carol"),
        DeviationRequest("payments", "Finance", "elevated_permissions",
                         "PCI audit requires direct DB reads", "dave"),
        DeviationRequest("api-gw", "Platform", "disable_encryption",
                         "Want faster local dev", "eve"),
        DeviationRequest("jobs", "Batch", "public_network_exposure",
                         "Quick demo for stakeholders", "frank"),
    ]

    for req in requests:
        print(f"\n  Request: '{req.deviation_type}' by {req.requested_by} "
              f"({req.service_name})")
        try:
            result = registry.request_deviation(req)
            tier = {"APPROVED_SELF_SERVICE": "Self-Service (auto-approved)",
                    "PENDING_APPROVAL": "Approval Required (ticket created)",
                    "UNKNOWN_DEVIATION_TYPE": "Unknown (needs classification)"}
            print(f"    -> {tier.get(result, result)}")
        except ValueError as e:
            print(f"    -> BLOCKED: {e}")

    print("\n" + "-" * 62)
    print("  Tier Summary:")
    print("    Self-Service : resource limits, env vars, health paths, ports")
    print("    Approval Req : custom DB, external integrations, runtimes")
    print("    Blocked      : disable encryption/auth, public exposure")
    print("=" * 62)
