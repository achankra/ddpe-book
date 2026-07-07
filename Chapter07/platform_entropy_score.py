"""Platform Entropy Score — Chapter 7: Measuring Platform Success

The meta-measurement that tracks how fast the platform itself is drifting
from domain truth. Even with DORA metrics, friction scores, and adoption
dashboards showing green, the platform can be slowly becoming legacy as
the business evolves and domain models diverge.

The Platform Entropy Score measures drift across three dimensions:

  Model Drift      — How far platform domain models have diverged from
                     current business processes. Measured via periodic
                     domain expert interviews scored against the
                     implemented ubiquitous language.

  Path Staleness   — What percentage of golden paths have not been updated
                     in response to business model changes. Tracked via
                     git history correlated with business change events.

  Boundary Erosion — How many cross-context calls bypass official
                     anti-corruption layers or published language
                     interfaces. Measured via traffic analysis.

A rising entropy score is the leading indicator that your platform is
becoming legacy. Track it quarterly, and you reframe platform maintenance
from "technical debt cleanup" to "domain alignment preservation" — a
narrative that sustains investment long after the initial build excitement
fades.

Interactive version available at https://ddpe.platformetrics.com

See also: dora_metrics.py (DORA metrics), friction_score.py (friction scoring),
          platform_roi.py (ROI modeling).
"""

from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# Data Model
# ============================================================================

ENTROPY_DIMENSIONS = ["Model Drift", "Path Staleness", "Boundary Erosion"]

DIMENSION_DESCRIPTIONS = {
    "Model Drift": (
        "How far platform domain models have diverged from current business "
        "processes, measured via periodic domain expert interviews scored "
        "against the implemented ubiquitous language"
    ),
    "Path Staleness": (
        "What percentage of golden paths have not been updated in response "
        "to business model changes, tracked via git history correlated with "
        "business change events"
    ),
    "Boundary Erosion": (
        "How many cross-context calls bypass official anti-corruption layers "
        "or published language interfaces, measured via traffic analysis"
    ),
}

DIMENSION_INDICATORS = {
    "Model Drift": [
        "Domain experts identify terms in platform APIs that no longer match business vocabulary",
        "New business processes have no corresponding platform abstractions",
        "Developers build workarounds because platform concepts don't map to current domain",
        "Onboarding materials reference outdated business workflows",
    ],
    "Path Staleness": [
        "Golden path templates reference deprecated services or APIs",
        "Business model changes (acquisitions, pivots, new products) not reflected in paths",
        "Git history shows no golden path updates correlated with business change events",
        "Teams fork golden paths rather than requesting updates",
    ],
    "Boundary Erosion": [
        "Cross-context API calls bypass anti-corruption layers",
        "Services directly import from other bounded contexts without translation",
        "Shared database access across context boundaries increasing",
        "Published language interfaces have undocumented consumers",
    ],
}

MEASUREMENT_METHODS = {
    "Model Drift": [
        "Periodic domain expert interviews (quarterly)",
        "Ubiquitous language audit — compare platform terms to current business glossary",
        "New business capability mapping — gap analysis against platform model",
        "Developer survey — 'Does the platform speak your domain language?'",
    ],
    "Path Staleness": [
        "Git history analysis — last update date per golden path",
        "Business change event log correlation — acquisitions, new product lines, reorgs",
        "Path fork tracking — count of teams maintaining local forks",
        "Template dependency scan — percentage using deprecated versions",
    ],
    "Boundary Erosion": [
        "Service mesh traffic analysis — cross-context calls vs. approved interfaces",
        "Anti-corruption layer bypass detection — direct imports from other contexts",
        "Database access audit — shared table access across bounded contexts",
        "API consumer analysis — undocumented consumers of published interfaces",
    ],
}


@dataclass
class EntropyMeasurement:
    """A single entropy measurement for one bounded context or platform area."""
    context_name: str
    quarter: str                    # e.g. "Q2 2026"
    model_drift: float              # 0-100 (0 = perfect alignment, 100 = complete divergence)
    path_staleness: float           # 0-100 (0 = all paths current, 100 = all paths stale)
    boundary_erosion: float         # 0-100 (0 = no bypass, 100 = all calls bypass ACL)

    @property
    def scores(self) -> dict[str, float]:
        return {
            "Model Drift": self.model_drift,
            "Path Staleness": self.path_staleness,
            "Boundary Erosion": self.boundary_erosion,
        }

    @property
    def entropy_score(self) -> float:
        """Composite entropy score — equal weighting across all three dimensions."""
        return (self.model_drift + self.path_staleness + self.boundary_erosion) / 3.0

    @property
    def risk_level(self) -> str:
        score = self.entropy_score
        if score <= 20:
            return "low"
        elif score <= 40:
            return "moderate"
        elif score <= 60:
            return "high"
        else:
            return "critical"


