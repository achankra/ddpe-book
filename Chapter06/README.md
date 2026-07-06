# Chapter 6: Golden Paths and API Design per Domain

This chapter covers the platform's published language — how to design domain-centric APIs with opinionated defaults, override patterns, and compliance guardrails that make the secure path the easy path.

## Files

### `override_validator.py`
An override validator implementing the **80-15-5 override pyramid** described in the chapter. Validates configuration change requests against a policy matrix that classifies every platform configuration into one of three tiers: **Flexible** (~80%, self-service, no approval), **Governed** (~15%, requires justification and platform team review), or **Blocked** (~5%, never permitted — non-negotiable security controls). The validator provides immediate feedback: why a configuration is blocked, what justification is needed for a governed override, or confirmation that a flexible change was auto-approved.

Run it to see the full override matrix and seven sample validation scenarios across all tiers:

```bash
python3 override_validator.py
```

> **Interactive version available:** The Override Validator tab in the [API Design Standards & Guardrails](https://ddpe.platformetrics.com) interactive tool provides a UI for defining and testing override rules.

### `flexibility_scoring.py`
A scoring tool that evaluates the balance between standardization and flexibility across platform configuration areas. Each area is rated on two axes — Standardization (1-5) and Flexibility (1-5) — plus qualitative assessments of developer friction and risk. The tool generates per-area recommendations: identifying over-standardization (high friction), under-standardization (inconsistency risk), appropriate locks (critical-risk areas), and well-balanced policies.

Run it to see a portfolio assessment of six sample configuration areas:

```bash
python3 flexibility_scoring.py
```

> **Interactive version available:** The Flexibility Scoring tab in the [API Design Standards & Guardrails](https://ddpe.platformetrics.com) interactive tool provides a UI for scoring your own configuration areas.

### `customization_tracker.py`
A lifecycle tracker for domain-specific customization requests, implementing the graduation criteria from Table 6-5 in the chapter. Tracks customizations through five stages — Requested → Approved → Implemented → Monitoring → Graduated — and evaluates each against graduation thresholds: 3+ requesting teams, 5+ active implementations, 3+ months in production, and a decreasing support ticket trend. When all criteria are met, the customization is ready to be absorbed into platform defaults.

Run it to see a portfolio of six sample customizations at various lifecycle stages with graduation assessments:

```bash
python3 customization_tracker.py
```

> **Interactive version available:** The Customization Tracker tab in the [API Design Standards & Guardrails](https://ddpe.platformetrics.com) interactive tool provides a UI for logging and tracking customization requests through their lifecycle.

### `domain-specific-api.http`
An HTTP request example demonstrating a domain-centric database provisioning API. The developer provides only three parameters — name, tier, and purpose — and the platform auto-applies domain-aware defaults including encryption, compliance controls, and backup policies based on the domain context. Contrast this with a generic API that would require dozens of explicit configuration fields.

### `domain_defaults.yaml`
A YAML configuration defining opinionated domain defaults for the Payments domain. Covers compute sizing, database settings (encryption at rest, backup retention), security policies (OAuth 2.0, RBAC, PCI-DSS compliance), and observability configuration (metrics, tracing, log levels). This is the configuration that powers the "smart defaults" behavior described in the chapter.

### `guardrails.rego`
Open Policy Agent (Rego) policy rules enforcing security, compliance, and operational guardrails. Examples include: public-facing services must have WAF enabled, databases must use encryption at rest, PCI-DSS domains require 90-day backup retention, and all deployments must define health checks. These policies run at the platform level, making compliance automatic rather than advisory.

### `API_Design_Standards.xlsx`
Documents API naming conventions, versioning strategy, error formats, and domain-specific patterns.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Review and customize the documented standards for your organization's API conventions. Fill in your domain-specific naming patterns, versioning rules, error response formats, and endpoint design standards. The workbook serves as a living reference that ensures consistency across domain-centric platform APIs.

> **Interactive version available:** An interactive version of this standards workbook is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python3 override_validator.py
python3 flexibility_scoring.py
python3 customization_tracker.py
```

The `.http` file can be used with VS Code's REST Client extension or any HTTP client. The `.rego` file can be evaluated with OPA:

```bash
opa eval -i input.json -d guardrails.rego "data.guardrails"
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers API design for self-service platform interfaces
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides comprehensive coverage of policy-as-code and security guardrails
