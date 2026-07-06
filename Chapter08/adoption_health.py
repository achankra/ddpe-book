# adoption_health.py
"""Platform Adoption Anti-Pattern Detection"""
from dataclasses import dataclass
from typing import List

@dataclass
class AntiPatternAssessment:
    name: str
    description: str
    severity: int  # 1-5
    warning_signs: List[str]
    interventions: List[str]

ANTI_PATTERNS = [
    AntiPatternAssessment(
        name="Build-it-and-they-will-come",
        description="Assuming superior technology guarantees adoption",
        severity=0,
        warning_signs=[
            "No user research before building features",
            "Platform roadmap driven by tech trends, not user needs",
            "Low adoption despite feature completeness",
        ],
        interventions=[
            "Co-develop with 2-3 pilot teams",
            "Run developer interviews before each major feature",
            "Publish adoption metrics transparently",
        ],
    ),
    AntiPatternAssessment(
        name="Platform-as-Gatekeeper",
        description="Platform team must approve every usage",
        severity=0,
        warning_signs=[
            "Teams waiting days for platform approvals",
            "Shadow infrastructure appearing",
            "Developers building workarounds",
        ],
        interventions=[
            "Move to self-service with guardrails",
            "Automate approval for standard patterns",
            "Reserve manual review for high-risk deviations only",
        ],
    ),
    AntiPatternAssessment(
        name="Ignoring-Bounded-Context-Boundaries",
        description="Forcing one domain model across all contexts",
        severity=0,
        warning_signs=[
            "Teams complaining about 'one-size-fits-all'",
            "Translation friction between domain concepts",
            "High customization request volume",
        ],
        interventions=[
            "Context map before scaling to new domains",
            "Anti-corruption layers at domain boundaries",
            "Allow domain-specific extensions of platform concepts",
        ],
    ),
]

def run_health_check(scores: dict):
    """scores: dict mapping anti-pattern name to severity (1-5)"""
    print("=== Platform Adoption Health Check ===")
    total = 0
    for ap in ANTI_PATTERNS:
        score = scores.get(ap.name, 0)
        ap.severity = score
        label = "LOW" if score <= 2 else "MODERATE" if score <= 3 else "SEVERE"
        icon = "✓" if score <= 2 else "⚠"
        print(f"{icon} {ap.name}: {score}/5 ({label})")
        total += (5 - score) * 20 / len(ANTI_PATTERNS)
    print(f"\nOverall Health Score: {total:.0f}/100")


if __name__ == "__main__":
    print("=" * 62)
    print("  Platform Adoption Health Check — Anti-Pattern Assessment")
    print("=" * 62)

    print("\n  Known anti-patterns being evaluated:")
    for ap in ANTI_PATTERNS:
        print(f"    - {ap.name}: {ap.description}")

    # Simulate a platform with mixed health
    scores = {
        "Build-it-and-they-will-come": 4,   # Severe
        "Platform-as-Gatekeeper": 2,        # Low
        "Ignoring-Bounded-Context-Boundaries": 3,  # Moderate
    }

    print()
    run_health_check(scores)

    # Show interventions for severe cases
    print("\n  Recommended Interventions:")
    for ap in ANTI_PATTERNS:
        if ap.severity >= 3:
            print(f"\n    {ap.name} (severity {ap.severity}/5):")
            for warning in ap.warning_signs:
                print(f"      Warning sign: {warning}")
            for action in ap.interventions:
                print(f"      -> {action}")

    print("=" * 62)
