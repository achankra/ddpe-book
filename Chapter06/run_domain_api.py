"""
Chapter 6: Domain-Specific API Contract Demo

Loads domain-specific-api.yaml (the request/response contract) and
domain_defaults.yaml, then simulates the platform API:
  - Developer sends 3 fields
  - Platform resolves 15+ fields from domain context
  - Shows the generic-API equivalent for contrast

Run: python Chapter06/run_domain_api.py
Requires: pip install pyyaml
"""

import yaml
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
API_SPEC_PATH = os.path.join(SCRIPT_DIR, "domain-specific-api.yaml")
DEFAULTS_PATH = os.path.join(SCRIPT_DIR, "domain_defaults.yaml")


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


# ── Simulated API requests ───────────────────────────────────────────

DOMAIN_API_REQUESTS = [
    {"name": "transaction-ledger", "tier": "production", "purpose": "transaction-storage"},
    {"name": "session-cache", "tier": "staging", "purpose": "session-management"},
    {"name": "audit-archive", "tier": "production", "purpose": "compliance-audit"},
]

# What you'd have to specify with a generic cloud API
GENERIC_API_FIELDS = [
    "engine", "engine_version", "instance_class", "storage_type", "storage_size",
    "iops", "multi_az", "vpc_id", "subnet_ids", "security_group_ids",
    "parameter_group", "option_group", "encryption_key_arn", "backup_retention_period",
    "backup_window", "maintenance_window", "monitoring_interval", "monitoring_role_arn",
    "performance_insights", "deletion_protection", "auto_minor_version_upgrade",
    "copy_tags_to_snapshot", "storage_encrypted", "publicly_accessible",
    "iam_database_authentication", "cloudwatch_logs_exports", "tags",
]


def simulate_platform_response(request, defaults_spec):
    """Simulate the platform API response using domain defaults."""
    infra = defaults_spec["infrastructure"]
    sec = defaults_spec["security"]
    obs = defaults_spec["observability"]

    domain = "payments"
    short = request["name"].replace("-", "")[:8]

    return {
        "id": f"db-pay-{request['name']}-{request['tier'][:4]}",
        "name": request["name"],
        "status": "provisioning",
        "domain": domain,
        "connection": {
            "host": f"{request['name']}.{domain}.internal",
            "port": 5432,
            "secret_ref": f"vault:{domain}/db/{request['name']}",
        },
        "applied_defaults": {
            "engine": f"{infra['database']['engine']}-{infra['database']['version']}",
            "encryption": infra["database"]["encryption"],
            "backup_retention": infra["database"]["backupRetention"],
            "multi_az": infra["database"]["multiAZ"],
            "compliance": sec["compliance"]["frameworks"],
            "audit_logging": sec["compliance"]["auditLogging"],
            "auth_method": sec["authentication"]["method"],
            "pii_masking": obs["logging"]["piiMasking"],
            "log_retention": obs["logging"]["retention"],
            "trace_sampling": obs["tracing"]["samplingRate"],
            "compute_size": infra["compute"]["defaultSize"],
            "min_replicas": infra["compute"]["minReplicas"],
            "max_replicas": infra["compute"]["maxReplicas"],
        },
        "estimated_ready": "~15 minutes (production tier)",
    }


def main():
    defaults = load_yaml(DEFAULTS_PATH)
    spec = defaults["spec"]

    # Read the API spec file as raw text to show the contract
    with open(API_SPEC_PATH) as f:
        api_raw = f.read()

    print("=" * 64)
    print("DOMAIN-SPECIFIC API — 3 FIELDS IN, 15+ FIELDS OUT")
    print("=" * 64)

    # ── Show the API contract from the file ──
    print(f"\n  Source: {os.path.basename(API_SPEC_PATH)}")
    print(f"  Defaults: {os.path.basename(DEFAULTS_PATH)}")

    print(f"\n  GENERIC CLOUD API")
    print(f"  You would specify {len(GENERIC_API_FIELDS)} parameters:")
    for i in range(0, len(GENERIC_API_FIELDS), 4):
        chunk = GENERIC_API_FIELDS[i:i+4]
        print(f"    {', '.join(chunk)}")

    print(f"\n  DOMAIN-SPECIFIC API")
    print(f"  You specify 3 parameters: name, tier, purpose")
    print(f"  The platform resolves the other {len(GENERIC_API_FIELDS) - 3} from domain context.\n")

    # ── Process each request ──
    print("─" * 64)
    print("  SIMULATED API CALLS")
    print("─" * 64)

    for i, req in enumerate(DOMAIN_API_REQUESTS, 1):
        print(f"\n  Request {i}:")
        print(f"  POST /api/v1/payments/databases")
        print(f"  {json.dumps(req, indent=2).replace(chr(10), chr(10) + '  ')}")

        response = simulate_platform_response(req, spec)

        print(f"\n  Response:")
        print(f"  HTTP/1.1 201 Created")

        # Print response as formatted JSON
        resp_json = json.dumps(response, indent=4)
        for line in resp_json.split("\n"):
            print(f"  {line}")

        # Count auto-applied fields
        auto_count = len(response["applied_defaults"])
        print(f"\n  → {auto_count} settings applied automatically from domain context")

    # ── Summary ──
    print(f"\n{'=' * 64}")
    print("CONFIGURATION EFFORT COMPARISON")
    print("=" * 64)
    print(f"\n  {'Approach':<30s} {'Fields':<10s} {'Time':<15s} {'Error Risk'}")
    print(f"  {'─' * 30} {'─' * 10} {'─' * 15} {'─' * 12}")
    print(f"  {'Generic cloud API':<30s} {'27+':<10s} {'30-60 min':<15s} {'High'}")
    print(f"  {'Domain-specific API':<30s} {'3':<10s} {'< 1 min':<15s} {'Low'}")
    print(f"  {'Reduction':<30s} {'89%':<10s} {'97%':<15s} {'—'}")
    print(f"\n  Domain defaults eliminate configuration toil.")
    print(f"  Compliance is a property of the platform, not a developer task.")


if __name__ == "__main__":
    main()
