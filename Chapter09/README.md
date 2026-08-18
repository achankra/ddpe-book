# Chapter 9: Real-World Case Studies

This chapter brings DDPE to life through three industry case studies — BFSI (Banking, Financial Services, and Insurance), Healthcare, and Semiconductor Manufacturing — demonstrating how domain-driven platforms solve problems that generic platforms cannot.

## Files

### `transaction_domain.py`
A BFSI transaction domain model that automatically applies regulatory compliance controls based on transaction metadata. High-value transactions trigger AML (Anti-Money Laundering) screening and enhanced logging; all transactions get PCI-DSS compliant audit trails. Demonstrates how domain-driven platforms encode regulatory requirements into the platform layer so that compliance becomes automatic rather than manual.

### `run_transaction_domain.py`
Extends `transaction_domain.py` to process five transactions across different regulatory scopes, amounts, and channels — from a $12.50 contactless payment (PCI-DSS only) to a $75,000 institutional trade (PCI-DSS + AML + KYC + Dodd-Frank). Shows per-transaction compliance controls, amount-based analysis (approval thresholds, enhanced due diligence), and a compliance summary with control trigger counts.

```bash
python3 run_transaction_domain.py
```

### `patient_data_domain.py`
A healthcare patient data domain implementing care-team-based access control with mandatory audit logging for every access attempt — granted or denied. Demonstrates HIPAA-aligned secure defaults where patient data access requires both authentication and a valid care-team relationship, with full auditability built into the platform.

### `schema_governance.py`
A schema-based governance system that validates service definitions against domain schemas, enforcing that production and mission-critical services declare telemetry endpoints, alert thresholds, and ownership metadata. Uses the semiconductor manufacturing domain as its context — showing how schema governance applies beyond traditional software domains.

### `run_schema_governance.py`
Extends `schema_governance.py` to validate seven services across four criticality tiers and multiple domains (semiconductor, BFSI, healthcare, internal tooling). Shows both passing and failing validations — missing telemetry endpoints, missing alert thresholds, undeclared dependencies on mission-critical services, missing ownership. Includes a governance summary with pass/fail rates by criticality tier.

```bash
python3 run_schema_governance.py
```

### `Before-After-Case-Study.xlsx`
Before/after metrics showing measurable improvements after DDPE adoption across industries.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Review the pre-populated case study data covering deployment frequency, compliance error rates, onboarding time, and developer satisfaction. Use the workbook as a template to document your own before/after metrics as you adopt DDPE — providing concrete evidence of platform impact to leadership and stakeholders.

> **Interactive version available:** An interactive version of this case study template is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

### `DDD Pattern Matrix.xlsx`
Maps DDD patterns to their value across BFSI, Healthcare, and Semiconductor domains.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Review how DDD patterns (bounded contexts, aggregates, domain events, anti-corruption layers) apply across the three case study domains. Use the matrix to identify which patterns will deliver the most value in your own industry context and prioritize your DDD adoption accordingly.

> **Interactive version available:** An interactive version of this pattern matrix is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python3 transaction_domain.py
python3 run_transaction_domain.py
python3 patient_data_domain.py
python3 schema_governance.py
python3 run_schema_governance.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers platform patterns for regulated industries
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides additional case studies and implementation patterns
