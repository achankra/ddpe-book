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


if __name__ == "__main__":
    print("=" * 62)
    print("  Patient Data Domain — Access Control & Audit Demo")
    print("=" * 62)

    domain = PatientDataDomain()

    # Set up care teams
    cardiology = CareTeam(
        id="CT-001", name="Cardiology Team, City Hospital",
        members={"dr-smith", "nurse-jones"},
        patient_scope={"patient-101", "patient-102"})
    oncology = CareTeam(
        id="CT-002", name="Oncology Team, City Hospital",
        members={"dr-patel"},
        patient_scope={"patient-201"})
    domain.care_teams = [cardiology, oncology]

    print(f"\n  Care Teams:")
    for team in domain.care_teams:
        print(f"    {team.name}")
        print(f"      Members : {', '.join(team.members)}")
        print(f"      Patients: {', '.join(team.patient_scope)}")

    # Access scenarios
    scenarios = [
        ("dr-smith", "patient-101", AccessPurpose.DIRECT_CARE,
         ["vitals", "medications"], "Cardiologist accessing own patient"),
        ("dr-smith", "patient-201", AccessPurpose.DIRECT_CARE,
         ["vitals"], "Cardiologist accessing oncology patient"),
        ("nurse-jones", "patient-102", AccessPurpose.TREATMENT_PLANNING,
         ["lab_results"], "Nurse accessing care-team patient"),
        ("dr-unknown", "patient-101", AccessPurpose.RESEARCH,
         ["demographics"], "Unknown doctor requesting research access"),
    ]

    print(f"\n  Access Requests:")
    for user, patient, purpose, elements, desc in scenarios:
        result = domain.access_patient_data(user, patient, purpose, elements)
        status = result["access"]
        icon = "GRANTED" if status == "GRANTED" else "DENIED "
        print(f"\n    {desc}")
        print(f"      {user} -> {patient} ({purpose.value})")
        print(f"      Result: {icon}", end="")
        if status == "GRANTED":
            print(f" via {result['care_team']}")
        else:
            print(f" — {result['reason']}")

    print(f"\n  Audit Log ({len(domain.audit_log)} entries — every access recorded):")
    for entry in domain.audit_log:
        g = "GRANT" if entry.granted else "DENY "
        print(f"    [{g}] {entry.user_id} -> {entry.patient_id} "
              f"({entry.purpose.value})")
    print("=" * 62)
