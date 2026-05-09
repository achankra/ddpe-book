"""Validate that IaC resources include mandatory ownership tags.

Small helper used by platform tooling or CI to ensure deployed resources
include mandatory tags such as Owner, Domain and Environment.
"""

from pathlib import Path
import json


# ============================================================================
# Configuration
# ============================================================================

MANDATORY_TAGS = ["Owner", "Domain", "Environment"]


# ============================================================================
# Validation Logic
# ============================================================================

def validate_mandatory_tags(iac_file_path: str) -> bool:
    """Return True when all mandatory tags are present in the IaC file.

    Args:
        iac_file_path: Path to a JSON file with a top-level
            'resource_definition' that contains a 'tags' mapping.

    Returns:
        True if all mandatory tags exist, False otherwise.
    """
    path = Path(iac_file_path)
    try:
        with open(path, "r") as f:
            config_data = json.load(f)

        resource_tags = (
            config_data
            .get("resource_definition", {})
            .get("tags", {})
        )

        missing_tags = [
            tag for tag in MANDATORY_TAGS
            if tag not in resource_tags
        ]

        if missing_tags:
            print("--- GOVERNANCE CHECK FAILED ---")
            print(f"Missing mandatory tags: {', '.join(missing_tags)}")
            return False

        print("--- GOVERNANCE CHECK PASSED ---")
        print("All mandatory tags present. Deployment authorized.")
        return True

    except FileNotFoundError:
        print(f"Error: Configuration file not found at {iac_file_path}")
        return False

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {iac_file_path}")
        return False


# ============================================================================
# Simulation
# ============================================================================

if __name__ == "__main__":

    # Example IaC file (used by a Stream-Aligned Team)
    example_config = {
        "resource_definition": {
            "type": "aws_dynamodb_table",
            "name": "PaymentsLedger",
            "tags": {
                "Owner": "PaymentsTeam",
                "Environment": "dev",
                "CostCenter": "P42"  # Optional, non-mandatory tag
            }
        }
    }

    # Write simulated IaC file
    sample_path = Path("payments_iac_config.json")
    with open(sample_path, "w") as f:
        json.dump(example_config, f, indent=2)

    # Run the platform governance check
    # This should FAIL because "Domain" tag is missing
    validate_mandatory_tags("payments_iac_config.json")

    print()

    # Now add the missing Domain tag and re-validate
    example_config["resource_definition"]["tags"]["Domain"] = "Payments"
    with open(sample_path, "w") as f:
        json.dump(example_config, f, indent=2)

    # This should PASS
    validate_mandatory_tags("payments_iac_config.json")

    # Clean up
    sample_path.unlink(missing_ok=True)
