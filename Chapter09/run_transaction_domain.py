"""
Chapter 9: BFSI Transaction Domain — Multi-Scenario Demo

Extends the transaction_domain.py model to process multiple
transactions across different regulatory scopes, amounts, and
channels — showing how domain-driven platforms automatically
apply the right compliance controls based on context.

Run: python Chapter09/run_transaction_domain.py
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
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
        for scope in self.regulatory_scopes:
            if scope == RegulatoryScope.AML:
                self._aml_check()
            elif scope == RegulatoryScope.PCI_DSS:
                self._pci_logging()
            elif scope == RegulatoryScope.KYC:
                self._kyc_check()
            elif scope == RegulatoryScope.DODD_FRANK:
                self._dodd_frank_reporting()
        if self.metadata.amount > 10000:
            self.audit_trail.append("Approval required: senior manager")
        if self.metadata.amount > 50000:
            self.audit_trail.append("Enhanced due diligence: triggered")
        return self

    def _aml_check(self):
        self.audit_trail.append("AML screening: passed")

    def _pci_logging(self):
        self.audit_trail.append("PCI-DSS: transaction logged to secure audit store")

    def _kyc_check(self):
        self.audit_trail.append("KYC: customer identity verified")

    def _dodd_frank_reporting(self):
        self.audit_trail.append("Dodd-Frank: regulatory report queued")


# ── Test transactions ───────────────────────────────────────────────

TRANSACTIONS = [
    {
        "id": "TX-20240115-001",
        "desc": "Standard retail transfer (under threshold)",
        "meta": TransactionMetadata(
            source="checking-001", destination="savings-002",
            amount=2500, currency="USD",
            justification="Customer savings transfer",
        ),
        "scopes": [RegulatoryScope.PCI_DSS],
        "context": {"product": "retail-banking", "channel": "mobile"},
    },
    {
        "id": "TX-20240115-002",
        "desc": "High-value transfer (triggers AML + approval)",
        "meta": TransactionMetadata(
            source="checking-003", destination="external-wire-004",
            amount=25000, currency="USD",
            justification="Customer-initiated wire transfer",
        ),
        "scopes": [RegulatoryScope.PCI_DSS, RegulatoryScope.AML, RegulatoryScope.KYC],
        "context": {"product": "retail-banking", "channel": "branch"},
    },
    {
        "id": "TX-20240115-003",
        "desc": "Very high-value institutional trade (full regulatory suite)",
        "meta": TransactionMetadata(
            source="trading-desk-A", destination="settlement-pool-B",
            amount=75000, currency="USD",
            justification="Institutional equity settlement",
        ),
        "scopes": [RegulatoryScope.PCI_DSS, RegulatoryScope.AML,
                    RegulatoryScope.KYC, RegulatoryScope.DODD_FRANK],
        "context": {"product": "institutional-trading", "channel": "direct-api"},
    },
    {
        "id": "TX-20240115-004",
        "desc": "Cross-border payment (GDPR + AML)",
        "meta": TransactionMetadata(
            source="eu-account-101", destination="us-account-202",
            amount=8000, currency="EUR",
            justification="Cross-border business payment",
        ),
        "scopes": [RegulatoryScope.PCI_DSS, RegulatoryScope.AML, RegulatoryScope.GDPR],
        "context": {"product": "cross-border-payments", "channel": "online-portal"},
    },
    {
        "id": "TX-20240115-005",
        "desc": "Micro-payment (minimal compliance)",
        "meta": TransactionMetadata(
            source="wallet-A", destination="merchant-B",
            amount=12.50, currency="USD",
            justification="Point-of-sale purchase",
        ),
        "scopes": [RegulatoryScope.PCI_DSS],
        "context": {"product": "digital-wallet", "channel": "contactless"},
    },
]


def main():
    print("=" * 64)
    print("BFSI TRANSACTION DOMAIN — COMPLIANCE AUTOMATION")
    print("=" * 64)

    print("\n  The platform applies regulatory controls automatically")
    print("  based on transaction metadata. The developer provides")
    print("  business context; the platform handles compliance.")

    # ── Show regulatory scopes ──
    print(f"\n  REGULATORY SCOPES")
    print(f"  {'─' * 58}")
    scope_triggers = {
        "PCI-DSS": "All transactions (audit logging)",
        "AML": "Flagged transfers, high-value, cross-border",
        "KYC": "New counterparties, high-value",
        "Dodd-Frank": "Institutional trades, derivatives",
        "GDPR": "Cross-border involving EU data subjects",
    }
    for scope, trigger in scope_triggers.items():
        print(f"    {scope:<12s}  {trigger}")

    # ── Process transactions ──
    print(f"\n{'=' * 64}")
    print("TRANSACTION PROCESSING")
    print("=" * 64)

    compliance_counts = {}

    for t in TRANSACTIONS:
        txn = Transaction(
            id=t["id"],
            metadata=t["meta"],
            regulatory_scopes=t["scopes"],
            domain_context=t["context"],
        )
        txn.submit()

        print(f"\n  {t['desc']}")
        print(f"  ┌─ ID:       {t['id']}")
        print(f"  │  Amount:   ${t['meta'].amount:,.2f} {t['meta'].currency}")
        print(f"  │  Channel:  {t['context']['channel']}")
        print(f"  │  Product:  {t['context']['product']}")
        print(f"  │  Scopes:   {', '.join(s.value for s in t['scopes'])}")
        print(f"  └─ Controls applied ({len(txn.audit_trail)}):")

        for entry in txn.audit_trail:
            icon = "✅" if "passed" in entry or "verified" in entry or "created" in entry or "logged" in entry else "⚠ "
            print(f"       {icon} {entry}")

        for scope in t["scopes"]:
            compliance_counts[scope.value] = compliance_counts.get(scope.value, 0) + 1

    # ── Summary ──
    print(f"\n{'=' * 64}")
    print("COMPLIANCE SUMMARY")
    print("=" * 64)

    print(f"\n  Transactions processed: {len(TRANSACTIONS)}")
    print(f"\n  Compliance controls triggered:")
    for scope, count in sorted(compliance_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {scope:<24s}  {count}× across {len(TRANSACTIONS)} transactions")

    # Amount-based analysis
    total_amount = sum(t["meta"].amount for t in TRANSACTIONS)
    high_value = [t for t in TRANSACTIONS if t["meta"].amount > 10000]
    very_high = [t for t in TRANSACTIONS if t["meta"].amount > 50000]

    print(f"\n  Amount analysis:")
    print(f"    Total volume:           ${total_amount:,.2f}")
    print(f"    Require approval:       {len(high_value)} (>${'10,000'})")
    print(f"    Enhanced due diligence: {len(very_high)} (>${'50,000'})")

    print(f"\n  The developer provides: transaction ID, amount, source,")
    print(f"  destination, and product context.")
    print(f"  The platform provides: every compliance control, audit log")
    print(f"  entry, approval routing, and regulatory report.")
    print(f"\n  Compliance is a property of the platform, not a developer task.")


if __name__ == "__main__":
    main()
