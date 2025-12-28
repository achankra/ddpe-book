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
