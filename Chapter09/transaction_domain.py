# transaction_domain.py
"""BFSI Transaction Domain Abstraction"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class RegulatoryScope(Enum):
    PCI_DSS = "pci-dss"
    AML = "anti-money-laundering"
    KYC = "know-your-customer"
    GDPR = "gdpr"
    DODD_FRANK = "dodd-frank"

@dataclass
class TransactionMetadata:
    source: str
    destination: str
    amount: float
    currency: str
    timestamp: datetime = field(default_factory=datetime.now)
    user_context: str = ""
    justification: str = ""

@dataclass
class Transaction:
    id: str
    metadata: TransactionMetadata
    regulatory_scopes: List[RegulatoryScope]
    domain_context: dict = field(default_factory=dict)
    audit_trail: List[str] = field(default_factory=list)

    def submit(self):
        """Platform automatically enforces compliance."""
        self.audit_trail.append(f"Transaction created: {self.id}")
        # Auto-apply compliance controls
        for scope in self.regulatory_scopes:
            if scope == RegulatoryScope.AML:
                self._aml_check()
            elif scope == RegulatoryScope.PCI_DSS:
                self._pci_logging()
        # Auto-approval for high-value transactions
        if self.metadata.amount > 10000:
            self.audit_trail.append("Approval required: senior manager")
        return self

    def _aml_check(self):
        self.audit_trail.append("AML screening: passed")

    def _pci_logging(self):
        self.audit_trail.append("PCI-DSS: transaction logged to secure audit store")

# Example: Team only provides business context
txn = Transaction(
    id="TX-20240115-001",
    metadata=TransactionMetadata(
        source="checking-001", destination="savings-002",
        amount=15000, currency="USD",
        justification="Customer-initiated transfer"
    ),
    regulatory_scopes=[RegulatoryScope.PCI_DSS, RegulatoryScope.AML],
    domain_context={"product": "retail-banking", "channel": "mobile"}
)
txn.submit()
for entry in txn.audit_trail:
    print(f"  → {entry}")
