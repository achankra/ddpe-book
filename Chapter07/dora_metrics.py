# dora_metrics.py
"""Domain-Aware DORA Metrics Tracker"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

@dataclass
class Deployment:
    service: str
    domain: str
    team: str
    timestamp: datetime
    lead_time_hours: float
    is_failure: bool = False
    recovery_time_hours: float = 0.0

class DORATracker:
    def __init__(self):
        self.deployments: List[Deployment] = []

    def record(self, deployment: Deployment):
        self.deployments.append(deployment)

    def metrics_by_domain(self, days: int = 30) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [d for d in self.deployments if d.timestamp > cutoff]
        by_domain = defaultdict(list)
        for d in recent:
            by_domain[d.domain].append(d)

        results = {}
        for domain, deps in by_domain.items():
            total = len(deps)
            failures = [d for d in deps if d.is_failure]
            results[domain] = {
                "deployment_frequency": total / (days / 7),  # per week
                "avg_lead_time_hours": sum(d.lead_time_hours for d in deps) / total,
                "change_failure_rate": len(failures) / total * 100,
                "avg_mttr_hours": (
                    sum(d.recovery_time_hours for d in failures) / len(failures)
                    if failures else 0
                ),
            }
        return results
