# genai_platform_interface.py
"""GenAI-Driven Platform Interface for Domain-Driven Platform Engineering.

Demonstrates a prompt-driven interface that interprets developer intent
and provisions domain-aware infrastructure using generative AI patterns.
This aligns with Chapter 10's vision of GenAI as an accelerator for
platform engineering—not replacing domain expertise, but augmenting
developer interaction with the platform.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import json


# ============================================================================
# Domain Context
# ============================================================================

class ComplianceFramework(Enum):
    PCI_DSS = "pci-dss-4.0"
    SOC2 = "soc2-type2"
    HIPAA = "hipaa"
    GDPR = "gdpr"


@dataclass
class DomainContext:
    """Captures the domain context that shapes infrastructure decisions."""
    domain: str
    data_classification: str
    compliance: List[ComplianceFramework] = field(default_factory=list)
    bounded_context: str = ""

    def requires_encryption_at_rest(self) -> bool:
        return self.data_classification in ["pii", "phi", "financial"]

    def requires_audit_logging(self) -> bool:
        return len(self.compliance) > 0


# ============================================================================
# Intent Parsing (simulates GenAI interpretation)
# ============================================================================

@dataclass
class ParsedIntent:
    """Structured output from interpreting a developer's natural language request."""
    action: str
    resource_type: str
    service_name: str
    domain: str
    tier: str = "development"
    purpose: str = ""
    confidence: float = 0.0


# Known domain mappings (in production, the GenAI model learns these)
DOMAIN_COMPLIANCE_MAP = {
    "payments": [ComplianceFramework.PCI_DSS, ComplianceFramework.SOC2],
    "healthcare": [ComplianceFramework.HIPAA],
    "customer-management": [ComplianceFramework.GDPR],
}

DOMAIN_DATA_CLASS_MAP = {
    "payments": "financial",
    "healthcare": "phi",
    "customer-management": "pii",
}


def parse_developer_intent(prompt: str) -> ParsedIntent:
    """Simulate GenAI parsing of a developer's natural-language request.

    In a real implementation, this would call an LLM with domain-specific
    context and few-shot examples. Here we use keyword matching to
    demonstrate the pattern.
    """
    prompt_lower = prompt.lower()

    # Determine action
    action = "provision"
    if any(w in prompt_lower for w in ["scale", "resize"]):
        action = "scale"
    elif any(w in prompt_lower for w in ["migrate", "move"]):
        action = "migrate"

    # Determine resource type
    resource_type = "service"
    if any(w in prompt_lower for w in ["database", "db", "store"]):
        resource_type = "database"
    elif any(w in prompt_lower for w in ["queue", "stream", "event"]):
        resource_type = "event-stream"
    elif any(w in prompt_lower for w in ["cache", "redis"]):
        resource_type = "cache"

    # Extract domain
    domain = "general"
    for d in DOMAIN_COMPLIANCE_MAP:
        if d.replace("-", " ") in prompt_lower or d in prompt_lower:
            domain = d
            break

    # Determine tier
    tier = "development"
    if "production" in prompt_lower or "prod" in prompt_lower:
        tier = "production"
    elif "staging" in prompt_lower:
        tier = "staging"

    # Extract a service name (simplified)
    service_name = f"{domain}-{resource_type}"

    return ParsedIntent(
        action=action,
        resource_type=resource_type,
        service_name=service_name,
        domain=domain,
        tier=tier,
        purpose=resource_type,
        confidence=0.87,
    )


# ============================================================================
# Platform Provisioning with Domain Defaults
# ============================================================================

def apply_domain_defaults(intent: ParsedIntent) -> Dict:
    """Apply opinionated, domain-aware defaults based on parsed intent.

    This is the core DDPE pattern: the platform knows what each domain
    needs and fills in the infrastructure details automatically.
    """
    context = DomainContext(
        domain=intent.domain,
        data_classification=DOMAIN_DATA_CLASS_MAP.get(intent.domain, "internal"),
        compliance=DOMAIN_COMPLIANCE_MAP.get(intent.domain, []),
        bounded_context=intent.domain,
    )

    provisioning_spec = {
        "action": intent.action,
        "resource": intent.resource_type,
        "name": intent.service_name,
        "tier": intent.tier,
        "domain_context": {
            "domain": context.domain,
            "data_classification": context.data_classification,
            "compliance": [c.value for c in context.compliance],
        },
        "applied_defaults": {
            "encryption_at_rest": context.requires_encryption_at_rest(),
            "audit_logging": context.requires_audit_logging(),
            "observability": {
                "metrics": True,
                "tracing": True,
                "log_level": "info",
            },
        },
    }

    # Add resource-specific defaults
    if intent.resource_type == "database":
        provisioning_spec["applied_defaults"].update({
            "engine": "postgresql-15",
            "backup_retention": "90d" if intent.tier == "production" else "7d",
            "multi_az": intent.tier == "production",
        })
    elif intent.resource_type == "event-stream":
        provisioning_spec["applied_defaults"].update({
            "engine": "kafka",
            "retention": "7d",
            "partitions": 6 if intent.tier == "production" else 1,
        })

    return provisioning_spec


# ============================================================================
# Simulation
# ============================================================================

if __name__ == "__main__":
    # Simulate a developer using a prompt-driven platform interface
    prompts = [
        "I need a production database for the payments domain",
        "Set up an event stream for customer-management",
        "Provision a cache for the healthcare staging environment",
    ]

    for prompt in prompts:
        print(f"\n{'='*60}")
        print(f"Developer prompt: \"{prompt}\"")
        print(f"{'='*60}")

        intent = parse_developer_intent(prompt)
        print(f"\nParsed intent (confidence: {intent.confidence:.0%}):")
        print(f"  Action: {intent.action}")
        print(f"  Resource: {intent.resource_type}")
        print(f"  Domain: {intent.domain}")
        print(f"  Tier: {intent.tier}")

        spec = apply_domain_defaults(intent)
        print(f"\nProvisioning spec with domain defaults:")
        print(json.dumps(spec, indent=2))
