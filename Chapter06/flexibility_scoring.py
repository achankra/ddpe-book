"""Flexibility Scoring Tool — Chapter 6: Golden Paths and API Design per Domain

Evaluates the balance between standardization and flexibility across platform
configuration areas. Each area is scored on two axes:
  - Standardization (1-5): 1=No standard → 5=Blocked/Mandatory
  - Flexibility     (1-5): 1=No flexibility → 5=Full flexibility

Plus qualitative assessments of developer friction and risk level.
The tool generates recommendations to help find the right balance.

Mirrors the Flexibility Scoring tab in the interactive tool at
https://ddpe.platformetrics.com/tools/api-design-standards

See also: override_validator.py for the 80-15-5 override pyramid.
"""

from dataclasses import dataclass
from typing import Optional


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class ConfigArea:
    """A platform configuration area to be assessed."""
    name: str
    current_policy: str
    standardization: int     # 1-5: 1=No standard, 5=Blocked/Mandatory
    flexibility: int         # 1-5: 1=No flexibility, 5=Full flexibility
    friction: str            # "low", "medium", "high"
    risk: str                # "low", "medium", "high", "critical"


@dataclass
class ScoringResult:
    """Assessment result for a single configuration area."""
    area: str
    standardization: int
    flexibility: int
    balance_score: float     # how well balanced (0-1, higher = better)
    recommendation: str
    recommendation_detail: str


# ============================================================================
# Scoring Engine
# ============================================================================

class FlexibilityScoringTool:
    """Scores the standardization-flexibility balance across config areas.

    The tool identifies:
    - Over-standardization: high std + low flex → developer friction
    - Under-standardization: low std + high flex → inconsistency risk
    - Good balance: appropriate std + flex for the risk level
    - Appropriate locks: high std + low flex justified by critical risk
    """

    FRICTION_WEIGHT = {"low": 0, "medium": 1, "high": 2}
    RISK_WEIGHT = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    def score(self, area: ConfigArea) -> ScoringResult:
        std = area.standardization
        flex = area.flexibility
        friction_w = self.FRICTION_WEIGHT[area.friction]
        risk_w = self.RISK_WEIGHT[area.risk]

        # Balance score: penalize extremes, reward proportional std/flex
        # Perfect balance = std + flex ≈ 6, neither too extreme
        total = std + flex
        spread = abs(std - flex)

        # Determine recommendation
        if risk_w >= 2 and std >= 4 and flex <= 2:
            # High/critical risk with strong standardization = appropriate
            rec = "No change needed"
            detail = (f"High standardization with low flexibility is appropriate "
                      f"for {area.risk}-risk configurations. Security and compliance "
                      f"requirements justify the restriction.")
            balance = 0.9

        elif std >= 4 and flex <= 2 and friction_w >= 1:
            # Over-standardized with friction
            rec = "Review friction points"
            detail = (f"'{area.name}' has high standardization (std={std}) but "
                      f"low flexibility (flex={flex}) with {area.friction} friction. "
                      f"Consider whether some configurations could move to "
                      f"'governed' tier to reduce developer friction while "
                      f"maintaining oversight.")
            balance = 0.3

        elif std <= 2 and flex >= 4:
            # Under-standardized
            rec = "Consider more guidance"
            detail = (f"'{area.name}' has low standardization (std={std}) and "
                      f"high flexibility (flex={flex}). While this maximizes "
                      f"autonomy, it may lead to inconsistency across teams. "
                      f"Consider adding lightweight standards or documented "
                      f"recommendations without restricting choice.")
            balance = 0.4

        elif 2 <= spread <= 3 and friction_w == 0:
            # Reasonable spread, low friction
            rec = "Good balance"
            detail = (f"'{area.name}' shows a reasonable balance between "
                      f"standardization (std={std}) and flexibility (flex={flex}) "
                      f"with low friction. The current policy is working well.")
            balance = 0.8

        elif spread <= 1 and std >= 3:
            # Both moderate-high, could indicate confusion
            rec = "Appropriate balance"
            detail = (f"'{area.name}' has similar standardization and flexibility "
                      f"scores (std={std}, flex={flex}), suggesting a governed "
                      f"approach with clear override paths. Monitor for friction.")
            balance = 0.7

        else:
            rec = "Needs review"
            detail = (f"'{area.name}' (std={std}, flex={flex}, "
                      f"friction={area.friction}, risk={area.risk}) may benefit "
                      f"from re-evaluation. Consider whether the current policy "
                      f"matches the actual risk profile.")
            balance = 0.5

        return ScoringResult(
            area=area.name,
            standardization=std,
            flexibility=flex,
            balance_score=balance,
            recommendation=rec,
            recommendation_detail=detail
        )

    def assess_portfolio(self, areas: list[ConfigArea]) -> dict:
        """Score all areas and produce portfolio-level metrics."""
        results = [self.score(a) for a in areas]

        avg_std = sum(a.standardization for a in areas) / len(areas)
        avg_flex = sum(a.flexibility for a in areas) / len(areas)
        avg_balance = sum(r.balance_score for r in results) / len(results)

        return {
            "results": results,
            "avg_standardization": avg_std,
            "avg_flexibility": avg_flex,
            "avg_balance": avg_balance,
            "areas_assessed": len(areas),
        }


