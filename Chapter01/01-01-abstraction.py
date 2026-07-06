"""
Python Microservice Scaffolding Tool

This helper abstracts away the complexity of creating a new service project,
including templates, CI/CD pipelines, observability defaults, and compliance
policies—all pre-configured by the Platform Team.

Features:
    - Golden path templates with best practices baked in
    - Domain-specific configuration injection
    - Observability (logging, metrics) enabled by default
    - Infrastructure as Code (IaC) ready
    - CI/CD pipeline pre-configured for first commit
"""

import os
import shutil


# ============================================================================
# Configuration
# ============================================================================

TEMPLATE_BASE_PATH = "platform_templates"
TEMPLATE_NAME = "python_api_starter_kit"

DEFAULT_CONFIG = {
    "DEFAULT_LOGGING_LEVEL": "INFO",
}


# ============================================================================
# Service Creation
# ============================================================================

def create_python_microservice(service_name: str, domain: str) -> None:
    """
    Create a Python microservice project using the platform template.

    Copies the standard platform template into a new project folder,
    appends domain-specific settings into config.yaml, and prints
    next steps for the developer.

    Args:
        service_name: Name of the new service (becomes directory name)
        domain:       Business domain this service belongs to
    """
    print(f"-> Initializing new service: {service_name}")
    print(f"   Domain: {domain}")

    template_path = os.path.join(TEMPLATE_BASE_PATH, TEMPLATE_NAME)
    target_path = os.path.join(os.getcwd(), service_name)

    try:
        # Copy the golden template (self-service enablement)
        shutil.copytree(template_path, target_path)

        # Inject domain-specific configuration
        _write_domain_config(target_path, domain)

        # Guide the developer on next steps
        _print_success_message(target_path)

    except FileExistsError:
        print(f"Error: Directory '{service_name}' already exists.")


def _write_domain_config(target_path: str, domain: str) -> None:
    """Append domain-specific values to the project config file."""
    config_path = os.path.join(target_path, "config.yaml")

    with open(config_path, "a") as f:
        f.write(f"\n# Domain Configuration\n")
        f.write(f"DOMAIN: {domain}\n")

        for key, value in DEFAULT_CONFIG.items():
            f.write(f"{key}: {value}\n")


def _print_success_message(target_path: str) -> None:
    """Display next steps after successful project creation."""
    print(f"\n-> Successfully created project at: {target_path}")
    print("\nNext steps:")
    print("   1. cd into the project directory")
    print("   2. Run 'git init' to initialize version control")
    print("   3. Start adding your business logic")
    print("\n   CI/CD pipeline is pre-configured and ready for first commit!")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 62)
    print("  Microservice Scaffolding Tool — Abstraction Demo")
    print("=" * 62)

    print("\n  This tool abstracts away project setup complexity:")
    print("    - Golden-path templates with best practices baked in")
    print("    - Domain-specific configuration injection")
    print("    - Observability (logging, metrics) enabled by default")
    print("    - CI/CD pipeline pre-configured for first commit")

    print("\n  Simulating: create_python_microservice('payment-status-api', 'Payments')")
    print()
    print("  -> Initializing new service: payment-status-api")
    print("     Domain: Payments")
    print()

    steps = [
        ("Copy golden template", f"platform_templates/{TEMPLATE_NAME} -> ./payment-status-api/"),
        ("Inject domain config", "config.yaml <- DOMAIN: Payments, DEFAULT_LOGGING_LEVEL: INFO"),
        ("Pre-configure CI/CD", "Pipeline ready for first commit"),
    ]
    for i, (step, detail) in enumerate(steps, 1):
        print(f"  [{i}/{len(steps)}] {step}")
        print(f"        {detail}")

    print()
    _print_success_message("./payment-status-api")

    print("\n  Key DDPE Insight:")
    print("    Developers focus on business logic, not boilerplate.")
    print("    The platform team maintains the templates centrally.")
    print("=" * 62)
