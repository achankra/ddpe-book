# onboarding_flow.py
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class ServiceType(Enum):
    API = "api"
    WORKER = "worker"
    SCHEDULED = "scheduled"
    EVENT_DRIVEN = "event-driven"

@dataclass
class OnboardingContext:
    team_name: str
    domain: str
    service_name: str
    service_type: ServiceType
    language: str
    compliance_requirements: List[str]
    data_classification: str

class OnboardingFlow:
    def __init__(self, context: OnboardingContext):
        self.context = context
        self.steps = []

    def initialize(self) -> "OnboardingFlow":
        """Validate context and prepare resources."""
        self._validate_team_permissions()
        self._validate_domain_exists()
        self._reserve_service_name()
        return self

    def scaffold(self) -> "OnboardingFlow":
        """Generate project structure from templates."""
        template = self._select_template()
        self._generate_code_structure(template)
        self._generate_infrastructure(template)
        self._generate_pipeline(template)
        return self

    def configure(self) -> "OnboardingFlow":
        """Apply domain and environment configuration."""
        self._apply_compliance_controls()
        self._configure_networking()
        self._setup_secrets()
        return self

    def deploy(self, environment: str = "dev") -> "OnboardingFlow":
        """Provision service to target environment."""
        self._provision_infrastructure(environment)
        self._deploy_service(environment)
        self._verify_deployment(environment)
        return self
        
    def observe(self) -> "OnboardingFlow":
        """Establish monitoring and alerting."""
        self._create_dashboards()
        self._configure_alerts()
        self._register_in_catalog()
        return self

    # --- Simulation helpers for demo (not part of production code) ---
    def _validate_team_permissions(self): pass
    def _validate_domain_exists(self): pass
    def _reserve_service_name(self): pass
    def _select_template(self): return f"{self.context.language}-{self.context.service_type.value}"
    def _generate_code_structure(self, t): pass
    def _generate_infrastructure(self, t): pass
    def _generate_pipeline(self, t): pass
    def _apply_compliance_controls(self): pass
    def _configure_networking(self): pass
    def _setup_secrets(self): pass
    def _provision_infrastructure(self, env): pass
    def _deploy_service(self, env): pass
    def _verify_deployment(self, env): pass
    def _create_dashboards(self): pass
    def _configure_alerts(self): pass
    def _register_in_catalog(self): pass


if __name__ == "__main__":
    print("=" * 62)
    print("  Developer Onboarding Flow — Full Lifecycle Demo")
    print("=" * 62)

    ctx = OnboardingContext(
        team_name="Payments Team",
        domain="payments",
        service_name="payment-gateway",
        service_type=ServiceType.API,
        language="python",
        compliance_requirements=["PCI-DSS", "SOC2"],
        data_classification="confidential",
    )

    print(f"\n  Team    : {ctx.team_name}")
    print(f"  Service : {ctx.service_name} ({ctx.service_type.value})")
    print(f"  Domain  : {ctx.domain}")
    print(f"  Language : {ctx.language}")
    print(f"  Compliance: {', '.join(ctx.compliance_requirements)}")
    print(f"  Data class: {ctx.data_classification}")

    flow = OnboardingFlow(ctx)

    stages = [
        ("initialize", "Validate permissions, domain, and reserve name",
         lambda: flow.initialize()),
        ("scaffold", "Generate code, infrastructure, and pipeline from templates",
         lambda: flow.scaffold()),
        ("configure", "Apply compliance controls, networking, and secrets",
         lambda: flow.configure()),
        ("deploy", "Provision infrastructure and deploy to dev environment",
         lambda: flow.deploy("dev")),
        ("observe", "Create dashboards, alerts, and register in catalog",
         lambda: flow.observe()),
    ]

    print(f"\n  Running {len(stages)}-stage onboarding flow:")
    for i, (name, desc, action) in enumerate(stages, 1):
        action()
        print(f"    [{i}/{len(stages)}] {name:12s} -> {desc}")

    print(f"\n  Onboarding complete. '{ctx.service_name}' is live in dev.")
    print("=" * 62)
