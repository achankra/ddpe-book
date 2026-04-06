# patient_data_domain.py
"""Healthcare Patient Data Domain — Secure Defaults"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Set
from enum import Enum

class AccessPurpose(Enum):
    DIRECT_CARE = "direct-patient-care"
    TREATMENT_PLANNING = "treatment-planning"
    BILLING = "billing"
    RESEARCH = "research"
    QUALITY_IMPROVEMENT = "quality-improvement"

@dataclass
class CareTeam:
    id: str
    name: str          # e.g. "Cardiology Team, ICU Hospital A"
    members: Set[str]  # user IDs
    patient_scope: Set[str]  # patient IDs within scope

@dataclass
class AuditEntry:
    timestamp: datetime
    user_id: str
    patient_id: str
    data_elements: List[str]
    purpose: AccessPurpose
    granted: bool
    care_team: str

class PatientDataDomain:
    """Shared kernel — all bounded contexts depend on this."""

    def __init__(self):
        self.care_teams: List[CareTeam] = []
        self.audit_log: List[AuditEntry] = []

    def access_patient_data(
        self, user_id: str, patient_id: str,
        purpose: AccessPurpose, data_elements: List[str]
    ) -> dict:
        # Find user's care team
        team = self._find_care_team(user_id, patient_id)
        granted = team is not None

        # ALWAYS audit — regardless of grant/deny
        self.audit_log.append(AuditEntry(
            timestamp=datetime.now(),
            user_id=user_id, patient_id=patient_id,
            data_elements=data_elements, purpose=purpose,
            granted=granted,
            care_team=team.name if team else "NONE",
        ))

        if not granted:
            return {"access": "DENIED", "reason": "Not a member of patient care team"}
        return {"access": "GRANTED", "care_team": team.name, "purpose": purpose.value}

    def _find_care_team(self, user_id: str, patient_id: str):
        for team in self.care_teams:
            if user_id in team.members and patient_id in team.patient_scope:
                return team
        return None
