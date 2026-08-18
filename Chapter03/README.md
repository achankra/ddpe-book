# Chapter 3: DDD Meets Platform Engineering

This chapter bridges Domain-Driven Design with platform engineering, covering bounded contexts, the four-layered service taxonomy, and strategic vs. tactical design patterns for platforms.

## Files

### `check_boundaries.py`
A bounded context violation detector that scans source files to identify unauthorized cross-context imports. Define allowed dependencies between bounded contexts, and the tool flags any module that reaches across boundaries it should not. Run this in CI to enforce context boundaries as your platform grows.

### `layer_separation.py`
Demonstrates the Repository Pattern for enforcing clean layer separation. Contrasts a tightly-coupled service that imports database drivers directly against a properly abstracted service that depends on a repository interface — showing how DDPE keeps infrastructure concerns out of domain logic.

### `test_architecture.py`
An architectural fitness function implemented as a pytest test. Asserts that service-layer files never directly import datastore libraries (`sqlalchemy`, `pymongo`, `boto3`, `psycopg2`), enforcing the layer isolation principle. Drop this into your test suite to catch architectural drift automatically.

### `ddpe_strategic_tactical_assessment.xlsx`
Evaluate whether your platform needs strategic DDD patterns (bounded contexts, context maps, published language), tactical patterns (aggregates, repositories, domain events), or both. Produces a right-sized DDD investment recommendation.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Rate your organization's maturity across each strategic and tactical dimension. The workbook produces a recommendation on where to focus your DDD investment based on your platform's current state and growth trajectory.

> **Interactive version available:** An interactive version of this assessment is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python check_boundaries.py
python layer_separation.py
pytest test_architecture.py
```

## Simulation Data

All scripts use embedded simulation data — no external dependencies required. See [Simulation Data Sources](../README.md#simulation-data-sources) in the repository root for a categorized overview across all chapters.

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.com) — covers strategic and tactical patterns for platform teams
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) — covers modular platform architecture and service boundary design
