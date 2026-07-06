"""Customization Tracker — Chapter 6: Golden Paths and API Design per Domain

Manages the lifecycle of domain-specific customization requests:
  Requested → Approved → Implemented → Monitoring → Graduated

Tracks which customizations are candidates for graduation into platform
defaults based on adoption breadth, production stability, and support trends.

Mirrors the Customization Tracker tab in the interactive tool at
https://ddpe.platformetrics.com/tools/api-design-standards

See also: override_validator.py (80-15-5 pyramid) and
          flexibility_scoring.py (standardization vs flexibility balance).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


# ============================================================================
# Data Model
# ============================================================================

LIFECYCLE_STAGES = ["Requested", "Approved", "Implemented", "Monitoring", "Graduated"]

@dataclass
class Customization:
    """A domain-specific customization request and its lifecycle state."""
    id: str
    name: str
    domain: str
    description: str
    requesting_team: str
    stage: str                           # one of LIFECYCLE_STAGES
    requested_date: datetime
    adopting_teams: list[str] = field(default_factory=list)
    months_in_production: int = 0
    support_ticket_trend: str = "n/a"    # "increasing", "stable", "decreasing"
    notes: str = ""

    @property
    def adoption_count(self) -> int:
        return len(self.adopting_teams)


# ============================================================================
# Graduation Criteria (from Table 6-5 in the book)
# ============================================================================

GRADUATION_CRITERIA = {
    "requesting_teams": {"threshold": 3, "rationale": "Demonstrates broad need"},
    "active_adoptions": {"threshold": 5, "rationale": "Proves practical value"},
    "months_in_production": {"threshold": 3, "rationale": "Validates stability"},
    "support_ticket_trend": {"threshold": "decreasing", "rationale": "Confirms usability"},
}


@dataclass
class GraduationAssessment:
    """Result of evaluating a customization against graduation criteria."""
    customization_id: str
    name: str
    criteria_met: dict[str, bool]
    eligible: bool
    recommendation: str


# ============================================================================
# Tracker
# ============================================================================

class CustomizationTracker:
    """Tracks customization requests through their lifecycle and identifies
    graduation candidates.

    Graduation criteria (from Table 6-5):
      - 3+ requesting teams (demonstrates broad need)
      - 5+ active implementations (proves practical value)
      - 3+ months in production (validates stability)
      - Decreasing support ticket trend (confirms usability)
    """

    def __init__(self):
        self._customizations: dict[str, Customization] = {}

    def add(self, customization: Customization):
        self._customizations[customization.id] = customization

    def advance_stage(self, cust_id: str) -> str:
        """Move a customization to the next lifecycle stage."""
        c = self._customizations[cust_id]
        current_idx = LIFECYCLE_STAGES.index(c.stage)
        if current_idx < len(LIFECYCLE_STAGES) - 1:
            c.stage = LIFECYCLE_STAGES[current_idx + 1]
        return c.stage

    def assess_graduation(self, cust_id: str) -> GraduationAssessment:
        """Evaluate whether a customization meets graduation criteria."""
        c = self._customizations[cust_id]

        criteria_met = {
            "requesting_teams": c.adoption_count >= GRADUATION_CRITERIA["requesting_teams"]["threshold"],
            "active_adoptions": c.adoption_count >= GRADUATION_CRITERIA["active_adoptions"]["threshold"],
            "months_in_production": c.months_in_production >= GRADUATION_CRITERIA["months_in_production"]["threshold"],
            "support_ticket_trend": c.support_ticket_trend == GRADUATION_CRITERIA["support_ticket_trend"]["threshold"],
        }

        all_met = all(criteria_met.values())
        met_count = sum(criteria_met.values())

        if all_met:
            rec = "Ready for graduation — absorb into platform defaults"
        elif met_count >= 3:
            failing = [k for k, v in criteria_met.items() if not v]
            rec = f"Nearly ready — {', '.join(failing)} not yet met"
        elif met_count >= 2:
            rec = "Progressing — continue monitoring before graduation"
        else:
            rec = "Too early — needs broader adoption and production time"

        return GraduationAssessment(
            customization_id=c.id,
            name=c.name,
            criteria_met=criteria_met,
            eligible=all_met,
            recommendation=rec
        )

    def portfolio_metrics(self) -> dict:
        """Compute portfolio-level health metrics."""
        all_custs = list(self._customizations.values())
        total = len(all_custs)
        if total == 0:
            return {}

        by_stage = {}
        for c in all_custs:
            by_stage.setdefault(c.stage, []).append(c)

        graduated = len(by_stage.get("Graduated", []))
        monitoring = len(by_stage.get("Monitoring", []))

        return {
            "total": total,
            "by_stage": {s: len(by_stage.get(s, [])) for s in LIFECYCLE_STAGES},
            "graduation_rate": f"{graduated/total:.0%}" if total else "0%",
            "in_monitoring": monitoring,
            "avg_adopting_teams": sum(c.adoption_count for c in all_custs) / total,
        }

    @property
    def all(self) -> list[Customization]:
        return list(self._customizations.values())


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Customization Tracker — Lifecycle & Graduation Demo")
    print("  Chapter 6: Golden Paths and API Design per Domain")
    print("=" * 70)

    tracker = CustomizationTracker()
    now = datetime.now()

    # Sample customizations at various lifecycle stages
    customizations = [
        Customization(
            id="CUST-001",
            name="Service inventory metadata fields",
            domain="Platform-wide",
            description="Custom metadata fields for tracking service ownership, "
                        "cost center, and data classification",
            requesting_team="Payments",
            stage="Monitoring",
            requested_date=now - timedelta(days=180),
            adopting_teams=["Payments", "Commerce", "Risk", "Analytics", "Identity"],
            months_in_production=5,
            support_ticket_trend="decreasing",
        ),
        Customization(
            id="CUST-002",
            name="TimescaleDB for time-series workloads",
            domain="Analytics",
            description="Alternative database engine for high-volume time-series "
                        "data instead of standard PostgreSQL",
            requesting_team="Analytics",
            stage="Monitoring",
            requested_date=now - timedelta(days=120),
            adopting_teams=["Analytics", "Risk", "Observability"],
            months_in_production=3,
            support_ticket_trend="stable",
        ),
        Customization(
            id="CUST-003",
            name="Custom retry policy for payment gateways",
            domain="Payments",
            description="Domain-specific retry backoff with idempotency key "
                        "tracking for external payment processor calls",
            requesting_team="Payments",
            stage="Implemented",
            requested_date=now - timedelta(days=60),
            adopting_teams=["Payments", "Settlements"],
            months_in_production=1,
            support_ticket_trend="stable",
        ),
        Customization(
            id="CUST-004",
            name="GraphQL gateway for BFF pattern",
            domain="Commerce",
            description="GraphQL federation layer for backend-for-frontend "
                        "pattern in customer-facing commerce apps",
            requesting_team="Commerce",
            stage="Approved",
            requested_date=now - timedelta(days=14),
            adopting_teams=["Commerce"],
            months_in_production=0,
            support_ticket_trend="n/a",
        ),
        Customization(
            id="CUST-005",
            name="Event replay capability for audit",
            domain="Risk",
            description="Ability to replay domain events for regulatory audit "
                        "reconstruction and compliance reporting",
            requesting_team="Risk",
            stage="Requested",
            requested_date=now - timedelta(days=3),
            adopting_teams=[],
            months_in_production=0,
            support_ticket_trend="n/a",
        ),
        Customization(
            id="CUST-006",
            name="Blue-green deployment for stateful services",
            domain="Platform-wide",
            description="Blue-green deployment strategy with state migration "
                        "support, graduated from customization to platform default",
            requesting_team="Identity",
            stage="Graduated",
            requested_date=now - timedelta(days=270),
            adopting_teams=["Identity", "Payments", "Commerce", "Risk",
                            "Analytics", "Settlements", "Onboarding"],
            months_in_production=8,
            support_ticket_trend="decreasing",
        ),
    ]

    for c in customizations:
        tracker.add(c)

    # ── Portfolio metrics ──
    metrics = tracker.portfolio_metrics()
    print(f"\n  PORTFOLIO METRICS")
    print(f"  {'─' * 66}")
    print(f"    Total customizations     : {metrics['total']}")
    print(f"    Graduation rate          : {metrics['graduation_rate']}")
    print(f"    In monitoring            : {metrics['in_monitoring']}")
    print(f"    Avg adopting teams       : {metrics['avg_adopting_teams']:.1f}")
    print(f"\n    By lifecycle stage:")
    for stage in LIFECYCLE_STAGES:
        count = metrics["by_stage"][stage]
        bar = "█" * count + "░" * (6 - count)
        print(f"      {stage:<14} {bar}  {count}")

    # ── Lifecycle view ──
    print(f"\n\n  CUSTOMIZATION LIFECYCLE")
    print(f"  {'─' * 66}")
    print(f"    Requested → Approved → Implemented → Monitoring → Graduated")
    print()

    for c in tracker.all:
        stage_idx = LIFECYCLE_STAGES.index(c.stage)
        progress = "".join(
            "●" if i <= stage_idx else "○"
            for i in range(len(LIFECYCLE_STAGES))
        )
        teams = ", ".join(c.adopting_teams) if c.adopting_teams else "—"
        print(f"    [{c.id}] {c.name}")
        print(f"      Stage: {progress} {c.stage}")
        print(f"      Domain: {c.domain}  |  Teams: {teams}")
        if c.months_in_production > 0:
            print(f"      Production: {c.months_in_production} months  |  "
                  f"Support trend: {c.support_ticket_trend}")
        print()

    # ── Graduation assessments ──
    print(f"\n  GRADUATION ASSESSMENTS")
    print(f"  {'─' * 66}")
    print(f"  Criteria (Table 6-5): 3+ teams, 5+ adoptions, 3+ months, "
          f"decreasing tickets\n")

    for c in tracker.all:
        if c.stage in ("Monitoring", "Implemented"):
            assessment = tracker.assess_graduation(c.id)
            met = sum(assessment.criteria_met.values())
            total_criteria = len(assessment.criteria_met)
            icon = "✓" if assessment.eligible else "⏳"

            print(f"    {icon} {c.name} ({c.id})")
            print(f"      Criteria met: {met}/{total_criteria}")
            for criterion, passed in assessment.criteria_met.items():
                mark = "✓" if passed else "✗"
                threshold = GRADUATION_CRITERIA[criterion]
                print(f"        {mark} {criterion}: "
                      f"threshold={threshold['threshold']} — "
                      f"{threshold['rationale']}")
            print(f"      → {assessment.recommendation}")
            print()

    # ── Key insight ──
    print(f"  {'─' * 66}")
    print(f"  KEY INSIGHT: When multiple teams independently request similar")
    print(f"  customizations, this signals a gap in platform defaults. The")
    print(f"  customization becomes a feature. What was special becomes standard.")
    print(f"  Without systematic tracking, these patterns go unrecognized.")
    print()
    print(f"  Interactive version: https://ddpe.platformetrics.com")
    print("=" * 70)
