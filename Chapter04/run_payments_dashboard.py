# run_payments_dashboard.py
# Python visualizer for payments_dashboard.yaml
# Reads the YAML dashboard definition and renders each panel
# with simulated payments domain data.

import yaml
import os
import random

random.seed(42)


def load_dashboard():
    """Read payments_dashboard.yaml from the same directory."""
    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payments_dashboard.yaml")
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def render_gauge(panel):
    """Render a gauge panel with thresholds."""
    value = round(random.uniform(98.8, 99.9), 2)
    thresholds = panel["thresholds"]
    color = "red"
    for t in sorted(thresholds, key=lambda x: x["value"], reverse=True):
        if value >= t["value"]:
            color = t["color"]
            break
    bar_width = int(value / 2)
    bar_char = "#" if color == "green" else ("~" if color == "yellow" else "!")
    bar = bar_char * bar_width
    print(f"    Value: {value}%  [{color.upper()}]")
    print(f"    [{bar:<50}] {value}%")
    print(f"    Thresholds: >=99.5 GREEN | >=99.0 YELLOW | <99.0 RED")


def render_timeseries(panel):
    """Render a time-series panel as a sparkline."""
    unit = panel.get("unit", "")
    hours = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    values = [round(random.uniform(1.2, 4.8), 2) for _ in hours]

    max_val = max(values)
    min_val = min(values)
    chart_height = 8
    print(f"    P95 Settlement Latency (last 24h, {unit})")
    print()

    for row in range(chart_height, 0, -1):
        threshold = min_val + (max_val - min_val) * (row / chart_height)
        label = f"{threshold:>5.1f}s" if row % 2 == 0 else "      "
        line = label + " |"
        for v in values:
            normalized = (v - min_val) / (max_val - min_val) * chart_height
            if normalized >= row:
                line += "  ## "
            else:
                line += "     "
        print(line)
    print("        +" + "-----" * len(hours))
    print("         " + "  ".join(hours))


def render_piechart(panel):
    """Render a pie chart as a horizontal breakdown."""
    types = {
        "credit_card": random.randint(35000, 50000),
        "debit_card": random.randint(20000, 35000),
        "bank_transfer": random.randint(10000, 20000),
        "digital_wallet": random.randint(8000, 15000),
        "crypto": random.randint(500, 3000),
    }
    total = sum(types.values())

    sorted_types = sorted(types.items(), key=lambda x: x[1], reverse=True)
    bar_total = 40

    for txn_type, count in sorted_types:
        pct = count / total * 100
        bar_len = int(pct / 100 * bar_total)
        bar = "#" * bar_len
        print(f"    {txn_type:<18} {bar:<40} {count:>6} ({pct:>5.1f}%)")

    print(f"    {'':18} {'':40} {total:>6} total")


def render_table(panel):
    """Render a table panel with error rates by payment method."""
    methods = {
        "credit_card": round(random.uniform(0.1, 0.8), 2),
        "debit_card": round(random.uniform(0.2, 1.2), 2),
        "bank_transfer": round(random.uniform(0.5, 2.5), 2),
        "digital_wallet": round(random.uniform(0.1, 0.6), 2),
        "crypto": round(random.uniform(1.0, 4.0), 2),
    }

    print(f"    {'Payment Method':<20} {'Error Rate':>10}  Status")
    print(f"    {'-'*20} {'-'*10}  {'-'*12}")

    for method, rate in sorted(methods.items(), key=lambda x: x[1], reverse=True):
        status = "CRITICAL" if rate > 1.0 else ("WARNING" if rate > 0.5 else "OK")
        indicator = "!!!" if status == "CRITICAL" else (" ! " if status == "WARNING" else "   ")
        print(f"    {method:<20} {rate:>9.2f}%  {status} {indicator}")


def render_alerts(alerts):
    """Render alert rules."""
    print("  Alert Rules:")
    for alert in alerts:
        print(f"    [{alert['severity'].upper():<8}] {alert['name']}")
        print(f"              Condition: {alert['condition']}")
        print(f"              Runbook:   {alert['runbook']}")


RENDERERS = {
    "gauge": render_gauge,
    "timeseries": render_timeseries,
    "piechart": render_piechart,
    "table": render_table,
}


if __name__ == "__main__":
    dashboard = load_dashboard()
    meta = dashboard["metadata"]
    spec = dashboard["spec"]

    print("=" * 70)
    print(f"  Domain Dashboard: {meta['name']}  (domain: {meta['domain']})")
    print(f"  Refresh: {spec['refresh']}  |  Time Range: {spec['timeRange']}")
    print("=" * 70)

    for panel in spec["panels"]:
        print(f"\n  [{panel['type'].upper()}] {panel['name']}")
        print(f"  Query: {panel['query'].strip()[:70]}...")
        print()

        renderer = RENDERERS.get(panel["type"])
        if renderer:
            renderer(panel)
        else:
            print(f"    (No renderer for type '{panel['type']}')")

    print()
    print("-" * 70)
    render_alerts(spec["alerts"])

    print()
    print("-" * 70)
    print("  This dashboard is defined in payments_dashboard.yaml.")
    print("  In production, apply it to Grafana via a custom CRD controller")
    print("  or import the queries directly into Grafana/Datadog/New Relic.")
    print("  The key point: observability is domain-aware. These panels")
    print("  track payments-specific signals (settlement latency, error")
    print("  rate by payment method) not generic infrastructure metrics.")
    print("=" * 70)
