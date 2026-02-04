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
