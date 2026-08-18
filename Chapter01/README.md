# Chapter 1: The Platform Engineering Renaissance

This chapter establishes the foundational principles of platform engineering and introduces the abstraction shift that Domain-Driven Platform Engineering (DDPE) brings to the discipline.

## Files

### `01-01-abstraction.py`
A microservice scaffolding tool that demonstrates platform abstraction in action. Given a service name and domain, it generates a complete project structure with pre-configured CI/CD pipelines, observability setup, and domain-specific configuration — showing how platforms reduce cognitive load by encoding best practices into golden-path templates.

### `01-02-ownership.py`
A governance validation script that checks Infrastructure-as-Code resource definitions for mandatory ownership tags (`Owner`, `Domain`, `Environment`). Demonstrates how platform teams embed compliance checks directly into CI pipelines so that governance becomes an automatic property of the platform rather than a manual burden.

### `01-03-customer-profile-api.yaml`
A declarative service provisioning request showing how developers express intent using domain concepts — bounded context, data classification, compliance requirements — rather than specifying low-level infrastructure details. The platform infers compute, networking, storage, and security settings from the domain context.

## Running the Code

```bash
python 01-01-abstraction.py
python 01-02-ownership.py
```

## Simulation Data

All scripts use embedded simulation data — no external dependencies required. See [Simulation Data Sources](../README.md#simulation-data-sources) in the repository root for a categorized overview across all chapters.

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.com) covers the broader principles of self-service platform interfaces
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides a comprehensive guide to building secure, developer-focused platforms
