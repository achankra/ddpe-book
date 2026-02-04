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
    "peripheral": EvolutionPolicy(
        layer="peripheral",
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
