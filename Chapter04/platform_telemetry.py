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
