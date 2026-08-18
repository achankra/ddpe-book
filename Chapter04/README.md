# Chapter 4: Anatomy of a Domain-Driven Platform

This chapter dissects the internal architecture of a domain-driven platform — its layering model, golden paths with controlled deviation, onboarding flows, and observability design.

## Files

### `escape_hatch.py`
An escape-hatch registry that classifies deviations from golden paths into three tiers: **blocked** (never permitted), **self-service** (auto-approved with logging), and **approval-required** (routed to platform team review). Demonstrates how platforms balance standardization with the flexibility engineers need in practice.

### `evolution_policy.py`
Defines versioning and evolution policies per platform layer — core, domain, and extension. Encodes rules for deprecation notice periods, migration support windows, and whether breaking changes are permitted at each layer. Use this pattern to manage platform evolution without breaking consumer trust.

### `onboarding_flow.py`
Models a multi-step developer onboarding flow (initialize, scaffold, configure, deploy, observe) using a fluent builder pattern. Shows the full lifecycle of bringing a new service onto the platform, from first command to first production deployment.

### `platform_telemetry.py`
Sets up OpenTelemetry-based instrumentation for platform operations. Defines counters and histograms for template instantiations, onboarding duration, and deviation requests, plus a tracing decorator for platform API calls. Requires `opentelemetry-api` and `opentelemetry-sdk` (optional — the code handles their absence gracefully).

### `deviation_analytics.sql`
A SQL query that aggregates golden-path deviation data over 90 days by type and domain, calculates approval rates, and recommends whether frequently-approved deviations should be absorbed into the golden path. Use this against your platform's deviation tracking database to evolve your golden paths based on real usage data.

### `run_deviation_analytics.py`
Python wrapper for `deviation_analytics.sql`. Creates an in-memory SQLite database seeded with sample deviation data across BFSI-Payments, Healthcare, and Retail domains, then runs the SQL query from the book. Demonstrates how the query surfaces deviations that should become golden path capabilities (3+ teams, >80% approval) versus patterns that need better guardrails (<20% approval).

### `payments_dashboard.yaml`
A domain dashboard definition for a Payments monitoring setup with panels for transaction success rate, settlement latency, volume by type, and error rate by payment method. Includes alerting rules with domain-appropriate thresholds — showing how observability should be domain-aware, not generic.

### `Platform_Anatomy_Assessment.xlsx`
Assess your platform's maturity across layering, golden paths, deviation management, and observability.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Rate your platform across each anatomy dimension — layering model clarity, golden path coverage, deviation management maturity, and observability depth. The workbook highlights gaps and produces a maturity profile that guides your next platform investments.

> **Interactive version available:** An interactive version of this assessment is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python escape_hatch.py
python evolution_policy.py
python onboarding_flow.py
python platform_telemetry.py
python run_deviation_analytics.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) provides implementation patterns for golden paths and self-service interfaces
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) covers platform observability and telemetry design in depth
