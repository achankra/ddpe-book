# platform_telemetry.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from functools import wraps
import time

tracer = trace.get_tracer("platform.golden-path")
meter = metrics.get_meter("platform.golden-path")

# Define platform-specific metrics
template_instantiations = meter.create_counter(
    "platform.template.instantiations",
    description="Number of template instantiations"
)

onboarding_duration = meter.create_histogram(
    "platform.onboarding.duration",
    description="Time to complete onboarding flow",
    unit="seconds"
)

deviation_requests = meter.create_counter(
    "platform.deviation.requests",
    description="Number of escape hatch requests"
)

def trace_platform_operation(operation_name: str):
    """Decorator for tracing platform operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(operation_name) as span:
                span.set_attribute("platform.layer", "extension")
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("outcome", "success")
                    return result
                except Exception as e:
                    span.set_attribute("outcome", "failure")
                    span.set_attribute("error.type", type(e).__name__)
                    span.record_exception(e)
                    raise
                finally:
                    duration = time.time() - start_time
                    span.set_attribute("duration_seconds", duration)
        return wrapper
    return decorator


if __name__ == "__main__":
    print("=" * 62)
    print("  Platform Telemetry — OpenTelemetry Instrumentation Demo")
    print("=" * 62)

    print("\n  Defined Metrics:")
    print("    Counter   : platform.template.instantiations")
    print("                Tracks how many times templates are used")
    print("    Histogram : platform.onboarding.duration (seconds)")
    print("                Measures time to complete onboarding flows")
    print("    Counter   : platform.deviation.requests")
    print("                Counts escape-hatch deviation requests")

    print("\n  Tracing Decorator: @trace_platform_operation")

    @trace_platform_operation("scaffold_service")
    def scaffold_service(name):
        time.sleep(0.05)
        return f"Scaffolded {name}"

    print("\n  Simulating instrumented operations:")

    result = scaffold_service("order-service")
    print(f"    scaffold_service('order-service') -> '{result}'")
    print(f"      Span: scaffold_service")
    print(f"        platform.layer = extension")
    print(f"        outcome        = success")
    print(f"        duration       ~ 0.05s")

    print("\n  Recording sample metrics:")
    template_instantiations.add(1, {"template": "python-api", "domain": "payments"})
    print("    template_instantiations +1 (python-api, payments)")
    onboarding_duration.record(42.5, {"domain": "payments"})
    print("    onboarding_duration = 42.5s (payments)")
    deviation_requests.add(1, {"type": "custom_database_engine", "tier": "approval"})
    print("    deviation_requests +1 (custom_database_engine)")

    print("\n  In production, metrics export to Prometheus/OTLP collectors.")
    print("\n" + "-" * 62)
    print("  What this looks like in practice:")
    print("    The scaffold_service call above is a traced operation.")
    print("    Each span captures attributes — which platform layer,")
    print("    success or failure, and duration — so you can query")
    print("    traces by domain, layer, or outcome.")
    print()
    print("    In a real setup, this data exports to Prometheus or an")
    print("    OTLP collector. From there you build dashboards like:")
    print("      - Onboarding time by domain (are some domains slower?)")
    print("      - Template usage by team (which golden paths get used?)")
    print("      - Deviation frequency by type (what's missing from")
    print("        the golden path?)")
    print()
    print("    The deviation_requests counter feeds directly into the")
    print("    deviation_analytics.sql query — high deviation counts")
    print("    with high approval rates signal golden path gaps.")
    print("=" * 62)
