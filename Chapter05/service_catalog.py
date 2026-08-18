"""
Chapter 5: Platform as a Product — Service Catalog in Action

Loads service_definition.yaml and demonstrates how a domain-driven platform
uses service offerings as a product catalog:
  1. Parses the YAML and validates completeness
  2. Simulates provisioning requests from domain teams
  3. Enforces domain-aware SLA contracts
  4. Tracks interaction mode usage across channels
  5. Checks version evolution policy compliance

Run: python Chapter05/service_catalog.py
Requires: pip install pyyaml
"""

import yaml
import os
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
YAML_PATH = os.path.join(SCRIPT_DIR, "service_definition.yaml")

# ── 1. Load and validate the service definition ──────────────────────────

def load_service_definition(path):
    with open(path) as f:
        return yaml.safe_load(f)

def validate_offering(defn):
    """Check that a service offering has all required fields for a platform product."""
    required = {
        "metadata.name": defn.get("metadata", {}).get("name"),
        "metadata.version": defn.get("metadata", {}).get("version"),
        "metadata.domain": defn.get("metadata", {}).get("domain"),
        "spec.description": defn.get("spec", {}).get("description"),
        "spec.sla": defn.get("spec", {}).get("sla"),
        "spec.selfService": defn.get("spec", {}).get("selfService"),
        "spec.evolution": defn.get("spec", {}).get("evolution"),
    }
    results = []
    for field, value in required.items():
        status = "PASS" if value else "MISSING"
        results.append((field, status, value))
    return results


# ── 2. Domain-aware provisioning requests ────────────────────────────────

PROVISIONING_REQUESTS = [
    {
        "team": "Payments",
        "domain": "bfsi-payments",
        "engine": "postgresql",
        "version": "16",
        "tier": "production",
        "channel": "api",
        "compliance": ["PCI-DSS"],
    },
    {
        "team": "Inventory",
        "domain": "retail-inventory",
        "engine": "postgresql",
        "version": "15",
        "tier": "staging",
        "channel": "cli",
        "compliance": [],
    },
    {
        "team": "Patient Records",
        "domain": "healthcare-records",
        "engine": "postgresql",
        "version": "14",
        "tier": "production",
        "channel": "portal",
        "compliance": ["HIPAA"],
    },
    {
        "team": "Marketing",
        "domain": "marketing-content",
        "engine": "postgresql",
        "version": "15",
        "tier": "dev",
        "channel": "terraform",
        "compliance": [],
    },
    {
        "team": "Risk Analytics",
        "domain": "bfsi-risk",
        "engine": "postgresql",
        "version": "16",
        "tier": "production",
        "channel": "api",
        "compliance": ["SOX"],
    },
]


def process_request(request, offering):
    """Validate a provisioning request against the service offering."""
    spec = offering["spec"]
    supported = spec.get("supportedDatabases", [])
    sla = spec.get("sla", {}).get("provisioning", {})
    channels = spec.get("selfService", {})
    issues = []

    # Check engine support
    engine_match = None
    for db in supported:
        if db["engine"] == request["engine"]:
            engine_match = db
            break
    if not engine_match:
        issues.append(f"Engine '{request['engine']}' not supported")
    else:
        if request["version"] not in engine_match["versions"]:
            issues.append(f"Version {request['version']} not in supported list {engine_match['versions']}")
        if request["tier"] not in engine_match["tiers"]:
            issues.append(f"Tier '{request['tier']}' not available")

    # Check channel availability
    if not channels.get(request["channel"], False):
        issues.append(f"Channel '{request['channel']}' not enabled")

    # Get SLA target
    sla_target = sla.get(request["tier"], "N/A")

    return {
        "team": request["team"],
        "domain": request["domain"],
        "tier": request["tier"],
        "channel": request["channel"],
        "sla_target": sla_target,
        "compliance": request["compliance"],
        "status": "APPROVED" if not issues else "REJECTED",
        "issues": issues,
    }


# ── 3. Interaction mode analysis ─────────────────────────────────────────

INTERACTION_LOG = [
    {"channel": "api", "count": 142, "avg_time_sec": 8},
    {"channel": "cli", "count": 87, "avg_time_sec": 12},
    {"channel": "portal", "count": 56, "avg_time_sec": 45},
    {"channel": "terraform", "count": 34, "avg_time_sec": 3},
]


def analyze_interactions(log):
    """Assess interaction mode maturity — X-as-a-Service readiness."""
    total = sum(e["count"] for e in log)
    results = []
    for entry in log:
        pct = entry["count"] / total * 100
        mode = "X-as-a-Service" if entry["avg_time_sec"] < 15 else "Collaboration"
        results.append({
            "channel": entry["channel"],
            "requests": entry["count"],
            "pct": pct,
            "avg_time": entry["avg_time_sec"],
            "mode": mode,
        })
    api_pct = sum(e["count"] for e in log if e["avg_time_sec"] < 15) / total * 100
    return results, api_pct


# ── 4. Version evolution policy ──────────────────────────────────────────

VERSION_HISTORY = [
    {"version": "v1.0.0", "released": "2024-06-01", "status": "deprecated", "deprecation_date": "2025-01-15"},
    {"version": "v1.5.0", "released": "2025-01-01", "status": "supported", "deprecation_date": None},
    {"version": "v2.0.0", "released": "2025-07-01", "status": "current", "deprecation_date": None},
]


