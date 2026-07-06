# Chapter 7: Measuring Platform Success

This chapter introduces a comprehensive measurement framework for domain-driven platforms — from DORA metrics and developer friction scoring to platform ROI modeling that speaks the language of business leadership.

## Files

### `dora_metrics.py`
A domain-aware DORA metrics tracker that records deployments and computes the four key DORA metrics — deployment frequency, lead time for changes, change failure rate, and mean time to recovery — broken down by domain. Unlike generic DORA tracking, this implementation lets you compare platform performance across different business domains and identify where domain-specific friction is dragging down delivery.

### `friction_score.py`
A developer friction score calculator that weights multiple friction sources — cross-team dependencies, test flakiness, security assessment delays, environment provisioning time, and more — into a composite score. Includes trend analysis and predictive warnings so platform teams can address rising friction before it impacts adoption.

### `platform_roi.py`
A platform ROI calculator that models build costs, ongoing maintenance, and developer productivity gains across a multi-year adoption ramp. Computes cumulative ROI with breakeven analysis — giving platform leaders the financial language they need to justify and sustain platform investment to business stakeholders.

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
python dora_metrics.py
python friction_score.py
python platform_roi.py
```

## Related Reading

- [Effective Platform Engineering](https://effectiveplatformengineering.org) covers developer experience metrics and feedback loops
- [The Platform Engineer's Handbook](https://peh-packt.platformetrics.com) provides additional measurement frameworks for platform maturity
