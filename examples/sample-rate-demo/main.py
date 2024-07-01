from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.status import Status, StatusCode
import time

# Configure the tracer provider and exporter
trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

tracer = trace.get_tracer(__name__)

# Helper function to create spans
def create_spans(trace_name, error=False, high_latency=False):
    with tracer.start_as_current_span(trace_name) as trace_span:
        for i in range(5):
            with tracer.start_as_current_span(f"span_{i}") as span:
                if error and i == 2:
                    span.set_status(Status(StatusCode.ERROR, "Simulated error"))
                if high_latency and i == 2:
                    time.sleep(2)  # Simulate high latency

# Create a trace with an error
create_spans("error_trace", error=True)

# Create a trace with high latency
create_spans("high_latency_trace", high_latency=True)

# Create a regular health trace
create_spans("regular_health_trace")

