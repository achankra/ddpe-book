"""
Chapter 7: Developer Friction Score — Multi-Domain Assessment

Extends the friction_score.py calculator to show a full portfolio
assessment across three domains, with per-source breakdown, trend
analysis, and cross-domain comparison.

Run: python Chapter07/run_friction_score.py
"""

from dataclasses import dataclass
from typing import List


@dataclass
class FrictionSource:
    name: str
    score: float        # 1-10 severity
    weight: float       # 0-1 importance
    multiplier: float   # <1 = improving, >1 = worsening

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    @property
    def predictive_score(self) -> float:
        return self.score * self.weight * self.multiplier


# ── Friction profiles per domain ────────────────────────────────────

DOMAIN_PROFILES = {
    "Payments": [
        FrictionSource("Cross-team dependencies", 8, 0.30, 1.2),
        FrictionSource("Test flakiness", 6, 0.20, 0.9),
        FrictionSource("Security assessments", 7, 0.25, 1.1),
        FrictionSource("Legacy integration", 9, 0.15, 1.3),
        FrictionSource("Build times", 5, 0.10, 0.8),
    ],
    "Healthcare": [
        FrictionSource("Compliance reviews", 9, 0.30, 1.0),
        FrictionSource("Data access approvals", 8, 0.25, 1.1),
        FrictionSource("Test flakiness", 4, 0.15, 0.8),
        FrictionSource("Environment provisioning", 7, 0.20, 0.9),
        FrictionSource("Build times", 3, 0.10, 1.0),
    ],
    "Marketing": [
        FrictionSource("Cross-team dependencies", 3, 0.20, 0.7),
        FrictionSource("Test flakiness", 7, 0.25, 1.2),
        FrictionSource("Security assessments", 2, 0.10, 1.0),
        FrictionSource("Environment provisioning", 8, 0.30, 1.3),
        FrictionSource("Build times", 6, 0.15, 0.9),
    ],
}


def calculate_friction(sources: List[FrictionSource]):
    """Calculate current and predictive friction scores."""
    current = sum(s.weighted_score for s in sources)
    predictive = sum(s.predictive_score for s in sources)
    delta = ((predictive - current) / current) * 100 if current else 0
    return current, predictive, delta


def main():
    print("=" * 64)
    print("DEVELOPER FRICTION SCORE — MULTI-DOMAIN ASSESSMENT")
    print("=" * 64)

    print("\n  Scoring: severity (1-10) × weight (0-1) = weighted score")
    print("  Multiplier: <1 improving, >1 worsening")
    print("  Predictive = weighted × multiplier (shows trajectory)")

    summaries = []

    for domain, sources in DOMAIN_PROFILES.items():
        current, predictive, delta = calculate_friction(sources)
        summaries.append((domain, current, predictive, delta))

        print(f"\n{'─' * 64}")
        print(f"  {domain.upper()} DOMAIN")
        print(f"{'─' * 64}")

        # Per-source breakdown
        print(f"\n  {'Source':<28s} {'Sev':>4s} {'Wt':>5s} {'Score':>6s} {'Mult':>5s} {'Pred':>6s} {'Trend':>6s}")
        print(f"  {'─' * 28} {'─' * 4} {'─' * 5} {'─' * 6} {'─' * 5} {'─' * 6} {'─' * 6}")

        for s in sorted(sources, key=lambda x: x.weighted_score, reverse=True):
            trend = "↑" if s.multiplier > 1.05 else "↓" if s.multiplier < 0.95 else "→"
            print(f"  {s.name:<28s} {s.score:>4.0f} {s.weight:>5.2f} {s.weighted_score:>6.2f}"
                  f" {s.multiplier:>5.1f} {s.predictive_score:>6.2f}  {trend}")

        print(f"\n  Current Friction Score:    {current:.2f}")
        print(f"  Predictive Friction Score: {predictive:.2f}")

        if delta > 10:
            print(f"  ⚠  Predicted increase of {delta:.1f}% — investigate worsening sources")
        elif delta > 0:
            print(f"  ↗  Slight upward trend ({delta:+.1f}%)")
        elif delta < -10:
            print(f"  ✅ Predicted decrease of {abs(delta):.1f}% — improvements taking effect")
        else:
            print(f"  →  Stable ({delta:+.1f}%)")

        # Top friction source
        top = max(sources, key=lambda s: s.weighted_score)
        print(f"  Top friction source: {top.name} (weighted: {top.weighted_score:.2f})")

    # ── Cross-domain comparison ──
    print(f"\n{'=' * 64}")
    print("CROSS-DOMAIN COMPARISON")
    print("=" * 64)

    print(f"\n  {'Domain':<16s} {'Current':>8s} {'Predicted':>10s} {'Delta':>8s} {'Status'}")
    print(f"  {'─' * 16} {'─' * 8} {'─' * 10} {'─' * 8} {'─' * 16}")

    for domain, current, predictive, delta in sorted(summaries, key=lambda x: x[1], reverse=True):
        if delta > 10:
            status = "⚠  Worsening"
        elif delta < -10:
            status = "✅ Improving"
        else:
            status = "→  Stable"
        print(f"  {domain:<16s} {current:>8.2f} {predictive:>10.2f} {delta:>+7.1f}%  {status}")

    # ── Recommendations ──
    print(f"\n{'=' * 64}")
    print("RECOMMENDATIONS")
    print("=" * 64)

    worst = max(summaries, key=lambda x: x[1])
    most_worsening = max(summaries, key=lambda x: x[3])
    print(f"\n  Highest friction:  {worst[0]} (score: {worst[1]:.2f})")
    print(f"  Fastest worsening: {most_worsening[0]} (delta: {most_worsening[3]:+.1f}%)")

    # Find the top worsening source across all domains
    all_worsening = []
    for domain, sources in DOMAIN_PROFILES.items():
        for s in sources:
            if s.multiplier > 1.0:
                all_worsening.append((domain, s))

    all_worsening.sort(key=lambda x: x[1].predictive_score - x[1].weighted_score, reverse=True)

    if all_worsening:
        print(f"\n  Top worsening friction sources (across all domains):")
        for domain, s in all_worsening[:5]:
            increase = s.predictive_score - s.weighted_score
            print(f"    {domain}/{s.name}: +{increase:.2f} (×{s.multiplier})")

    print(f"\n  Domain-driven platforms reduce friction by encoding domain")
    print(f"  knowledge into the platform layer. Cross-team dependencies")
    print(f"  and compliance reviews are the top candidates for automation.")


if __name__ == "__main__":
    main()
