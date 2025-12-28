# This function abstracts away the complexity of setting up logging, metrics, infrastructure configuration (IaC), and compliance policies.

import os
import shutil

def create_python_microservice(service_name, domain):
    """
    Creates a new Python microservice from the standard golden template.
    This template includes default CI/CD, Observability hooks, and compliance config.
    """
    print(f"-> Initializing new service: {service_name} in domain: {domain}")

    # 1. Logic to select the pre-configured Python template (owned by Platform Team)
    template_path = os.path.join("platform_templates", "python_api_starter_kit")
    target_path = os.path.join(os.getcwd(), service_name)

    # 2. Copy and configure the template (Enablement)
    try:
        shutil.copytree(template_path, target_path)
        
        # Inject domain-specific configuration values (reducing cognitive load)
        with open(os.path.join(target_path, 'config.yaml'), 'a') as f:
            f.write(f"\nDOMAIN: {domain}\n")
            f.write("DEFAULT_LOGGING_LEVEL: INFO\n") # Observability by default [13, 14]

        print(f"-> Successfully created project structure at: {target_path}")
        print("-> Run 'git init' and start adding business logic!")

        # 3. The newly created service includes the full path-to-production pipeline
        print("-> CI/CD pipeline (GitHub Actions/CircleCI config) included and ready for first commit.")

    except FileExistsError:
        print(f"Error: Directory {service_name} already exists.")

# Developer's action (Self-Service)
create_python_microservice("payment_status_api", "Payments")
