# Domain-Driven Platform Engineering — Companion Code

[![Apress](https://img.shields.io/badge/Publisher-Apress-blue)](https://link.springer.com/book/10.1007/979-8-8688-2761-7)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)](https://www.python.org/)

Companion code repository for **Domain-Driven Platform Engineering: How to Build Context-Aware, Scalable, and Self-Service Platforms for the Enterprise** by Ajay Chankramath and Eamonn Ryan (Apress, 2026).

## About the Book

Platform engineering has matured as a discipline, but adoption remains uneven. Generic platforms — one-size-fits-all CI/CD, observability, and deployment templates — hit a ceiling because the hardest engineering problems are domain-specific. This book introduces Domain-Driven Platform Engineering (DDPE), applying Domain-Driven Design principles to platform engineering so that platforms speak the language of the business domains they serve.

The code in this repository provides working implementations, assessment models, policy examples, and data tools that accompany each chapter. Every example is designed to be runnable and adaptable to your own organization.

## Repository Structure

```
.
├── Chapter01/   # The Platform Engineering Renaissance
├── Chapter02/   # Understanding Domains in an Engineering Context
├── Chapter03/   # DDD Meets Platform Engineering
├── Chapter04/   # Anatomy of a Domain-Driven Platform
├── Chapter05/   # Team Topologies and Platform as a Product
├── Chapter06/   # Golden Paths and API Design per Domain
├── Chapter07/   # Measuring Platform Success
├── Chapter08/   # Patterns for Scaling Platform Adoption
├── Chapter09/   # Real-World Case Studies
├── Chapter10/   # GenAI and Autonomous Platforms
└── requirements.txt
```

Each chapter folder contains its own `README.md` with detailed descriptions of every file.

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip

### Installation

```bash
git clone https://github.com/apress/domain-driven-platform-engineering.git
cd domain-driven-platform-engineering
pip install -r requirements.txt
```

### Running the Code

Most Python files are self-contained and can be run directly:

```bash
python Chapter01/01-01-abstraction.py
python Chapter07/friction_score.py
python Chapter10/genai_platform_interface.py
```

Excel workbooks (`.xlsx`) can be opened in Microsoft Excel, Google Sheets, or LibreOffice Calc. YAML and SQL files are provided as reference configurations and queries.

## Chapter Overview

| Chapter | Title | Code Focus |
|---------|-------|------------|
| 1 | The Platform Engineering Renaissance | Platform abstraction, golden-path scaffolding, governance validation |
| 2 | Understanding Domains in an Engineering Context | Domain identification scorecard |
| 3 | DDD Meets Platform Engineering | Bounded context enforcement, layer separation, architectural fitness functions |
| 4 | Anatomy of a Domain-Driven Platform | Escape hatches, evolution policies, onboarding flows, telemetry, deviation analytics |
| 5 | Team Topologies and Platform as a Product | Service definitions, platform product canvas |
| 6 | Golden Paths and API Design per Domain | Domain-centric APIs, opinionated defaults, OPA guardrails |
| 7 | Measuring Platform Success | DORA metrics, friction scoring, platform ROI modeling |
| 8 | Patterns for Scaling Platform Adoption | Adoption anti-pattern detection, phased rollout planning |
| 9 | Real-World Case Studies | BFSI transaction domains, healthcare data governance, schema validation |
| 10 | GenAI and Autonomous Platforms | GenAI-driven prompt-to-infrastructure interface |

## Dependencies

The codebase intentionally uses minimal dependencies:

- **openpyxl** — Excel file generation (used by assessment and scoring tools across chapters)
- **opentelemetry-api / opentelemetry-sdk** — Optional; used in Chapter 4 and Chapter 7 for observability examples. The code handles their absence gracefully.

## Simulation Data Sources

Every script in this repository is self-contained — no external databases, APIs, or credentials are required. The simulation data embedded in each script falls into three categories:

**Domain Registries and Policy Matrices.** Static configuration that defines how domains behave: regulatory rules for BFSI transactions (Ch9), the 80-15-5 override policy matrix (Ch6), domain defaults for Payments/Healthcare/Marketing (Ch6), OPA guardrail policies (Ch6), escape-hatch tier classifications (Ch4), evolution policies per platform layer (Ch4), dashboard panel definitions (Ch4), bounded context boundary maps (Ch3), service catalog definitions (Ch5), anti-pattern catalogs (Ch8), rollout phase definitions (Ch8), domain context registries for GenAI (Ch10), and bounded context profiles for entropy scoring (Ch7).

**Simulated User Requests.** The transactions, provisioning requests, and developer actions that exercise the domain registries: five BFSI transactions from $12.50 contactless to $75K institutional (Ch9), patient data access attempts with care-team validation (Ch9), seven service definitions tested against schema governance (Ch9), database provisioning requests across domains (Ch5, Ch6), natural-language developer prompts parsed into provisioning intents (Ch10), deployment and incident records for DORA tracking (Ch7), deviation records seeded into SQLite (Ch4), and IaC resource definitions checked for ownership tags (Ch1).

**Scoring and Assessment Frameworks.** The rubrics, thresholds, and weighting criteria that produce quantitative outputs: friction source weights and trend analysis (Ch7), 4-layer compliance depth scoring with adoption theater detection (Ch7), platform entropy across model drift, path staleness, and boundary erosion (Ch7), multi-scenario ROI modeling with breakeven analysis (Ch7), flexibility scoring across standardization and developer autonomy axes (Ch6), customization graduation criteria from Table 6-5 (Ch6), and adoption health scoring against anti-pattern indicators (Ch8).

All data is representative of real-world patterns but uses fictional organizations, amounts, and identifiers. To adapt examples for your own organization, modify the data structures at the top of each script — the processing logic remains the same.

## Also by Ajay Chankramath

- **[Effective Platform Engineering](https://effectiveplatformengineering.com)** — Build self-service interfaces to boost developer experience (Manning, 2025)
- **[The Platform Engineer's Handbook](https://peh-packt.platformetrics.com)** — Build secure, developer-focused platforms that streamline modern software delivery (Packt, 2026)

## Companion Site

Visit **[ddpe.platformetrics.com](https://ddpe.platformetrics.com)** for updated examples, revised recommendations, and new code as the tools and frameworks covered in the book evolve.

## License

This code is provided as companion material to the book. See the [Apress Source Code License](https://www.apress.com/gp/services/source-code) for terms.
