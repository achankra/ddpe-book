# platform_roi.py
"""Platform Value Model — ROI Calculator"""

def calculate_platform_roi(
    monthly_dev_cost: float = 15000,
    total_developers: int = 500,
    productivity_gain_pct: float = 0.10,  # Conservative 10%
    initial_build_team: int = 10,
    build_months: int = 12,
    maintenance_team: int = 5,
    monthly_infra_cost: float = 50000,
    adoption_ramp: dict = None  # year -> % of devs adopted
):
    if adoption_ramp is None:
        adoption_ramp = {1: 0.10, 2: 0.30, 3: 0.60}

    build_cost = initial_build_team * monthly_dev_cost * build_months
    annual_maintenance = (maintenance_team * monthly_dev_cost + monthly_infra_cost) * 12

    print("=== Platform ROI Analysis ===")
    cumulative = -build_cost  # Initial investment
    print(f"Initial Build Cost: ${build_cost:,.0f}")

    for year, adoption_pct in adoption_ramp.items():
        adopted_devs = total_developers * adoption_pct
        annual_benefit = adopted_devs * monthly_dev_cost * 12 * productivity_gain_pct
        annual_cost = annual_maintenance
        if year == 1:
            annual_cost += build_cost
        cumulative += annual_benefit - (annual_maintenance if year > 1 else 0)
        print(f"Year {year}: Cost=${annual_cost:,.0f} | "
              f"Benefit=${annual_benefit:,.0f} | "
              f"Cumulative=${cumulative:,.0f}")

    total_cost = build_cost + annual_maintenance * len(adoption_ramp)
    total_benefit = sum(
        total_developers * pct * monthly_dev_cost * 12 * productivity_gain_pct
        for pct in adoption_ramp.values()
    )
    roi = ((total_benefit - total_cost) / total_cost) * 100
    print(f"→ 3-Year ROI: {roi:.0f}%")

calculate_platform_roi()
