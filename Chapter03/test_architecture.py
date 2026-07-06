# test_architecture.py
"""Fitness Function: Ensure services never import datastores directly."""

import ast
from pathlib import Path

FORBIDDEN_IN_SERVICES = ['sqlalchemy', 'pymongo', 'boto3', 'psycopg2']

def test_service_layer_isolation():
    """Services must import repositories, never datastores."""
    
    for service_file in Path('src/services').glob('*.py'):
        source = service_file.read_text()
        
        for forbidden in FORBIDDEN_IN_SERVICES:
            assert forbidden not in source, \
                f"VIOLATION: {service_file.name} imports '{forbidden}' directly"

# Run: pytest test_architecture.py

if __name__ == "__main__":
    print("=" * 62)
    print("  Architectural Fitness Function — Layer Isolation Check")
    print("=" * 62)

    # Simulate service files with known contents
    simulated_files = {
        "payment_service.py": "from repositories import PaymentRepo\nclass PaymentService: ...",
        "order_service.py": "from repositories import OrderRepo\nclass OrderService: ...",
        "report_service.py": "import psycopg2\nconn = psycopg2.connect(...)",
        "user_service.py": "import boto3\ns3 = boto3.client('s3')",
        "notify_service.py": "from repositories import NotifyRepo\nclass NotifyService: ...",
    }

    print(f"\n  Forbidden imports in service layer: {FORBIDDEN_IN_SERVICES}")
    print(f"  Scanning {len(simulated_files)} service files...\n")

    violations = []
    for filename, source in simulated_files.items():
        file_violations = [f for f in FORBIDDEN_IN_SERVICES if f in source]
        if file_violations:
            for v in file_violations:
                print(f"  FAIL  {filename} imports '{v}' directly")
                violations.append((filename, v))
        else:
            print(f"  PASS  {filename}")

    print(f"\n  Results: {len(simulated_files) - len(violations)} passed, "
          f"{len(violations)} violations found")
    if violations:
        print("  Action: Move datastore access behind repository abstractions.")
    else:
        print("  All services properly isolated from datastores.")
    print("=" * 62)