# ============================================================================
# Demo — matches the interactive tool at ddpe.platformetrics.com
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Flexibility Scoring Tool")
    print("  Chapter 6: Golden Paths and API Design per Domain")
    print("=" * 70)

    # Sample configuration areas (matching the interactive tool's defaults)
    areas = [
        ConfigArea("Database Engine",      "Governed override",              4, 2, "medium", "medium"),
        ConfigArea("Compute Sizing",       "Flexible",                       2, 5, "low",    "low"),
        ConfigArea("Network Exposure",     "Blocked for sensitive domains",  5, 1, "low",    "high"),
        ConfigArea("Encryption Settings",  "Blocked",                        5, 1, "low",    "critical"),
        ConfigArea("Log Retention",        "Domain-specific",                3, 3, "low",    "medium"),
        ConfigArea("CI/CD Pipeline",       "Standardized",                   5, 1, "medium", "low"),
    ]

    tool = FlexibilityScoringTool()
    portfolio = tool.assess_portfolio(areas)

    # Portfolio summary
    print(f"\n  PORTFOLIO SUMMARY")
    print(f"  {'─' * 66}")
    print(f"    Avg Standardization : {portfolio['avg_standardization']:.1f} / 5.0")
    print(f"    Avg Flexibility     : {portfolio['avg_flexibility']:.1f} / 5.0")
    print(f"    Areas Assessed      : {portfolio['areas_assessed']}")
    print(f"    Overall Balance     : {portfolio['avg_balance']:.0%}")

    # Scoring scale reference
    print(f"\n  SCORING SCALES")
    print(f"  {'─' * 66}")
    print(f"    Standardization: 1=No standard → 5=Blocked/Mandatory")
    print(f"    Flexibility:     1=No flexibility → 5=Full flexibility")
    print(f"    Friction:        Low=Rarely complained → High=Frequent escalations")
    print(f"    Risk:            Low=Convenience → Critical=Major breach potential")

    # Detailed results
    print(f"\n  AREA-BY-AREA ASSESSMENT")
    print(f"  {'─' * 66}")

    for result in portfolio["results"]:
        area = next(a for a in areas if a.name == result.area)
        print(f"\n    {result.area}")
        print(f"      Policy:    {area.current_policy}")
        print(f"      Std={result.standardization}  Flex={result.flexibility}  "
              f"Friction={area.friction}  Risk={area.risk}")
        print(f"      → {result.recommendation}")
        print(f"        {result.recommendation_detail}")

    # Identify action items
    print(f"\n\n  ACTION ITEMS")
    print(f"  {'─' * 66}")

    needs_attention = [r for r in portfolio["results"]
                       if r.recommendation in ("Review friction points",
                                                "Consider more guidance",
                                                "Needs review")]
    good = [r for r in portfolio["results"]
            if r.recommendation in ("No change needed", "Good balance",
                                    "Appropriate balance")]

    if needs_attention:
        print(f"    Areas needing attention ({len(needs_attention)}):")
        for r in needs_attention:
            print(f"      • {r.area}: {r.recommendation}")
    else:
        print(f"    No areas require immediate attention.")

    print(f"\n    Areas well-balanced ({len(good)}):")
    for r in good:
        print(f"      • {r.area}: {r.recommendation}")

    print(f"\n\n  {'─' * 66}")
    print(f"  KEY INSIGHT: The goal is not maximum flexibility or maximum")
    print(f"  standardization — it's the right balance for each area's risk")
    print(f"  profile. Critical-risk areas deserve strong locks. Low-risk")
    print(f"  areas deserve full autonomy. The friction signal tells you")
    print(f"  when the balance is wrong.")
    print()
    print(f"  Interactive version: https://ddpe.platformetrics.com")
    print("=" * 70)
