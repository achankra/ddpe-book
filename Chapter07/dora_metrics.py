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


if __name__ == "__main__":
    print("=" * 62)
    print("  Domain-Aware DORA Metrics — Multi-Domain Demo")
    print("=" * 62)

    tracker = DORATracker()
    now = datetime.now()

    # Payments domain: frequent deploys, low failure rate
    for i in range(12):
        tracker.record(Deployment(
            service="payment-api", domain="payments", team="payments-team",
            timestamp=now - timedelta(days=i * 2),
            lead_time_hours=4.0 + (i % 3), is_failure=(i == 5),
            recovery_time_hours=0.5 if i == 5 else 0.0))

    # Inventory domain: slower, higher failure rate
    for i in range(5):
        tracker.record(Deployment(
            service="inventory-svc", domain="inventory", team="warehouse-team",
            timestamp=now - timedelta(days=i * 5),
            lead_time_hours=24.0 + (i * 4), is_failure=(i % 2 == 0),
            recovery_time_hours=4.0 if i % 2 == 0 else 0.0))

    results = tracker.metrics_by_domain(days=30)

    for domain, m in results.items():
        print(f"\n  [{domain.upper()}]")
        print(f"    Deployment Frequency  : {m['deployment_frequency']:.1f} / week")
        print(f"    Avg Lead Time         : {m['avg_lead_time_hours']:.1f} hours")
        print(f"    Change Failure Rate   : {m['change_failure_rate']:.1f}%")
        print(f"    Mean Time to Recovery : {m['avg_mttr_hours']:.1f} hours")

    print("\n" + "-" * 62)
    print("  Insight: Payments deploys frequently with low failure rate.")
    print("  Inventory has longer lead times and higher failure rate —")
    print("  a candidate for golden-path adoption to improve flow.")
    print("=" * 62)
