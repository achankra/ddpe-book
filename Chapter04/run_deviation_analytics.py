# run_deviation_analytics.py
# Python wrapper for deviation_analytics.sql
# Creates an in-memory SQLite database with sample deviation data,
# then runs the SQL query from the book to analyze golden-path deviations.

import sqlite3
from datetime import datetime, timedelta
import random

def create_schema(conn):
    """Create the deviations table."""
    conn.execute("""
        CREATE TABLE deviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deviation_type TEXT NOT NULL,
            domain TEXT NOT NULL,
            team_name TEXT NOT NULL,
            service_name TEXT NOT NULL,
            requested_by TEXT NOT NULL,
            approved BOOLEAN NOT NULL,
            requested_at DATE NOT NULL,
            justification TEXT
        )
    """)

def seed_data(conn):
    """Populate with sample deviation data across BFSI, Healthcare,
    and Retail domains over the past 90 days."""
    now = datetime.now()
    deviations = [
        # BFSI — Payments domain: frequent custom DB requests (high approval)
        ("custom_database_engine", "BFSI-Payments", "settlements", "settle-svc", "alice", True),
        ("custom_database_engine", "BFSI-Payments", "reconciliation", "recon-svc", "bob", True),
        ("custom_database_engine", "BFSI-Payments", "fraud-detection", "fraud-svc", "carol", True),
        ("custom_database_engine", "BFSI-Payments", "settlements", "settle-svc", "alice", True),
        ("custom_database_engine", "BFSI-Payments", "ledger", "ledger-svc", "dave", True),
        ("custom_database_engine", "BFSI-Payments", "fraud-detection", "fraud-svc", "carol", False),

        # BFSI — Payments: elevated permissions for PCI audit
        ("elevated_permissions", "BFSI-Payments", "settlements", "settle-svc", "alice", True),
        ("elevated_permissions", "BFSI-Payments", "reconciliation", "recon-svc", "bob", True),
        ("elevated_permissions", "BFSI-Payments", "ledger", "ledger-svc", "dave", True),
        ("elevated_permissions", "BFSI-Payments", "fraud-detection", "fraud-svc", "carol", True),

        # BFSI — Payments: blocked deviations attempted
        ("non_standard_runtime", "BFSI-Payments", "settlements", "settle-svc", "alice", False),
        ("non_standard_runtime", "BFSI-Payments", "fraud-detection", "fraud-svc", "carol", False),

        # Healthcare: custom health check paths (high approval, many teams)
        ("custom_health_check_paths", "Healthcare", "clinical-data", "patient-svc", "emma", True),
        ("custom_health_check_paths", "Healthcare", "pharmacy", "rx-svc", "frank", True),
        ("custom_health_check_paths", "Healthcare", "lab-results", "lab-svc", "grace", True),
        ("custom_health_check_paths", "Healthcare", "imaging", "dicom-svc", "hank", True),
        ("custom_health_check_paths", "Healthcare", "clinical-data", "consent-svc", "emma", True),

        # Healthcare: external service integration (mixed approval)
        ("external_service_integration", "Healthcare", "clinical-data", "ehr-bridge", "emma", True),
        ("external_service_integration", "Healthcare", "pharmacy", "drug-db-svc", "frank", True),
        ("external_service_integration", "Healthcare", "lab-results", "lab-svc", "grace", False),
        ("external_service_integration", "Healthcare", "imaging", "pacs-svc", "hank", False),

        # Healthcare: non-standard ports for legacy HL7 interfaces
        ("non_standard_ports", "Healthcare", "clinical-data", "hl7-bridge", "emma", True),
        ("non_standard_ports", "Healthcare", "lab-results", "lis-bridge", "grace", True),
        ("non_standard_ports", "Healthcare", "pharmacy", "rx-bridge", "frank", True),

        # Retail: custom resource limits (high approval)
        ("custom_resource_limits", "Retail", "catalog", "search-svc", "iris", True),
        ("custom_resource_limits", "Retail", "checkout", "cart-svc", "jack", True),
        ("custom_resource_limits", "Retail", "recommendations", "rec-svc", "kate", True),
        ("custom_resource_limits", "Retail", "catalog", "image-svc", "iris", True),

        # Retail: non-standard runtime (low approval)
        ("non_standard_runtime", "Retail", "catalog", "search-svc", "iris", False),
        ("non_standard_runtime", "Retail", "checkout", "cart-svc", "jack", False),
        ("non_standard_runtime", "Retail", "recommendations", "rec-svc", "kate", False),
        ("non_standard_runtime", "Retail", "catalog", "search-svc", "iris", True),
    ]

    for i, (dev_type, domain, team, svc, user, approved) in enumerate(deviations):
        days_ago = random.randint(1, 89)
        requested_at = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        conn.execute(
            """INSERT INTO deviations
               (deviation_type, domain, team_name, service_name, requested_by, approved, requested_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (dev_type, domain, team, svc, user, approved, requested_at)
        )
    conn.commit()

def run_analytics(conn):
    """Run the deviation_analytics.sql query from the book."""
    query = """
    WITH deviation_summary AS (
      SELECT
        deviation_type,
        domain,
        COUNT(*) as deviation_count,
        COUNT(DISTINCT team_name) as affected_teams,
        AVG(CASE WHEN approved THEN 1 ELSE 0 END) as approval_rate
      FROM deviations
      WHERE requested_at >= date('now', '-90 days')
      GROUP BY deviation_type, domain
    )
    SELECT
      deviation_type,
      domain,
      deviation_count,
      affected_teams,
      ROUND(approval_rate * 100, 1) as approval_pct,
      CASE
        WHEN affected_teams >= 3 AND approval_rate > 0.8
        THEN 'Consider adding to golden path'
        WHEN approval_rate < 0.2
        THEN 'Review deviation category'
        ELSE 'Monitor'
      END as recommendation
    FROM deviation_summary
    ORDER BY deviation_count DESC
    """
    return conn.execute(query).fetchall()


if __name__ == "__main__":
    print("=" * 90)
    print("  Golden Path Deviation Analytics (Chapter 4)")
    print("  Analyzes 90-day deviation patterns to evolve golden paths")
    print("=" * 90)

    random.seed(42)
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    seed_data(conn)
    results = run_analytics(conn)

    print(f"\n  {'Deviation Type':<32} {'Domain':<18} {'Count':>5} {'Teams':>5} "
          f"{'Appr%':>6}  Recommendation")
    print("  " + "-" * 86)

    for row in results:
        dev_type, domain, count, teams, approval_pct, recommendation = row
        print(f"  {dev_type:<32} {domain:<18} {count:>5} {teams:>5} "
              f"{approval_pct:>5.1f}%  {recommendation}")

    print("\n" + "-" * 90)
    print("  How to read this:")
    print("    'Consider adding to golden path' = 3+ teams request it, >80% approved.")
    print("      This deviation is a missing platform capability, not an exception.")
    print("    'Review deviation category' = <20% approved. Likely a blocked pattern")
    print("      that teams keep attempting. Improve docs or guardrails.")
    print("    'Monitor' = Mixed signal. Watch for trends before acting.")
    print("=" * 90)

    conn.close()
