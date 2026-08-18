"""
Chapter 9: Schema Governance — Multi-Service Validation

Extends schema_governance.py to validate multiple service definitions
across different criticality tiers and domains, showing both passing
and failing validations with actionable remediation guidance.

Run: python Chapter09/run_schema_governance.py
"""

from dataclasses import dataclass, field
from typing import List
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
        if self.criticality == CriticalityTier.MISSION_CRITICAL:
            if len(self.upstream_deps) == 0 and len(self.downstream_deps) == 0:
                errors.append("Mission-critical services must declare dependencies")
        return errors


# ── Service definitions across domains ──────────────────────────────

SERVICES = [
    # Semiconductor domain — fully compliant
    ServiceSchema(
        name="wafer-yield-analyzer",
        owner_team="fab-engineering",
        product_line="semiconductor-manufacturing",
        criticality=CriticalityTier.PRODUCTION,
        upstream_deps=["metrology-service", "defect-detection-pipeline"],
        downstream_deps=["yield-reporting-service"],
        telemetry_endpoint="/metrics",
        alert_thresholds={"error_rate": 0.005, "p99_latency_ms": 300},
    ),
    # BFSI domain — fully compliant, mission-critical
    ServiceSchema(
        name="transaction-processor",
        owner_team="payments-core",
        product_line="bfsi-payments",
        criticality=CriticalityTier.MISSION_CRITICAL,
        upstream_deps=["fraud-detection", "account-service"],
        downstream_deps=["settlement-engine", "audit-logger"],
        telemetry_endpoint="/metrics/payments",
        alert_thresholds={"error_rate": 0.001, "p99_latency_ms": 100, "tps_min": 1000},
    ),
    # Healthcare domain — missing telemetry (FAILS)
    ServiceSchema(
        name="patient-records-api",
        owner_team="clinical-systems",
        product_line="healthcare",
        criticality=CriticalityTier.PRODUCTION,
        upstream_deps=["identity-service"],
        downstream_deps=["ehr-sync"],
        telemetry_endpoint="",  # Missing!
        alert_thresholds={"error_rate": 0.01},
    ),
    # Development service — passes (lower requirements)
    ServiceSchema(
        name="feature-flag-tester",
        owner_team="platform-tools",
        product_line="internal-tooling",
        criticality=CriticalityTier.DEVELOPMENT,
    ),
    # Missing owner team (FAILS)
    ServiceSchema(
        name="legacy-bridge",
        owner_team="",  # Missing!
        product_line="migration",
        criticality=CriticalityTier.STAGING,
    ),
    # Mission-critical with no dependencies declared (FAILS)
    ServiceSchema(
        name="settlement-engine",
        owner_team="payments-settlement",
        product_line="bfsi-payments",
        criticality=CriticalityTier.MISSION_CRITICAL,
        telemetry_endpoint="/metrics/settlement",
        alert_thresholds={"error_rate": 0.0005, "p99_latency_ms": 50},
        # No deps declared — violation for mission-critical
    ),
    # Production with no alert thresholds (FAILS)
    ServiceSchema(
        name="reporting-dashboard",
        owner_team="analytics",
        product_line="business-intelligence",
        criticality=CriticalityTier.PRODUCTION,
        telemetry_endpoint="/metrics/reporting",
        alert_thresholds={},  # Missing!
    ),
]


def main():
    print("=" * 64)
    print("SCHEMA GOVERNANCE — SERVICE VALIDATION")
    print("=" * 64)

    print("\n  Schema governance enforces that services declare")
    print("  required metadata based on their criticality tier.")

    print(f"\n  VALIDATION RULES")
    print(f"  {'─' * 58}")
    print(f"    All tiers:         owner_team, product_line required")
    print(f"    Production+:       telemetry_endpoint, alert_thresholds required")
    print(f"    Mission-critical:  dependencies must be declared")

    # ── Validate each service ──
    print(f"\n{'=' * 64}")
    print("SERVICE VALIDATIONS")
    print("=" * 64)

    passed = 0
    failed = 0
    failures_by_tier = {}

    for svc in SERVICES:
        errors = svc.validate()
        tier = svc.criticality.value

        if errors:
            icon = "❌"
            status = "FAILED"
            failed += 1
            failures_by_tier[tier] = failures_by_tier.get(tier, 0) + 1
        else:
            icon = "✅"
            status = "PASSED"
            passed += 1

        print(f"\n  {icon} {svc.name}")
        print(f"    Owner:       {svc.owner_team or '(missing)'}")
        print(f"    Product:     {svc.product_line}")
        print(f"    Criticality: {tier}")
        print(f"    Deps:        {len(svc.upstream_deps)} upstream, {len(svc.downstream_deps)} downstream")
        print(f"    Telemetry:   {svc.telemetry_endpoint or '(not configured)'}")
        print(f"    Alerts:      {len(svc.alert_thresholds)} threshold(s)")
        print(f"    Result:      {status}")

        if errors:
            for e in errors:
                print(f"    ⚠  {e}")

    # ── Summary ──
    print(f"\n{'=' * 64}")
    print("GOVERNANCE SUMMARY")
    print("=" * 64)

    print(f"\n  Total services:  {len(SERVICES)}")
    print(f"  Passed:          {passed}")
    print(f"  Failed:          {failed}")

    print(f"\n  By criticality tier:")
    tier_counts = {}
    for svc in SERVICES:
        t = svc.criticality.value
        tier_counts.setdefault(t, {"total": 0, "pass": 0, "fail": 0})
        tier_counts[t]["total"] += 1
        if svc.validate():
            tier_counts[t]["fail"] += 1
        else:
            tier_counts[t]["pass"] += 1

    print(f"    {'Tier':<20s} {'Total':>6s} {'Pass':>6s} {'Fail':>6s}")
    print(f"    {'─' * 20} {'─' * 6} {'─' * 6} {'─' * 6}")
    for tier in ["mission-critical", "production", "staging", "development"]:
        if tier in tier_counts:
            c = tier_counts[tier]
            print(f"    {tier:<20s} {c['total']:>6d} {c['pass']:>6d} {c['fail']:>6d}")

    print(f"\n  Schema governance runs as a pre-deploy gate.")
    print(f"  Non-compliant services are blocked before they reach")
    print(f"  production — compliance is structural, not advisory.")


if __name__ == "__main__":
    main()
