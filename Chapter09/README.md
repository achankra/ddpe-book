# Chapter 9: Real-World Case Studies

This chapter brings DDPE to life through three industry case studies — BFSI (Banking, Financial Services, and Insurance), Healthcare, and Semiconductor Manufacturing — demonstrating how domain-driven platforms solve problems that generic platforms cannot.

## Files

### `transaction_domain.py`
A BFSI transaction domain model that automatically applies regulatory compliance controls based on transaction metadata. High-value transactions trigger AML (Anti-Money Laundering) screening and enhanced logging; all transactions get PCI-DSS compliant audit trails. Demonstrates how domain-driven platforms encode regulatory requirements into the platform layer so that compliance becomes automatic rather than manual.

### `patient_data_domain.py`
A healthcare patient data domain implementing care-team-based access control with mandatory audit logging for every access attempt — granted or denied. Demonstrates HIPAA-aligned secure defaults where patient data access requires both authentication and a valid care-team relationship, with full auditability built into the platform.

### `schema_governance.py`
A schema-based governance system that validates service definitions against domain schemas, enforcing that production and mission-critical services declare telemetry endpoints, alert thresholds, and ownership metadata. Uses the semiconductor manufacturing domain as its context — showing how schema governance applies beyond traditional software domains.

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
python transaction_domain.py
python patient_data_domain.py
python schema_governance.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers platform patterns for regulated industries
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides additional case studies and implementation patterns
