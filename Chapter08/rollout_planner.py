# rollout_planner.py
"""Four-Phase Platform Rollout Strategy"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class RolloutPhase:
    name: str
    stage: str
    duration_weeks: str
    contexts: str
    activities: List[str]
    success_criteria: List[str]
    ddd_focus: str

ROLLOUT_PHASES = [
    RolloutPhase(
        name="Phase 1", stage="Pilot",
        duration_weeks="8-12", contexts="1 bounded context",
        activities=[
            "Platform build alongside willing team",
            "Team training and adoption support",
            "Co-development of domain abstractions",
            "Intensive support and rapid iteration",
        ],
        success_criteria=[
            "Proof of concept validated in production",
            "Pilot team reports measurable friction reduction",
            "Domain abstractions documented and tested",
        ],
        ddd_focus="Context map (Draft)",
    ),
    RolloutPhase(
        name="Phase 2", stage="Early Expansion",
        duration_weeks="12-16", contexts="2-3 related contexts",
        activities=[
            "Integrate related bounded contexts",
            "Stabilize ubiquitous language across contexts",
            "Build shared kernels where appropriate",
            "Grow adoption organically via success stories",
        ],
        success_criteria=[
            "10-15% adoption across target domains",
            "Ubiquitous language agreed and documented",
            "Cross-domain collaboration patterns established",
        ],
        ddd_focus="Shared kernels (Identified)",
    ),
    RolloutPhase(
        name="Phase 3", stage="Broad Adoption",
        duration_weeks="16-24", contexts="Multiple domains (40%+)",
        activities=[
            "Cross-domain integration via published language",
            "Establish governance frameworks",
            "Anti-corruption layers at all domain boundaries",
            "Reference architectures for each domain",
        ],
        success_criteria=[
            "40%+ adoption across organization",
            "Published language stable and versioned",
            "Cross-domain consistency verified",
        ],
        ddd_focus="Published language (Stable)",
    ),
    RolloutPhase(
        name="Phase 4", stage="Org Standard",
        duration_weeks="Ongoing", contexts="Organization-wide (70%+)",
        activities=[
            "Optimize operations and observability",
            "Innovation support for new domains",
            "Continuous governance and evolution",
            "Platform drives organizational change",
        ],
        success_criteria=[
            "70%+ adoption, platform is institutional infrastructure",
            "Domain abstractions drive competitive advantage",
            "Governance frameworks actively maintained",
        ],
        ddd_focus="Strategic DDD (Governance)",
    ),
]

def print_rollout_plan():
    print("=== Phased Rollout Plan ===")
    for phase in ROLLOUT_PHASES:
        print(f"\n{phase.name}: {phase.stage} ({phase.duration_weeks} weeks)")
        print(f"  → {phase.contexts}")
        print(f"  → DDD Focus: {phase.ddd_focus}")
        for activity in phase.activities:
            print(f"     • {activity}")

print_rollout_plan()
