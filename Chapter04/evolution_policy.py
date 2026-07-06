# evolution_policy.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class ChangeType(Enum):
    PATCH = "patch"      # Bug fixes, no API changes
    MINOR = "minor"      # Additive changes, backward compatible
    MAJOR = "major"      # Breaking changes

@dataclass
class EvolutionPolicy:
    layer: str
    deprecation_notice_days: int
    migration_support_months: int
    breaking_change_allowed: bool

    def can_release(self, change_type: ChangeType, 
                    deprecation_date: datetime = None) -> bool:
        if change_type == ChangeType.MAJOR:
            if not self.breaking_change_allowed:
                return False
            if deprecation_date:
                notice_given = (datetime.now() - deprecation_date).days
                return notice_given >= self.deprecation_notice_days
        return True

# Layer-specific policies
POLICIES = {
    "core": EvolutionPolicy(
        layer="core",
        deprecation_notice_days=90,
        migration_support_months=12,
        breaking_change_allowed=True  # With extended notice
    ),
    "domain": EvolutionPolicy(
        layer="domain",
        deprecation_notice_days=30,
        migration_support_months=6,
        breaking_change_allowed=True
    ),
    "extension": EvolutionPolicy(
        layer="extension",
        deprecation_notice_days=14,
        migration_support_months=3,
        breaking_change_allowed=True
    )
}


if __name__ == "__main__":
    print("=" * 62)
    print("  Evolution Policy — Versioning Rules Per Platform Layer")
    print("=" * 62)

    for name, policy in POLICIES.items():
        print(f"\n  [{policy.layer.upper()} layer]")
        print(f"    Deprecation notice : {policy.deprecation_notice_days} days")
        print(f"    Migration support  : {policy.migration_support_months} months")
        print(f"    Breaking changes   : {'Allowed (with notice)' if policy.breaking_change_allowed else 'Not allowed'}")

    print("\n" + "-" * 62)
    print("  Release Scenarios:")

    scenarios = [
        ("core",      ChangeType.PATCH, None,                                "Bug fix to core"),
        ("core",      ChangeType.MAJOR, None,                                "Major core change (no notice)"),
        ("core",      ChangeType.MAJOR, datetime.now() - timedelta(days=91), "Major core change (91 days notice)"),
        ("domain",    ChangeType.MINOR, None,                                "Minor domain addition"),
        ("domain",    ChangeType.MAJOR, datetime.now() - timedelta(days=15), "Major domain change (15 days notice)"),
        ("extension", ChangeType.MAJOR, datetime.now() - timedelta(days=14), "Major extension change (14 days notice)"),
    ]

    for layer, change, dep_date, description in scenarios:
        policy = POLICIES[layer]
        allowed = policy.can_release(change, dep_date)
        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"\n    {description}")
        print(f"      Layer: {layer}, Change: {change.value} -> {status}")

    print("\n" + "=" * 62)
