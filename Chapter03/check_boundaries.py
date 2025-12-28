# check_boundaries.py
"""Detect bounded context violations - the 'chatter' that signals poor boundaries."""

from pathlib import Path

# Define what each context is allowed to import
BOUNDARIES = {
    'payments': ['shared'],           # payments cannot import inventory, shipping
    'inventory': ['shared'],          # inventory cannot import payments, shipping  
    'shipping': ['shared', 'inventory'],  # shipping can read inventory
}

def check_context(context_name: str) -> list[str]:
    """Return list of boundary violations for a context."""
    violations = []
    allowed = BOUNDARIES.get(context_name, [])
    
    for py_file in Path(f'src/domains/{context_name}').glob('**/*.py'):
        content = py_file.read_text()
        
        for other_context in BOUNDARIES.keys():
            if other_context != context_name and other_context not in allowed:
                if f'from domains.{other_context}' in content:
                    violations.append(f"{py_file.name} imports {other_context}")
    
    return violations

# Usage
for context in BOUNDARIES:
    issues = check_context(context)
    status = "✓ Clean" if not issues else f"❌ {len(issues)} violations"
    print(f"{context}: {status}")








    
