"""
Chapter 6: Domain Defaults in Action

Loads domain_defaults.yaml and demonstrates how domain-aware defaults
eliminate manual configuration. Shows the contrast between what a
developer specifies (3 fields) and what the platform applies automatically
(20+ settings) based on domain context.

Run: python Chapter06/run_domain_defaults.py
Requires: pip install pyyaml
"""

import yaml
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULTS_PATH = os.path.join(SCRIPT_DIR, "domain_defaults.yaml")


def load_defaults(path):
    with open(path) as f:
        return yaml.safe_load(f)


# ── Simulated domain registry (other domains for contrast) ───────────

DOMAIN_REGISTRY = {
    "healthcare": {
        "infrastructure": {
            "compute": {"defaultSize": "large", "minReplicas": 3, "maxReplicas": 15},
            "database": {"engine": "postgresql", "version": "15",
                         "encryption": "aes-256-gcm", "backupRetention": "7y",
                         "multiAZ": True},
        },
        "security": {
            "authentication": {"method": "oauth2", "tokenExpiry": "30m"},
            "authorization": {"model": "abac", "defaultPolicy": "deny"},
            "compliance": {"frameworks": ["hipaa", "hitrust"],
                           "auditLogging": "required"},
        },
        "observability": {
            "logging": {"level": "info", "format": "json",
                        "retention": "7y", "piiMasking": "enabled"},
            "metrics": {"interval": "15s", "retention": "13mo"},
            "tracing": {"enabled": True, "samplingRate": 0.5},
        },
    },
    "marketing": {
        "infrastructure": {
            "compute": {"defaultSize": "small", "minReplicas": 1, "maxReplicas": 10},
            "database": {"engine": "postgresql", "version": "15",
                         "encryption": "tls-1.3", "backupRetention": "30d",
                         "multiAZ": False},
        },
        "security": {
            "authentication": {"method": "oauth2", "tokenExpiry": "8h"},
            "authorization": {"model": "rbac", "defaultPolicy": "allow"},
            "compliance": {"frameworks": ["standard"],
                           "auditLogging": "optional"},
        },
        "observability": {
            "logging": {"level": "warn", "format": "json",
                        "retention": "30d", "piiMasking": "disabled"},
            "metrics": {"interval": "60s", "retention": "3mo"},
            "tracing": {"enabled": True, "samplingRate": 0.01},
        },
    },
}


# ── Provisioning requests ────────────────────────────────────────────

REQUESTS = [
    {"developer": "Alice", "domain": "payments", "service": "fraud-detector", "tier": "production"},
    {"developer": "Bob", "domain": "healthcare", "service": "patient-portal", "tier": "production"},
    {"developer": "Carol", "domain": "marketing", "service": "campaign-tracker", "tier": "dev"},
]


def apply_defaults(request, payments_spec, registry):
    """Resolve the full configuration from a 3-field request."""
    domain = request["domain"]

    if domain == "payments":
        spec = payments_spec
    elif domain in registry:
        spec = registry[domain]
    else:
        spec = None

    if not spec:
        return None

    infra = spec["infrastructure"]
    sec = spec["security"]
    obs = spec["observability"]

    return {
        "service_id": f"svc-{domain[:3]}-{request['service']}-{request['tier'][:4]}",
        "service": request["service"],
        "domain": domain,
        "tier": request["tier"],
        "applied_defaults": {
            "compute": infra["compute"],
            "database": infra["database"],
            "auth": f"{sec['authentication']['method']} (token: {sec['authentication']['tokenExpiry']})",
            "authorization": f"{sec['authorization']['model']}, default={sec['authorization']['defaultPolicy']}",
            "compliance": sec["compliance"]["frameworks"],
            "audit_logging": sec["compliance"]["auditLogging"],
            "log_retention": obs["logging"]["retention"],
            "pii_masking": obs["logging"]["piiMasking"],
            "trace_sampling": obs["tracing"]["samplingRate"],
            "metric_interval": obs["metrics"]["interval"],
        },
    }


def count_settings(spec):
    """Count total configuration settings in a defaults spec."""
    count = 0
    for section in spec.values():
        if isinstance(section, dict):
            for subsection in section.values():
                if isinstance(subsection, dict):
                    count += len(subsection)
                else:
                    count += 1
    return count