def check_evolution_policy(history, policy):
    """Validate version transitions against the evolution policy."""
    dep_notice_days = int(policy.get("deprecationNotice", "90d").replace("d", ""))
    max_supported = policy.get("supportedVersions", 2)
    results = []

    active_versions = [v for v in history if v["status"] in ("current", "supported")]
    deprecated = [v for v in history if v["status"] == "deprecated"]

    # Check supported version count
    version_count_ok = len(active_versions) <= max_supported
    results.append({
        "check": f"Active versions <= {max_supported}",
        "value": f"{len(active_versions)} active",
        "status": "PASS" if version_count_ok else "VIOLATION",
    })

    # Check deprecation notice period
    for v in deprecated:
        if v["deprecation_date"]:
            released = datetime.strptime(v["released"], "%Y-%m-%d")
            deprecated_on = datetime.strptime(v["deprecation_date"], "%Y-%m-%d")
            notice_given = (deprecated_on - released).days
            ok = notice_given >= dep_notice_days
            results.append({
                "check": f"{v['version']} deprecation notice >= {dep_notice_days}d",
                "value": f"{notice_given} days given",
                "status": "PASS" if ok else "VIOLATION",
            })

    return results


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    offering = load_service_definition(YAML_PATH)

    # ── Section 1: Validate ──
    print("=" * 60)
    print("SERVICE OFFERING VALIDATION")
    print(f"Loading: {os.path.basename(YAML_PATH)}")
    print("=" * 60)

    checks = validate_offering(offering)
    all_pass = True
    for field, status, value in checks:
        icon = "✅" if status == "PASS" else "❌"
        display = str(value)[:50] if value else "(empty)"
        print(f"  {icon} {field:30s} {display}")
        if status != "PASS":
            all_pass = False

    name = offering["metadata"]["name"]
    version = offering["metadata"]["version"]
    domain = offering["metadata"]["domain"]
    print(f"\n  Offering: {name} {version} ({domain})")
    print(f"  Result:   {'Complete — ready for catalog' if all_pass else 'Incomplete — fix missing fields'}")

    # ── Section 2: Process requests ──
    print("\n" + "=" * 60)
    print("PROVISIONING REQUESTS (domain-aware)")
    print("=" * 60)

    for req in PROVISIONING_REQUESTS:
        result = process_request(req, offering)
        icon = "✅" if result["status"] == "APPROVED" else "❌"
        compliance = ", ".join(result["compliance"]) if result["compliance"] else "none"
        print(f"\n  {icon} {result['team']} ({result['domain']})")
        print(f"    Tier: {result['tier']}  |  Channel: {result['channel']}  |  SLA: {result['sla_target']}")
        print(f"    Compliance: {compliance}  |  Status: {result['status']}")
        if result["issues"]:
            for issue in result["issues"]:
                print(f"    ⚠  {issue}")

    approved = sum(1 for r in PROVISIONING_REQUESTS if process_request(r, offering)["status"] == "APPROVED")
    print(f"\n  Summary: {approved}/{len(PROVISIONING_REQUESTS)} approved")

    # ── Section 3: Interaction modes ──
    print("\n" + "=" * 60)
    print("INTERACTION MODE ANALYSIS")
    print("=" * 60)

    modes, api_pct = analyze_interactions(INTERACTION_LOG)
    for m in modes:
        bar = "█" * int(m["pct"] / 2)
        print(f"  {m['channel']:12s} {bar:25s} {m['requests']:4d} ({m['pct']:4.1f}%)  avg {m['avg_time']:2d}s  [{m['mode']}]")

    print(f"\n  Self-service rate: {api_pct:.0f}% of requests complete in <15 seconds")
    if api_pct >= 75:
        print("  Assessment: X-as-a-Service maturity achieved")
    else:
        print(f"  Assessment: {100 - api_pct:.0f}% of requests still require collaboration mode")
        print("  Action: Improve portal UX to reduce avg completion time below 15s")

    # ── Section 4: Evolution policy ──
    print("\n" + "=" * 60)
    print("VERSION EVOLUTION POLICY")
    print("=" * 60)

    policy = offering["spec"]["evolution"]
    print(f"  Deprecation notice: {policy.get('deprecationNotice', 'N/A')}")
    print(f"  Max supported versions: {policy.get('supportedVersions', 'N/A')}")
    print()

    for v in VERSION_HISTORY:
        icon = {"current": "●", "supported": "○", "deprecated": "✗"}
        status_icon = icon.get(v["status"], "?")
        dep = f"  (deprecated {v['deprecation_date']})" if v["deprecation_date"] else ""
        print(f"  {status_icon} {v['version']:10s} released {v['released']}  [{v['status']}]{dep}")

    print()
    checks = check_evolution_policy(VERSION_HISTORY, policy)
    for c in checks:
        icon = "✅" if c["status"] == "PASS" else "❌"
        print(f"  {icon} {c['check']:45s} {c['value']}")

    print("\n" + "=" * 60)
    print("PLATFORM AS A PRODUCT — KEY TAKEAWAYS")
    print("=" * 60)
    print("  1. Service definitions make platform capabilities discoverable")
    print("  2. SLA contracts set expectations per environment tier")
    print("  3. Multiple self-service channels reduce cognitive load")
    print("  4. Evolution policies protect consumer trust")
    print("  5. Interaction mode analysis measures X-as-a-Service maturity")


if __name__ == "__main__":
    main()
