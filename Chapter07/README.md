# Chapter 7: Measuring Platform Success

This chapter introduces a comprehensive measurement framework for domain-driven platforms — from DORA metrics and developer friction scoring to platform ROI modeling that speaks the language of business leadership.

## Files

### `dora_metrics.py`
A domain-aware DORA metrics tracker that records deployments and computes the four key DORA metrics — deployment frequency, lead time for changes, change failure rate, and mean time to recovery — broken down by domain. Unlike generic DORA tracking, this implementation lets you compare platform performance across different business domains and identify where domain-specific friction is dragging down delivery.

### `friction_score.py`
A developer friction score calculator that weights multiple friction sources — cross-team dependencies, test flakiness, security assessment delays, environment provisioning time, and more — into a composite score. Includes trend analysis and predictive warnings so platform teams can address rising friction before it impacts adoption.

### `platform_roi.py`
A platform ROI calculator that models build costs, ongoing maintenance, and developer productivity gains across a multi-year adoption ramp. Computes cumulative ROI with breakeven analysis — giving platform leaders the financial language they need to justify and sustain platform investment to business stakeholders.

### `platform_entropy_score.py`
Implements the **Platform Entropy Score** — the meta-measurement that tracks how fast the platform itself is drifting from domain truth. Measures drift across three dimensions: **Model Drift** (how far platform domain models have diverged from current business processes), **Path Staleness** (what percentage of golden paths have not been updated in response to business model changes), and **Boundary Erosion** (how many cross-context calls bypass official anti-corruption layers). A rising entropy score is the leading indicator that your platform is becoming legacy.

Run it to see entropy profiles for five sample bounded contexts with quarterly trend analysis:

```bash
python3 platform_entropy_score.py
```

> **Interactive version available:** The Platform Entropy Score tab in the [Measuring Platform Success](https://ddpe.platformetrics.com) interactive tool provides a UI for tracking entropy across your bounded contexts over time.

### `compliance_depth_index.py`
Implements the **Golden Path Compliance Depth Index** first introduced in this chapter. Scores how deeply teams have adopted each golden path across four layers — **Surface** (using the tools), **Structural** (following architecture patterns), **Behavioral** (preserving opinionated defaults), and **Cultural** (championing the platform). Uses weighted scoring where deeper layers count more, and detects "adoption theater" — teams that score high on Surface but low on Behavioral/Cultural, signaling they appear adopted but are actively diverging.

Run it to see depth profiles for six sample teams with radar charts, risk assessments, and portfolio-level analytics:

```bash
python3 compliance_depth_index.py
```

> **Interactive version available:** The Compliance Depth Index tab in the [Measuring Platform Success](https://ddpe.platformetrics.com) interactive tool provides a UI for scoring your teams' adoption depth across golden paths.

### `Platform Return on Investment.xlsx`
Interactive ROI model with pre-built formulas for multi-scenario, multi-year analysis.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. Enter your platform's build costs, ongoing maintenance costs, and expected developer productivity gains. Adjust the adoption ramp assumptions for your organization. The workbook computes cumulative ROI across multiple scenarios with breakeven analysis — giving platform leaders the financial language they need to justify and sustain platform investment.

> **Interactive version available:** An interactive version of this ROI model is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

### `Team Level Metrics tied to business outcomes.xlsx`
Maps team-level engineering metrics to business outcomes. Use to demonstrate the platform-to-revenue connection.

**How to use:** Open in Microsoft Excel, Google Sheets, or LibreOffice Calc. For each team, map their engineering metrics (deployment frequency, lead time, defect rates) to the business outcomes that leadership tracks (revenue impact, customer satisfaction, time-to-market). The completed workbook provides the evidence platform teams need to demonstrate that platform investments translate into business results.

> **Interactive version available:** An interactive version of this metrics mapping is available at [ddpe.platformetrics.com](https://ddpe.platformetrics.com).

## Running the Code

```bash
python3 dora_metrics.py
python3 friction_score.py
python3 platform_roi.py
python3 platform_entropy_score.py
python3 compliance_depth_index.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers developer experience metrics and feedback loops
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides additional measurement frameworks for platform maturity
