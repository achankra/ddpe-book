"""Validate that IaC resources include mandatory ownership tags.

Small helper used by platform tooling or CI to ensure deployed resources
include mandatory tags such as Owner, Domain and Environment.
"""

from pathlib import Path
import json
from typing import List


MANDATORY_TAGS = ["Owner", "Domain", "Environment"]


def validate_mandatory_tags(iac_file_path: str | Path) -> bool:
    """Return True when all mandatory tags are present in the IaC file.

    Args:
        iac_file_path: Path to a JSON file with a top-level
            'resource_definition' that contains a 'tags' mapping.

    Returns:
        True if all mandatory tags exist, False otherwise.
    """

    path = Path(iac_file_path)
    try:
        if __name__ == "__main__":
            # Generate a small example file and run validation (safe for screenshots)
            sample = _example_config()
            sample_path = Path("payments_iac_config.json")
            sample_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")
            validate_mandatory_tags(sample_path)
                            "Domain": "Payments",
                            "Environment": "dev",
                            "CostCenter": "P42",  # optional
                        },
                    }
                }

# --- Simulation --- 
            if __name__ == "__main__":
                # Generate a small example file and run validation (safe for screenshots)
                sample = _example_config()
                sample_path = Path("payments_iac_config.json")
                sample_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")
                validate_mandatory_tags(sample_path)

# 1. Example IaC file (used by the Stream-Aligned Team) 

example_config = { 

    "resource_definition": { 

        "type": "aws_dynamodb_table", 

        "name": "PaymentsLedger", 

        "tags": { 

            "Owner": "PaymentsTeam", 

            "Environment": "dev", 

            "CostCenter": "P42" # Optional, non-mandatory tag 

        } 

    } 

} 

 

# Write simulated IaC file 

with open("payments_iac_config.json", 'w') as f: 

    json.dump(example_config, f) 

 

# Run the platform check 

validate_mandatory_tags("payments_iac_config.json") 
