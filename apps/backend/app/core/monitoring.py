from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import time

# Custom metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

active_users = Gauge(
    "active_users",
    "Number of active users"
)

def setup_monitoring(app):
    # Initialize the instrumentator
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )

    # Add custom metrics
    instrumentator.add(metrics.default())
    instrumentator.add(metrics.latency())
    instrumentator.add(metrics.requests())
    instrumentator.add(metrics.responses())
    instrumentator.add(metrics.requests_inprogress())

    # Add business metrics
    @instrumentator.instrument()
    def business_metrics(info: Info) -> None:
        # Add your custom business metrics here
        pass

    # Initialize the instrumentator
    instrumentator.instrument(app).expose(app) 