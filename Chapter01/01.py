"""
IaC Mandatory Tag Validator

This script ensures that any resource deployed via Infrastructure as Code
(e.g., a DynamoDB table) includes mandatory, domain-specific tags.

Tags enforce consistency for cost tracking, ownership signals, and
governance compliance at the point of change.
"""

import json


# ============================================================================
# Configuration
# ============================================================================

MANDATORY_TAGS = ["Owner", "Domain", "Environment"]


# ============================================================================
# Validation Logic
# ============================================================================

def validate_mandatory_tags(iac_file_path):
    """
    Checks an IaC configuration file for mandatory tags.

    Args:
        iac_file_path: Path to the infrastructure configuration file
                       (JSON format, e.g., Terraform plan output)

    Returns:
        bool: True if all mandatory tags present, False otherwise
    """
    try:
        with open(iac_file_path, 'r') as f:
            config_data = json.load(f)

        resource_tags = (
            config_data
            .get('resource_definition', {})
            .get('tags', {})
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

        json.dump(example_config, f, indent=2)

    # Run the platform governance check
    validate_mandatory_tags("payments_iac_config.json")