@dataclass
class EntropyTrend:
    """Tracks entropy measurements over multiple quarters for one context."""
    context_name: str
    measurements: list[EntropyMeasurement] = field(default_factory=list)

    @property
    def latest(self) -> Optional[EntropyMeasurement]:
        return self.measurements[-1] if self.measurements else None

    @property
    def trend_direction(self) -> str:
        """Determine if entropy is rising, stable, or falling."""
        if len(self.measurements) < 2:
            return "insufficient_data"
        recent = self.measurements[-1].entropy_score
        previous = self.measurements[-2].entropy_score
        delta = recent - previous
        if delta > 5:
            return "rising"
        elif delta < -5:
            return "falling"
        else:
            return "stable"

    @property
    def quarter_over_quarter_delta(self) -> Optional[float]:
        if len(self.measurements) < 2:
            return None
        return self.measurements[-1].entropy_score - self.measurements[-2].entropy_score


# ============================================================================
# Platform Entropy Score Engine
# ============================================================================

class PlatformEntropyScorer:
    """Calculates and tracks Platform Entropy Score across bounded contexts.

    The Platform Entropy Score is the leading indicator that your platform
    is becoming legacy. Unlike DORA metrics (which measure engineering
    speed) or adoption metrics (which measure usage), entropy measures
    whether the platform still accurately represents the business.

    Entropy thresholds:
      - Low (0-20):      Platform models closely align with business reality
      - Moderate (21-40): Some drift — schedule domain alignment review
      - High (41-60):     Significant divergence — active remediation needed
      - Critical (61-100): Platform is becoming legacy — urgent intervention
    """

    def __init__(self):
        self._trends: dict[str, EntropyTrend] = {}

    def record(self, measurement: EntropyMeasurement):
        """Record an entropy measurement for a bounded context."""
        if measurement.context_name not in self._trends:
            self._trends[measurement.context_name] = EntropyTrend(
                context_name=measurement.context_name
            )
        self._trends[measurement.context_name].measurements.append(measurement)

    def assess(self, measurement: EntropyMeasurement) -> dict:
        """Assess a single entropy measurement and generate recommendations."""
        score = measurement.entropy_score
        risk = measurement.risk_level
        recommendations = []

        # Dimension-specific recommendations
        if measurement.model_drift > 50:
            recommendations.append(
                "Schedule domain expert interviews — platform language has diverged "
                "significantly from business vocabulary"
            )
        elif measurement.model_drift > 30:
            recommendations.append(
                "Conduct ubiquitous language audit — compare platform API terms "
                "against current business glossary"
            )

        if measurement.path_staleness > 50:
            recommendations.append(
                "Correlate golden path update history with recent business changes — "
                "paths may not reflect current domain needs"
            )
        elif measurement.path_staleness > 30:
            recommendations.append(
                "Review golden path fork count — teams may be maintaining local "
                "forks because templates are outdated"
            )

        if measurement.boundary_erosion > 50:
            recommendations.append(
                "Audit cross-context traffic — significant bypass of anti-corruption "
                "layers detected. Boundaries may need realignment"
            )
        elif measurement.boundary_erosion > 30:
            recommendations.append(
                "Monitor anti-corruption layer usage — early signs of boundary "
                "erosion. Review context map for accuracy"
            )

        # Overall assessment
        if risk == "critical":
            assessment = (
                "Platform is becoming legacy. Domain models have significantly "
                "diverged from business reality. Reframe maintenance as 'domain "
                "alignment preservation' and secure investment for remediation."
            )
        elif risk == "high":
            assessment = (
                "Significant domain drift detected. Without intervention, the "
                "platform will increasingly feel like a constraint rather than "
                "an enabler. Prioritize domain realignment."
            )
        elif risk == "moderate":
            assessment = (
                "Some domain drift present. Schedule quarterly domain alignment "
                "reviews to prevent further divergence."
            )
        else:
            assessment = (
                "Platform models closely align with business reality. Continue "
                "quarterly entropy tracking to maintain alignment."
            )

        return {
            "context": measurement.context_name,
            "quarter": measurement.quarter,
            "entropy_score": round(score, 1),
            "risk_level": risk,
            "assessment": assessment,
            "recommendations": recommendations,
            "scores": {k: round(v, 1) for k, v in measurement.scores.items()},
        }

    def portfolio_summary(self) -> dict:
        """Aggregate entropy metrics across all bounded contexts."""
        if not self._trends:
            return {}

        latest_measurements = []
        for trend in self._trends.values():
            if trend.latest:
                latest_measurements.append(trend.latest)

        if not latest_measurements:
            return {}

        total = len(latest_measurements)
        avg_entropy = sum(m.entropy_score for m in latest_measurements) / total
        avg_by_dim = {}
        for dim in ENTROPY_DIMENSIONS:
            dim_key = {
                "Model Drift": "model_drift",
                "Path Staleness": "path_staleness",
                "Boundary Erosion": "boundary_erosion",
            }[dim]
            avg_by_dim[dim] = sum(
                getattr(m, dim_key) for m in latest_measurements
            ) / total

        risk_counts = {"low": 0, "moderate": 0, "high": 0, "critical": 0}
        for m in latest_measurements:
            risk_counts[m.risk_level] += 1

        rising_contexts = []
        for name, trend in self._trends.items():
            if trend.trend_direction == "rising":
                rising_contexts.append(name)

        return {
            "total_contexts": total,
            "avg_entropy_score": round(avg_entropy, 1),
            "avg_by_dimension": {k: round(v, 1) for k, v in avg_by_dim.items()},
            "risk_distribution": risk_counts,
            "rising_entropy_contexts": rising_contexts,
        }

    @property
    def all_trends(self) -> dict[str, EntropyTrend]:
        return dict(self._trends)


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Platform Entropy Score")
    print("  Chapter 7: Measuring Platform Success")
    print("=" * 70)

    scorer = PlatformEntropyScorer()

    # ── Q1 2026 measurements ──
    q1_data = [
        EntropyMeasurement(
            context_name="Payments",
            quarter="Q1 2026",
            model_drift=15, path_staleness=10, boundary_erosion=8,
        ),
        EntropyMeasurement(
            context_name="Commerce",
            quarter="Q1 2026",
            model_drift=25, path_staleness=30, boundary_erosion=20,
        ),
        EntropyMeasurement(
            context_name="Analytics",
            quarter="Q1 2026",
            model_drift=35, path_staleness=45, boundary_erosion=30,
        ),
        EntropyMeasurement(
            context_name="Risk & Compliance",
            quarter="Q1 2026",
            model_drift=20, path_staleness=15, boundary_erosion=12,
        ),
        EntropyMeasurement(
            context_name="Customer Identity",
            quarter="Q1 2026",
            model_drift=40, path_staleness=55, boundary_erosion=45,
        ),
    ]

    # ── Q2 2026 measurements (entropy has changed) ──
    q2_data = [
        EntropyMeasurement(
            context_name="Payments",
            quarter="Q2 2026",
            model_drift=18, path_staleness=12, boundary_erosion=10,
        ),
        EntropyMeasurement(
            context_name="Commerce",
            quarter="Q2 2026",
            model_drift=35, path_staleness=40, boundary_erosion=30,
        ),
        EntropyMeasurement(
            context_name="Analytics",
            quarter="Q2 2026",
            model_drift=30, path_staleness=40, boundary_erosion=25,
        ),
        EntropyMeasurement(
            context_name="Risk & Compliance",
            quarter="Q2 2026",
            model_drift=22, path_staleness=18, boundary_erosion=15,
        ),
        EntropyMeasurement(
            context_name="Customer Identity",
            quarter="Q2 2026",
            model_drift=55, path_staleness=65, boundary_erosion=58,
        ),
    ]

    for m in q1_data + q2_data:
        scorer.record(m)

    # ── Entropy dimensions ──
    print(f"\n  ENTROPY DIMENSIONS")
    print(f"  {'─' * 66}")
    for dim in ENTROPY_DIMENSIONS:
        print(f"    {dim:<20} {DIMENSION_DESCRIPTIONS[dim][:60]}...")

    # ── Current quarter assessments ──
    print(f"\n\n  CONTEXT ENTROPY PROFILES (Q2 2026)")
    print(f"  {'─' * 66}")

    for m in q2_data:
        result = scorer.assess(m)
        risk_icon = {
            "low": "●", "moderate": "◐", "high": "○", "critical": "◉"
        }[result["risk_level"]]
        risk_label = {
            "low": "Low", "moderate": "Moderate", "high": "HIGH", "critical": "CRITICAL"
        }[result["risk_level"]]

        # Get trend
        trend = scorer.all_trends[m.context_name]
        trend_dir = trend.trend_direction
        delta = trend.quarter_over_quarter_delta
        trend_icon = {"rising": "↑", "falling": "↓", "stable": "→", "insufficient_data": "—"}[trend_dir]
        delta_str = f" ({delta:+.1f})" if delta is not None else ""

        print(f"\n    {risk_icon} {m.context_name}")
        print(f"      Entropy Score: {result['entropy_score']:.0f}  |  "
              f"Risk: {risk_label}  |  Trend: {trend_icon}{delta_str}")
        print()

        # ASCII bars
        bar_width = 40
        for dim in ENTROPY_DIMENSIONS:
            score = result["scores"][dim]
            filled = int(score / 100 * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            print(f"      {dim:<20} {bar} {score:>5.1f}")

        # Assessment
        print(f"\n      → {result['assessment'][:80]}")
        if len(result['assessment']) > 80:
            print(f"        {result['assessment'][80:]}")
        for rec in result["recommendations"]:
            print(f"        • {rec[:75]}")
            if len(rec) > 75:
                print(f"          {rec[75:]}")

    # ── Portfolio summary ──
    summary = scorer.portfolio_summary()
    print(f"\n\n  PORTFOLIO ENTROPY SUMMARY")
    print(f"  {'─' * 66}")
    print(f"    Contexts assessed      : {summary['total_contexts']}")
    print(f"    Average entropy score  : {summary['avg_entropy_score']}")
    print()
    print(f"    Dimension averages:")
    for dim in ENTROPY_DIMENSIONS:
        avg = summary["avg_by_dimension"][dim]
        bar_width = 40
        filled = int(avg / 100 * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"      {dim:<20} {bar} {avg:>5.1f}")

    print(f"\n    Risk distribution:")
    for risk, count in summary["risk_distribution"].items():
        bar = "█" * count + "░" * (5 - count)
        label = {
            "low": "Low      ", "moderate": "Moderate ",
            "high": "High     ", "critical": "Critical "
        }[risk]
        print(f"      {label} {bar}  {count}")

    if summary["rising_entropy_contexts"]:
        print(f"\n    ⚠ Rising entropy detected in: {', '.join(summary['rising_entropy_contexts'])}")
        print(f"      These contexts are drifting further from domain truth.")
        print(f"      A rising entropy score is the leading indicator that your")
        print(f"      platform is becoming legacy in these areas.")

    # ── Trend analysis ──
    print(f"\n\n  QUARTER-OVER-QUARTER TREND")
    print(f"  {'─' * 66}")
    print(f"    {'Context':<22} {'Q1 Score':>10} {'Q2 Score':>10} {'Delta':>8} {'Trend':>8}")
    print(f"    {'─' * 58}")
    for name, trend in scorer.all_trends.items():
        q1_score = trend.measurements[0].entropy_score
        q2_score = trend.measurements[1].entropy_score
        delta = q2_score - q1_score
        trend_dir = trend.trend_direction
        trend_icon = {"rising": "↑ Rising", "falling": "↓ Falling", "stable": "→ Stable"}[trend_dir]
        print(f"    {name:<22} {q1_score:>10.1f} {q2_score:>10.1f} {delta:>+8.1f} {trend_icon:>8}")

    # ── Key insight ──
    print(f"\n\n  {'─' * 66}")
    print(f"  KEY INSIGHT: The Platform Entropy Score is the leading indicator")
    print(f"  that your platform is becoming legacy. Unlike DORA metrics (speed)")
    print(f"  or adoption metrics (usage), entropy measures whether the platform")
    print(f"  still accurately represents the business. Track it quarterly.")
    print(f"  Reframe platform maintenance from 'technical debt cleanup' to")
    print(f"  'domain alignment preservation' — a narrative that sustains")
    print(f"  investment long after the initial build excitement fades.")
    print()
    print(f"  Interactive version: https://ddpe.platformetrics.com")
    print("=" * 70)
