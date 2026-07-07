"""Golden Path Compliance Depth Index — Chapter 8: Patterns for Scaling Platform Adoption

Scores how deeply teams have actually adopted each golden path across four layers:
  Surface    — Team instantiated the template / uses the tools
  Structural — Team follows the architecture patterns and conventions
  Behavioral — Team preserves opinionated defaults, uses override pyramid correctly
  Cultural   — Team champions the platform, contributes improvements back

A team scoring 95 on Surface but 15 on Behavioral is a "ticking time bomb" —
they appear adopted but are actively diverging. This metric separates real
platform value from adoption theater.

Track as a radar chart per team per golden path. When the Compliance Depth
Index is trending down quarter over quarter, the platform is delivering
genuine, deep adoption.

Interactive version available at https://ddpe.platformetrics.com

See also: adoption_health.py (anti-pattern detection) and
          rollout_planner.py (phased rollout strategy).
"""

from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# Data Model
# ============================================================================

DEPTH_LAYERS = ["Surface", "Structural", "Behavioral", "Cultural"]

LAYER_DESCRIPTIONS = {
    "Surface": "Uses the template/tools — instantiated golden path, CI runs green",
    "Structural": "Follows architecture patterns — layer separation, API conventions, repository pattern",
    "Behavioral": "Preserves opinionated defaults — override pyramid respected, no shadow configs",
    "Cultural": "Champions the platform — contributes improvements, mentors other teams",
}

LAYER_INDICATORS = {
    "Surface": [
        "Golden path template instantiated",
        "CI/CD pipeline running on platform",
        "Service registered in catalog",
        "Standard observability deployed",
    ],
    "Structural": [
        "Repository pattern enforced (no direct datastore imports)",
        "API naming conventions followed",
        "Domain language used in service interfaces",
        "Bounded context boundaries respected",
    ],
    "Behavioral": [
        "Opinionated defaults preserved (not overridden without governed approval)",
        "Override pyramid followed (flexible/governed/blocked tiers)",
        "No shadow infrastructure or workarounds",
        "Escape hatches used through proper registry",
    ],
    "Cultural": [
        "Team contributes improvements back to golden path",
        "Team members mentor other teams on platform adoption",
        "Team participates in platform community of practice",
        "Team advocates for platform in architecture reviews",
    ],
}


@dataclass
class GoldenPathScore:
    """Compliance depth scores for one team on one golden path."""
    team: str
    golden_path: str
    surface: int         # 0-100
    structural: int      # 0-100
    behavioral: int      # 0-100
    cultural: int        # 0-100
    quarter: str = ""    # e.g. "Q1 2026"

    @property
    def scores(self) -> dict[str, int]:
        return {
            "Surface": self.surface,
            "Structural": self.structural,
            "Behavioral": self.behavioral,
            "Cultural": self.cultural,
        }

    @property
    def overall(self) -> float:
        """Weighted average — deeper layers count more."""
        weights = {"Surface": 1.0, "Structural": 1.5, "Behavioral": 2.0, "Cultural": 2.5}
        total_weight = sum(weights.values())
        return sum(self.scores[layer] * weights[layer] for layer in DEPTH_LAYERS) / total_weight

    @property
    def depth_gap(self) -> int:
        """Gap between shallowest adoption (Surface) and deepest (Cultural).
        Large positive gaps signal adoption theater."""
        return self.surface - self.cultural


@dataclass
class DepthAssessment:
    """Assessment result for a team's compliance depth."""
    team: str
    golden_path: str
    overall_score: float
    depth_gap: int
    risk_level: str          # "healthy", "warning", "critical"
    assessment: str
    recommendations: list[str]


# ============================================================================
# Compliance Depth Index Engine
# ============================================================================

