"""Override Validator — Chapter 6: Golden Paths and API Design per Domain

Validates configuration override requests against an 80-15-5 override pyramid:
  - Flexible  (~80%): Self-service, no approval needed (low risk)
  - Governed  (~15%): Requires justification + platform team review (medium risk)
  - Blocked   (~5%):  Never permitted, non-negotiable security (critical risk)

Mirrors the interactive Override Validator at https://ddpe.platformetrics.com
See also: Chapter 4's escape_hatch.py for the deviation registry pattern.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ============================================================================
# Override Policy Matrix
# ============================================================================

@dataclass
class OverrideRule:
    """A single row in the Override Validator matrix."""
    configuration: str
    default: str
    override_level: str       # "flexible", "governed", or "blocked"
    approval: str             # who must approve ("none", "platform team", "N/A")
    risk: str                 # "low", "medium", "critical"
    expiration: Optional[str] = None  # e.g. "Review annually", None = permanent

    def __str__(self):
        return (f"{self.configuration:<30} | {self.override_level:<10} | "
                f"risk={self.risk:<8} | approval={self.approval}")


# Default override rules — matches the interactive tool at ddpe.platformetrics.com
OVERRIDE_RULES: list[OverrideRule] = [
    # ── Flexible (~80%): low risk, self-service ──
    OverrideRule("log_level",           "INFO",              "flexible",  "None",          "low"),
    OverrideRule("dev_resource_limits",  "Standard tier",    "flexible",  "None",          "low"),
    OverrideRule("feature_flags",        "Disabled",         "flexible",  "None",          "low"),
    OverrideRule("health_check_path",    "/healthz",         "flexible",  "None",          "low"),
    OverrideRule("replica_count",        "2",                "flexible",  "None",          "low"),
    OverrideRule("cache_ttl",            "300s",             "flexible",  "None",          "low"),
    OverrideRule("metric_interval",      "15s",              "flexible",  "None",          "low"),
    OverrideRule("alert_thresholds",     "Domain default",   "flexible",  "None",          "low"),

    # ── Governed (~15%): medium risk, needs justification ──
    OverrideRule("database_engine",      "PostgreSQL 15",    "governed",  "Platform team", "medium", "Review annually"),
    OverrideRule("custom_auth_provider", "Platform OAuth2",  "governed",  "Platform team", "medium", "Review annually"),
    OverrideRule("non_standard_runtime", "Python 3.12",      "governed",  "Platform team", "medium", "Review quarterly"),

    # ── Blocked (~5%): critical risk, never allowed ──
    OverrideRule("encryption_at_rest",   "Enabled (AES-256)","blocked",   "N/A",           "critical"),
    OverrideRule("network_exposure",     "Private only",     "blocked",   "N/A",           "critical"),
    OverrideRule("audit_logging",        "Enabled",          "blocked",   "N/A",           "critical"),
    OverrideRule("vulnerability_scan",   "Enabled",          "blocked",   "N/A",           "critical"),
]


# ============================================================================
# Override Request & Validation
# ============================================================================

@dataclass
class OverrideRequest:
    """A developer's request to change a configuration from its default."""
    configuration: str
    requested_value: str
    requester: str
    team: str
    justification: str = ""


@dataclass
class ValidationResult:
    """The outcome of validating an override request."""
    configuration: str
    outcome: str           # "approved", "pending_review", "rejected"
    override_level: str
    risk: str
    message: str
    expiration: Optional[str] = None


