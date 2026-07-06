# Chapter 10: GenAI and Autonomous Platforms

This chapter looks at the future of platform engineering — how generative AI, agentic workflows, and composable architectures are reshaping the discipline, and why domain-driven platforms provide the architectural scaffolding that makes enterprise-grade AI-assisted engineering safe and effective.

## Files

### `genai_platform_interface.py`
A GenAI-driven platform interface that parses natural-language developer prompts (e.g., "I need a production database for the payments domain") into structured provisioning intents, then auto-applies domain-aware infrastructure defaults. Demonstrates the prompt-driven interface pattern discussed in the chapter — where the platform interprets developer intent through domain context rather than requiring explicit configuration.

The implementation includes:
- **Intent parsing** — extracts action, resource type, domain, and tier from natural language
- **Domain context resolution** — maps domains to compliance frameworks and data classifications
- **Automatic default application** — applies encryption, audit logging, backup policies, and observability settings based on domain context
- **Resource-specific configuration** — different defaults for databases, event streams, caches, and services

### `GenAI - 6 Level Maturity Model.xlsx`
Six-level maturity model for GenAI adoption in platform engineering — from basic code assist through fully autonomous operations.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Assess your organization against each of the six maturity levels to determine where you currently stand. The workbook identifies the capabilities, governance structures, and domain context needed to progress to each subsequent level, providing a realistic GenAI adoption roadmap for your platform team.

> **Interactive version available:** An interactive version of this maturity model is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

### `GenAI Readiness Assessment.xlsx`
Evaluate your platform's readiness for GenAI-augmented workflows: data readiness, governance, domain context, and team capability.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Rate your platform across each readiness dimension — data quality and availability, governance frameworks, domain context richness, and team capability. The workbook produces a readiness score and highlights the specific gaps that must be addressed before GenAI-augmented workflows can be safely and effectively adopted.

> **Interactive version available:** An interactive version of this readiness assessment is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python genai_platform_interface.py
```

The script runs three example prompts demonstrating how the same interface handles different domains and resource types with appropriate domain-aware defaults.

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers the foundations of self-service platform interfaces that GenAI extends
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides practical guidance on AI-augmented platform services and automation