class ComplianceDepthIndex:
    """Scores and analyzes golden path adoption depth across teams.

    The key insight: adoption theater shows high Surface scores with low
    Behavioral/Cultural scores. The Compliance Depth Index catches this
    by weighting deeper layers more heavily and flagging dangerous gaps.

    Depth gap thresholds:
      - Healthy:  Surface - Cultural <= 20 (genuine, even adoption)
      - Warning:  Surface - Cultural 21-40 (diverging, needs attention)
      - Critical: Surface - Cultural > 40  (adoption theater / time bomb)
    """

    HEALTHY_GAP = 20
    WARNING_GAP = 40

    def __init__(self):
        self._scores: list[GoldenPathScore] = []

    def add(self, score: GoldenPathScore):
        self._scores.append(score)

    def assess(self, score: GoldenPathScore) -> DepthAssessment:
        """Evaluate a single team's compliance depth."""
        gap = score.depth_gap
        overall = score.overall
        recommendations = []

        if gap <= self.HEALTHY_GAP:
            risk = "healthy"
            assessment = "Genuine adoption — depth is consistent across all layers"
        elif gap <= self.WARNING_GAP:
            risk = "warning"
            assessment = "Diverging adoption — surface usage outpacing deeper integration"
            # Find weakest layer
            weakest = min(score.scores, key=score.scores.get)
            recommendations.append(
                f"Focus on {weakest} layer (score: {score.scores[weakest]})"
            )
            if score.behavioral < 50:
                recommendations.append(
                    "Review override usage — team may be bypassing opinionated defaults"
                )
            if score.cultural < 30:
                recommendations.append(
                    "Invite team to platform community of practice"
                )
        else:
            risk = "critical"
            assessment = ("Adoption theater — appears adopted on surface but actively "
                         "diverging at deeper layers. This is a ticking time bomb.")
            recommendations.append(
                "Conduct adoption retrospective with the team immediately"
            )
            if score.behavioral < 30:
                recommendations.append(
                    "Audit for shadow infrastructure and undocumented overrides"
                )
            if score.cultural < 20:
                recommendations.append(
                    "Assign a platform champion to embed with the team"
                )
            recommendations.append(
                "Consider whether the golden path needs adaptation for this domain"
            )

        return DepthAssessment(
            team=score.team,
            golden_path=score.golden_path,
            overall_score=overall,
            depth_gap=gap,
            risk_level=risk,
            assessment=assessment,
            recommendations=recommendations,
        )

    def portfolio_summary(self) -> dict:
        """Aggregate metrics across all teams and golden paths."""
        if not self._scores:
            return {}

        assessments = [self.assess(s) for s in self._scores]
        total = len(assessments)

        risk_counts = {"healthy": 0, "warning": 0, "critical": 0}
        for a in assessments:
            risk_counts[a.risk_level] += 1

        avg_by_layer = {}
        for layer in DEPTH_LAYERS:
            layer_key = layer.lower()
            avg_by_layer[layer] = sum(
                getattr(s, layer_key) for s in self._scores
            ) / total

        avg_overall = sum(a.overall_score for a in assessments) / total
        avg_gap = sum(a.depth_gap for a in assessments) / total

        return {
            "total_assessments": total,
            "risk_distribution": risk_counts,
            "avg_by_layer": avg_by_layer,
            "avg_overall": round(avg_overall, 1),
            "avg_depth_gap": round(avg_gap, 1),
            "theater_teams": [a.team for a in assessments if a.risk_level == "critical"],
        }

    @property
    def all_scores(self) -> list[GoldenPathScore]:
        return list(self._scores)


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Golden Path Compliance Depth Index")
    print("  Chapter 8: Patterns for Scaling Platform Adoption")
    print("=" * 70)

    index = ComplianceDepthIndex()

    # Sample data — teams at various adoption depths
    scores = [
        GoldenPathScore(
            team="Payments",
            golden_path="Microservice Template",
            surface=95, structural=88, behavioral=82, cultural=75,
            quarter="Q2 2026",
        ),
        GoldenPathScore(
            team="Commerce",
            golden_path="Microservice Template",
            surface=90, structural=70, behavioral=45, cultural=20,
            quarter="Q2 2026",
        ),
        GoldenPathScore(
            team="Analytics",
            golden_path="Data Pipeline Template",
            surface=85, structural=80, behavioral=75, cultural=60,
            quarter="Q2 2026",
        ),
        GoldenPathScore(
            team="Risk",
            golden_path="Microservice Template",
            surface=80, structural=65, behavioral=55, cultural=45,
            quarter="Q2 2026",
        ),
        GoldenPathScore(
            team="Identity",
            golden_path="Microservice Template",
            surface=92, structural=90, behavioral=85, cultural=80,
            quarter="Q2 2026",
        ),
        GoldenPathScore(
            team="Marketing",
            golden_path="Frontend Template",
            surface=88, structural=40, behavioral=25, cultural=10,
            quarter="Q2 2026",
        ),
    ]

    for s in scores:
        index.add(s)

    # ── Layer definitions ──
    print(f"\n  COMPLIANCE DEPTH LAYERS")
    print(f"  {'─' * 66}")
    for layer in DEPTH_LAYERS:
        print(f"    {layer:<12} {LAYER_DESCRIPTIONS[layer]}")

    # ── Radar charts (ASCII) ──
    print(f"\n\n  TEAM DEPTH PROFILES")
    print(f"  {'─' * 66}")

    for s in index.all_scores:
        assessment = index.assess(s)
        risk_icon = {"healthy": "●", "warning": "◐", "critical": "○"}[assessment.risk_level]
        risk_label = {"healthy": "Healthy", "warning": "Warning", "critical": "CRITICAL"}[assessment.risk_level]

        print(f"\n    {risk_icon} {s.team} — {s.golden_path}  ({s.quarter})")
        print(f"      Overall: {assessment.overall_score:.0f}  |  Depth gap: {assessment.depth_gap}  |  Risk: {risk_label}")
        print()

        # ASCII radar chart
        bar_width = 40
        for layer in DEPTH_LAYERS:
            score = s.scores[layer]
            filled = int(score / 100 * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            print(f"      {layer:<12} {bar} {score:>3}")

        # Assessment & recommendations
        print(f"\n      → {assessment.assessment}")
        for rec in assessment.recommendations:
            print(f"        • {rec}")

    # ── Portfolio summary ──
    summary = index.portfolio_summary()
    print(f"\n\n  PORTFOLIO SUMMARY")
    print(f"  {'─' * 66}")
    print(f"    Teams assessed       : {summary['total_assessments']}")
    print(f"    Average overall score: {summary['avg_overall']}")
    print(f"    Average depth gap    : {summary['avg_depth_gap']}")
    print()
    print(f"    Risk distribution:")
    for risk, count in summary["risk_distribution"].items():
        bar = "█" * count + "░" * (6 - count)
        label = {"healthy": "Healthy ", "warning": "Warning ", "critical": "Critical"}[risk]
        print(f"      {label} {bar}  {count}")

    if summary["theater_teams"]:
        print(f"\n    ⚠ Adoption theater detected in: {', '.join(summary['theater_teams'])}")
        print(f"      These teams appear adopted on the surface but are diverging")
        print(f"      at deeper layers. Immediate attention required.")

    # ── Layer averages ──
    print(f"\n\n  LAYER AVERAGES (across all teams)")
    print(f"  {'─' * 66}")
    for layer in DEPTH_LAYERS:
        avg = summary["avg_by_layer"][layer]
        bar_width = 40
        filled = int(avg / 100 * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"    {layer:<12} {bar} {avg:>5.1f}")

    drop = summary["avg_by_layer"]["Surface"] - summary["avg_by_layer"]["Cultural"]
    print(f"\n    Surface → Cultural drop: {drop:.1f} points")
    if drop > 30:
        print(f"    ⚠ Significant depth erosion — platform adoption is shallow overall")
    elif drop > 15:
        print(f"    ◐ Moderate depth erosion — some teams need deeper integration support")
    else:
        print(f"    ● Healthy depth profile — adoption is genuine across layers")

    # ── Key insight ──
    print(f"\n\n  {'─' * 66}")
    print(f"  KEY INSIGHT: The most dangerous adoption metric is a high Surface")
    print(f"  score with a low Behavioral score. These teams look adopted on")
    print(f"  every dashboard but are routing around guardrails through escape")
    print(f"  hatches, shadow configs, or silent overrides. The Compliance Depth")
    print(f"  Index makes this gap visible before it becomes a production incident.")
    print()
    print(f"  Interactive version: https://ddpe.platformetrics.com")
    print("=" * 70)