class OverrideValidator:
    """Validates configuration overrides against the 80-15-5 pyramid.

    - Flexible configs pass immediately (self-service).
    - Governed configs require justification and route to platform team review.
    - Blocked configs are rejected outright — no exceptions through this path.
    """

    def __init__(self, rules: list[OverrideRule] | None = None):
        self._rules = {r.configuration: r for r in (rules or OVERRIDE_RULES)}

    def validate(self, request: OverrideRequest) -> ValidationResult:
        rule = self._rules.get(request.configuration)

        if rule is None:
            return ValidationResult(
                configuration=request.configuration,
                outcome="unknown",
                override_level="unknown",
                risk="unknown",
                message=(f"Configuration '{request.configuration}' is not in the "
                         f"override matrix. Contact the platform team to classify it.")
            )

        if rule.override_level == "blocked":
            return ValidationResult(
                configuration=request.configuration,
                outcome="rejected",
                override_level="blocked",
                risk=rule.risk,
                message=(f"BLOCKED: '{request.configuration}' cannot be overridden. "
                         f"Default '{rule.default}' is a non-negotiable security control. "
                         f"Contact platform-security@ for exception process.")
            )

        if rule.override_level == "governed":
            if not request.justification:
                return ValidationResult(
                    configuration=request.configuration,
                    outcome="rejected",
                    override_level="governed",
                    risk=rule.risk,
                    message=(f"GOVERNED: '{request.configuration}' requires justification. "
                             f"Resubmit with a business reason for changing "
                             f"'{rule.default}' to '{request.requested_value}'.")
                )
            return ValidationResult(
                configuration=request.configuration,
                outcome="pending_review",
                override_level="governed",
                risk=rule.risk,
                message=(f"GOVERNED: Override routed to {rule.approval} for review. "
                         f"Justification: '{request.justification}'"),
                expiration=rule.expiration
            )

        # flexible
        return ValidationResult(
            configuration=request.configuration,
            outcome="approved",
            override_level="flexible",
            risk=rule.risk,
            message=(f"APPROVED: '{request.configuration}' changed from "
                     f"'{rule.default}' to '{request.requested_value}'. "
                     f"No approval needed (self-service).")
        )

    def print_matrix(self):
        """Print the full override matrix grouped by tier."""
        tiers = {"flexible": [], "governed": [], "blocked": []}
        for rule in self._rules.values():
            tiers[rule.override_level].append(rule)

        total = len(self._rules)
        for tier_name, label, pct in [
            ("flexible", "FLEXIBLE (self-service)", "~80%"),
            ("governed", "GOVERNED (justification + review)", "~15%"),
            ("blocked",  "BLOCKED (never permitted)", "~5%"),
        ]:
            rules = tiers[tier_name]
            actual_pct = f"{len(rules)/total*100:.0f}%"
            print(f"\n  {label}  [{len(rules)} rules, {actual_pct} of matrix]")
            print(f"  {'─' * 68}")
            for r in rules:
                exp = f"  (expires: {r.expiration})" if r.expiration else ""
                print(f"    {r.configuration:<25} default={r.default:<20} "
                      f"risk={r.risk}{exp}")


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Override Validator — 80-15-5 Override Pyramid Demo")
    print("  Chapter 6: Golden Paths and API Design per Domain")
    print("=" * 70)

    validator = OverrideValidator()

    # Show the full matrix
    print("\n  OVERRIDE POLICY MATRIX")
    validator.print_matrix()

    # Simulate override requests across all three tiers
    print("\n\n" + "=" * 70)
    print("  VALIDATING OVERRIDE REQUESTS")
    print("=" * 70)

    requests = [
        # Flexible — should auto-approve
        OverrideRequest(
            "log_level", "DEBUG", "alice", "Payments",
            justification="Debugging latency spike in settlement flow"
        ),
        OverrideRequest(
            "replica_count", "5", "bob", "Commerce",
            justification="Holiday traffic surge"
        ),

        # Governed — with justification (should route to review)
        OverrideRequest(
            "database_engine", "TimescaleDB", "carol", "Analytics",
            justification="Time-series workload needs native hypertable support"
        ),

        # Governed — without justification (should reject)
        OverrideRequest(
            "custom_auth_provider", "Auth0", "dave", "Identity",
            justification=""
        ),

        # Blocked — should reject regardless
        OverrideRequest(
            "encryption_at_rest", "Disabled", "eve", "Dev-Tools",
            justification="Faster local development"
        ),
        OverrideRequest(
            "network_exposure", "Public", "frank", "Marketing",
            justification="Quick demo for stakeholders"
        ),

        # Unknown — not in the matrix
        OverrideRequest(
            "custom_dns_resolver", "8.8.8.8", "grace", "Networking",
            justification="Need Google DNS"
        ),
    ]

    for req in requests:
        result = validator.validate(req)

        status_icon = {
            "approved": "✓",
            "pending_review": "⏳",
            "rejected": "✗",
            "unknown": "?"
        }[result.outcome]

        print(f"\n  {status_icon} {req.requester} ({req.team}) → "
              f"'{req.configuration}' = '{req.requested_value}'")
        print(f"    {result.message}")
        if result.expiration:
            print(f"    Override expiration: {result.expiration}")

    # Summary
    print("\n\n" + "-" * 70)
    print("  80-15-5 PYRAMID SUMMARY")
    print("  ─" * 35)
    print("    ~80% Flexible  : Self-service, no approval — team preference")
    print("    ~15% Governed  : Justification + platform team review — some risk")
    print("     ~5% Blocked   : Never permitted — non-negotiable security")
    print()
    print("  Interactive version: https://ddpe.platformetrics.com")
    print("=" * 70)
