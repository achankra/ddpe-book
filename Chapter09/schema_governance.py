# schema_governance.py
"""Schema-Based Governance for Scaling Platform Adoption"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class CriticalityTier(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    MISSION_CRITICAL = "mission-critical"

@dataclass
class ServiceSchema:
    """Domain schema that services must conform to."""
    name: str
    owner_team: str
    product_line: str
    criticality: CriticalityTier
    upstream_deps: List[str] = field(default_factory=list)
    downstream_deps: List[str] = field(default_factory=list)
    telemetry_endpoint: str = ""
    log_routing: str = "centralized"
    alert_thresholds: dict = field(default_factory=dict)

    def validate(self) -> List[str]:
        """Validate service against domain schema requirements."""
        errors = []
        if not self.owner_team:
            errors.append("owner_team is required")
        if not self.product_line:
            errors.append("product_line is required")
        if self.criticality in [CriticalityTier.PRODUCTION, CriticalityTier.MISSION_CRITICAL]:
            if not self.telemetry_endpoint:
                errors.append("Production services must declare telemetry endpoint")
            if not self.alert_thresholds:
                errors.append("Production services must define alert thresholds")
        return errors

# Example: Team generates a conforming service definition
service = ServiceSchema(
    name="order-processor",
    owner_team="commerce-team",
    product_line="e-commerce",
    criticality=CriticalityTier.PRODUCTION,
    upstream_deps=["inventory-service", "payment-gateway"],
    downstream_deps=["notification-service"],
    telemetry_endpoint="/metrics",
    log_routing="centralized",
    alert_thresholds={"error_rate": 0.01, "p99_latency_ms": 500},
)

errors = service.validate()
if errors:
    print(f"Schema validation FAILED: {errors}")
else:
    print(f"Service '{service.name}' validated against ServiceDomain schema")
    print(f"  ✓ owner_team: {service.owner_team}")
    print(f"  ✓ criticality_tier: {service.criticality.value}")
    print(f"  ✓ dependencies: {len(service.upstream_deps) + len(service.downstream_deps)} declared")
    print(f"  ✓ telemetry: configured")
    print(f"  → Ready for deployment")
