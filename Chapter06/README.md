# Chapter 6: Golden Paths and API Design per Domain

This chapter covers the platform's published language — how to design domain-centric APIs with opinionated defaults, override patterns, and compliance guardrails that make the secure path the easy path.

## Files

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

The `.http` file can be used with VS Code's REST Client extension or any HTTP client. The `.rego` file can be evaluated with OPA:

```bash
opa eval -i input.json -d guardrails.rego "data.guardrails"
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers API design for self-service platform interfaces
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides comprehensive coverage of policy-as-code and security guardrails
