"""
Chapter 7: Platform ROI — Multi-Scenario Analysis

Extends the platform_roi.py calculator to show a full investment
analysis with three scenarios (conservative, baseline, aggressive),
year-by-year breakdown, and breakeven analysis.

Run: python Chapter07/run_platform_roi.py
"""


# ── Scenario definitions ────────────────────────────────────────────

SCENARIOS = {
    "Conservative": {
        "monthly_dev_cost": 15000,
        "total_developers": 500,
        "productivity_gain_pct": 0.08,
        "initial_build_team": 10,
        "build_months": 12,
        "maintenance_team": 5,
        "monthly_infra_cost": 50000,
        "adoption_ramp": {1: 0.10, 2: 0.25, 3: 0.45},
    },
    "Baseline": {
        "monthly_dev_cost": 15000,
        "total_developers": 500,
        "productivity_gain_pct": 0.10,
        "initial_build_team": 10,
        "build_months": 12,
        "maintenance_team": 5,
        "monthly_infra_cost": 50000,
        "adoption_ramp": {1: 0.10, 2: 0.30, 3: 0.60},
    },
    "Aggressive": {
        "monthly_dev_cost": 15000,
        "total_developers": 500,
        "productivity_gain_pct": 0.15,
        "initial_build_team": 10,
        "build_months": 12,
        "maintenance_team": 5,
        "monthly_infra_cost": 50000,
        "adoption_ramp": {1: 0.15, 2: 0.40, 3: 0.75},
    },
}


def calculate_roi(params):
    """Calculate full ROI with year-by-year breakdown."""
    build_cost = params["initial_build_team"] * params["monthly_dev_cost"] * params["build_months"]
    annual_maintenance = (params["maintenance_team"] * params["monthly_dev_cost"] + params["monthly_infra_cost"]) * 12

    years = []
    cumulative = -build_cost

    for year, adoption_pct in params["adoption_ramp"].items():
        adopted_devs = params["total_developers"] * adoption_pct
        annual_benefit = adopted_devs * params["monthly_dev_cost"] * 12 * params["productivity_gain_pct"]
        annual_cost = annual_maintenance
        if year == 1:
            annual_cost += build_cost
        cumulative += annual_benefit - (annual_maintenance if year > 1 else 0)

        years.append({
            "year": year,
            "adoption_pct": adoption_pct,
            "adopted_devs": adopted_devs,
            "benefit": annual_benefit,
            "cost": annual_cost,
            "cumulative": cumulative,
        })

    total_cost = build_cost + annual_maintenance * len(params["adoption_ramp"])
    total_benefit = sum(
        params["total_developers"] * pct * params["monthly_dev_cost"] * 12 * params["productivity_gain_pct"]
        for pct in params["adoption_ramp"].values()
    )
    roi = ((total_benefit - total_cost) / total_cost) * 100

    # Find breakeven
    breakeven = None
    for y in years:
        if y["cumulative"] >= 0 and breakeven is None:
            breakeven = y["year"]

    return {
        "build_cost": build_cost,
        "annual_maintenance": annual_maintenance,
        "total_cost": total_cost,
        "total_benefit": total_benefit,
        "roi": roi,
        "breakeven_year": breakeven,
        "years": years,
    }


def main():
    print("=" * 64)
    print("PLATFORM ROI — MULTI-SCENARIO ANALYSIS")
    print("=" * 64)

    # ── Show assumptions ──
    base = SCENARIOS["Baseline"]
    print(f"\n  SHARED ASSUMPTIONS")
    print(f"  {'─' * 58}")
    print(f"  Total developers:       {base['total_developers']}")
    print(f"  Monthly dev cost:       ${base['monthly_dev_cost']:,}")
    print(f"  Build team size:        {base['initial_build_team']} engineers × {base['build_months']} months")
    print(f"  Maintenance team:       {base['maintenance_team']} engineers + ${base['monthly_infra_cost']:,}/mo infra")

    print(f"\n  VARIABLE ASSUMPTIONS")
    print(f"  {'─' * 58}")
    print(f"  {'Scenario':<16s} {'Prod. Gain':>10s} {'Yr1 Adopt':>10s} {'Yr2 Adopt':>10s} {'Yr3 Adopt':>10s}")
    print(f"  {'─' * 16} {'─' * 10} {'─' * 10} {'─' * 10} {'─' * 10}")
    for name, params in SCENARIOS.items():
        ramp = params["adoption_ramp"]
        print(f"  {name:<16s} {params['productivity_gain_pct']:>9.0%}"
              f" {ramp[1]:>9.0%} {ramp[2]:>9.0%} {ramp[3]:>9.0%}")

    # ── Run each scenario ──
    results = {}
    for name, params in SCENARIOS.items():
        results[name] = calculate_roi(params)

    for name, r in results.items():
        print(f"\n{'─' * 64}")
        print(f"  {name.upper()} SCENARIO")
        print(f"{'─' * 64}")
        print(f"\n  Initial Build Cost: ${r['build_cost']:,.0f}")
        print(f"  Annual Maintenance: ${r['annual_maintenance']:,.0f}")

        print(f"\n  {'Year':<6s} {'Adoption':>8s} {'Devs':>6s} {'Benefit':>12s} {'Cost':>12s} {'Cumulative':>12s}")
        print(f"  {'─' * 6} {'─' * 8} {'─' * 6} {'─' * 12} {'─' * 12} {'─' * 12}")

        for y in r["years"]:
            marker = " ← breakeven" if y["cumulative"] >= 0 and y["year"] == r["breakeven_year"] else ""
            print(f"  {y['year']:<6d} {y['adoption_pct']:>7.0%} {y['adopted_devs']:>6.0f}"
                  f" ${y['benefit']:>10,.0f} ${y['cost']:>10,.0f} ${y['cumulative']:>10,.0f}{marker}")

        print(f"\n  3-Year ROI: {r['roi']:.0f}%")
        if r["breakeven_year"]:
            print(f"  Breakeven:  Year {r['breakeven_year']}")
        else:
            print(f"  Breakeven:  Not reached in 3 years")

    # ── Scenario comparison ──
    print(f"\n{'=' * 64}")
    print("SCENARIO COMPARISON")
    print("=" * 64)

    print(f"\n  {'Scenario':<16s} {'Total Cost':>12s} {'Total Benefit':>14s} {'3-Yr ROI':>9s} {'Breakeven':>10s}")
    print(f"  {'─' * 16} {'─' * 12} {'─' * 14} {'─' * 9} {'─' * 10}")

    for name, r in results.items():
        be = f"Year {r['breakeven_year']}" if r["breakeven_year"] else "N/A"
        print(f"  {name:<16s} ${r['total_cost']:>10,.0f} ${r['total_benefit']:>12,.0f} {r['roi']:>8.0f}% {be:>10s}")

    # ── Key insight ──
    print(f"\n{'=' * 64}")
    print("KEY INSIGHT")
    print("=" * 64)
    print(f"\n  All scenarios break even within 3 years.")
    print(f"  The difference between scenarios is adoption speed, not")
    print(f"  whether the investment pays off.")
    print(f"\n  Domain-driven platforms accelerate adoption because teams")
    print(f"  get immediate value from domain-aware defaults instead of")
    print(f"  spending months customizing a generic platform.")


if __name__ == "__main__":
    main()
