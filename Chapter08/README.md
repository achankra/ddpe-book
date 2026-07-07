# Chapter 8: Patterns for Scaling Platform Adoption

This chapter addresses the hardest problem in platform engineering — getting engineers to actually use the platform. It covers adoption anti-patterns, catalysts, and a phased rollout strategy grounded in domain-driven thinking.

## Files

### `adoption_health.py`
Defines common platform adoption anti-patterns — including "build it and they will come," "platform as gatekeeper," and "ignoring bounded contexts" — with warning signs and recommended interventions for each. Includes a health-check scorer that evaluates your platform's current adoption posture and flags risks before they become entrenched.

### `rollout_planner.py`
A four-phase rollout strategy planner covering Pilot, Early Expansion, Broad Adoption, and Organizational Standard. Each phase defines duration, key activities, success criteria, and DDD focus areas. Use it to plan a realistic adoption trajectory that builds confidence incrementally rather than attempting a big-bang rollout.

### `Adoption_Scoring.xlsx`
Measure adoption depth across teams and domains — beyond simple usage counts to real benefit.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. For each team and domain, score adoption across multiple dimensions: active usage, integration depth, self-service utilization, and developer satisfaction. The workbook produces an adoption depth score that distinguishes teams that are genuinely benefiting from the platform versus those with only surface-level adoption.

> **Interactive version available:** An interactive version of this scoring tool is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

### `MaturityModel.xlsx`
Platform adoption maturity model: Ad Hoc, Emerging, Established, Optimized. Benchmark your organization and plan the next level.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Assess your organization against each maturity dimension to determine your current stage. The workbook identifies the specific investments and milestones needed to progress from your current level to the next, providing a concrete roadmap for scaling platform adoption.

> **Interactive version available:** An interactive version of this maturity model is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python3 adoption_health.py
python3 rollout_planner.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers adoption strategies and developer experience optimization
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides additional patterns for scaling platform adoption across enterprise organizations