def main():
    defaults = load_defaults(DEFAULTS_PATH)
    meta = defaults["metadata"]
    spec = defaults["spec"]

    print("=" * 64)
    print("DOMAIN DEFAULTS — CONFIGURATION BEFORE CODE")
    print("=" * 64)
    print(f"\n  Loaded: {os.path.basename(DEFAULTS_PATH)}")
    print(f"  Domain: {meta['domain']}  |  Version: {meta['version']}")

    # ── Show what's in the defaults file ──
    print(f"\n  Settings in payments defaults: {count_settings(spec)}")
    print(f"  Settings developer specifies:  3  (name, tier, purpose)")
    print(f"  Configuration ratio:           1:{count_settings(spec) // 3}")
    print(f"\n  The developer declares intent. The platform resolves configuration.\n")

    # ── Key defaults by category ──
    print("─" * 64)
    print("  PAYMENTS DOMAIN DEFAULTS (from YAML)")
    print("─" * 64)

    infra = spec["infrastructure"]
    sec = spec["security"]
    obs = spec["observability"]

    print(f"\n  Infrastructure")
    print(f"    Compute:    {infra['compute']['defaultSize']} ({infra['compute']['minReplicas']}-{infra['compute']['maxReplicas']} replicas)")
    print(f"    Database:   {infra['database']['engine']} {infra['database']['version']}")
    print(f"    Encryption: {infra['database']['encryption']}")
    print(f"    Backup:     {infra['database']['backupRetention']}  Multi-AZ: {infra['database']['multiAZ']}")

    print(f"\n  Security")
    print(f"    Auth:       {sec['authentication']['method']} (token: {sec['authentication']['tokenExpiry']})")
    print(f"    AuthZ:      {sec['authorization']['model']}, default={sec['authorization']['defaultPolicy']}")
    print(f"    Compliance: {', '.join(sec['compliance']['frameworks'])}")
    print(f"    Audit:      {sec['compliance']['auditLogging']}")

    print(f"\n  Observability")
    print(f"    Logging:    {obs['logging']['level']}/{obs['logging']['format']}, retain {obs['logging']['retention']}, PII masking {obs['logging']['piiMasking']}")
    print(f"    Metrics:    every {obs['metrics']['interval']}, retain {obs['metrics']['retention']}")
    print(f"    Tracing:    {obs['tracing']['samplingRate'] * 100:.0f}% sampling")

    # ── Process requests across domains ──
    print(f"\n{'=' * 64}")
    print("PROVISIONING WITH DOMAIN-AWARE DEFAULTS")
    print("=" * 64)

    for req in REQUESTS:
        result = apply_defaults(req, spec, DOMAIN_REGISTRY)
        if not result:
            continue

        ad = result["applied_defaults"]
        print(f"\n  {req['developer']} requests: \"{req['service']}\" in {req['domain']} ({req['tier']})")
        print(f"  ┌─ Developer provides: name, tier, purpose")
        print(f"  └─ Platform resolves {len(ad)} configuration groups automatically:")
        print(f"       Compute:    {ad['compute']['defaultSize']} ({ad['compute']['minReplicas']}-{ad['compute']['maxReplicas']} replicas)")
        print(f"       Database:   {ad['database']['engine']} {ad['database']['version']}, encryption={ad['database']['encryption']}")
        print(f"       Backup:     {ad['database']['backupRetention']}, multi-AZ={ad['database']['multiAZ']}")
        print(f"       Auth:       {ad['auth']}")
        print(f"       Compliance: {', '.join(ad['compliance'])}")
        print(f"       Audit log:  {ad['audit_logging']}")
        print(f"       Log retain: {ad['log_retention']}, PII masking: {ad['pii_masking']}")
        print(f"       Tracing:    {ad['trace_sampling'] * 100:.0f}% sampling")

    # ── Cross-domain comparison ──
    print(f"\n{'=' * 64}")
    print("CROSS-DOMAIN COMPARISON")
    print("=" * 64)
    print(f"\n  {'Setting':<24s} {'Payments':<18s} {'Healthcare':<18s} {'Marketing':<18s}")
    print(f"  {'─' * 24} {'─' * 18} {'─' * 18} {'─' * 18}")

    hc = DOMAIN_REGISTRY["healthcare"]
    mk = DOMAIN_REGISTRY["marketing"]

    comparisons = [
        ("Compute size", infra["compute"]["defaultSize"], hc["infrastructure"]["compute"]["defaultSize"], mk["infrastructure"]["compute"]["defaultSize"]),
        ("Encryption", infra["database"]["encryption"], hc["infrastructure"]["database"]["encryption"], mk["infrastructure"]["database"]["encryption"]),
        ("Backup retention", infra["database"]["backupRetention"], hc["infrastructure"]["database"]["backupRetention"], mk["infrastructure"]["database"]["backupRetention"]),
        ("Multi-AZ", str(infra["database"]["multiAZ"]), str(hc["infrastructure"]["database"]["multiAZ"]), str(mk["infrastructure"]["database"]["multiAZ"])),
        ("Compliance", ", ".join(sec["compliance"]["frameworks"]), ", ".join(hc["security"]["compliance"]["frameworks"]), ", ".join(mk["security"]["compliance"]["frameworks"])),
        ("Audit logging", sec["compliance"]["auditLogging"], hc["security"]["compliance"]["auditLogging"], mk["security"]["compliance"]["auditLogging"]),
        ("Token expiry", sec["authentication"]["tokenExpiry"], hc["security"]["authentication"]["tokenExpiry"], mk["security"]["authentication"]["tokenExpiry"]),
        ("Log retention", obs["logging"]["retention"], hc["observability"]["logging"]["retention"], mk["observability"]["logging"]["retention"]),
        ("PII masking", obs["logging"]["piiMasking"], hc["observability"]["logging"]["piiMasking"], mk["observability"]["logging"]["piiMasking"]),
        ("Trace sampling", f"{obs['tracing']['samplingRate'] * 100:.0f}%", f"{hc['observability']['tracing']['samplingRate'] * 100:.0f}%", f"{mk['observability']['tracing']['samplingRate'] * 100:.0f}%"),
    ]

    for label, pay, hcv, mkv in comparisons:
        print(f"  {label:<24s} {pay:<18s} {hcv:<18s} {mkv:<18s}")

    print(f"\n  Same platform. Same API. Different domains get different defaults.")
    print(f"  That's the value of domain awareness at the platform layer.")


if __name__ == "__main__":
    main()
