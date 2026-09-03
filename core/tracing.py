import os
import time

import opik
from opik.integrations.langchain import OpikTracer

from core.config import settings
from core.pii import redact_nested

os.environ["OPIK_API_KEY"] = settings.opik_api_key
os.environ["OPIK_WORKSPACE"] = settings.opik_workspace

PROJECT_NAME = "aurora-saas-assistant"
_client = opik.Opik()


def get_tracer(thread_id: str) -> OpikTracer:
    return OpikTracer(project_name=PROJECT_NAME, thread_id=thread_id)


def redact_traces(tracer: OpikTracer) -> None:
    tracer.flush()
    for trace in tracer.created_traces():
        content = None
        for _ in range(5):
            try:
                content = _client.get_trace_content(trace.id)
                break
            except Exception:
                time.sleep(1)
        if content is None:
            continue
        _client.trace(
            id=trace.id,
            project_name=PROJECT_NAME,
            name=content.name,
            start_time=content.start_time,
            end_time=content.end_time,
            thread_id=content.thread_id,
            metadata=content.metadata,
            tags=content.tags,
            input=redact_nested(content.input),
            output=redact_nested(content.output),
        )