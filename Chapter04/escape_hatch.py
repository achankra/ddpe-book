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
