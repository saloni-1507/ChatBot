from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from agents.base import FieldCollector
from core import react_json_agent
from core.llm import chat_llm, vision_llm
from core.utils import json_shape_example
from core.vectorstore import search
from models import Case
from schemas.state import CaseFields, Turn
from schemas.support import SupportResolution

_EXAMPLE = json_shape_example(SupportResolution)


class Prompts:
    SYSTEM = f"""You resolve Aurora support issues using ONLY the search_support_kb tool - \
never answer from your own knowledge. Call it with the user's issue; if the results don't clearly \
resolve it, call it again with a differently-phrased query (up to 3 attempts total) before giving \
up. Only answer if a result explicitly addresses the user's exact symptom - a result that is only \
generally related, or covers a different cause of a superficially similar problem, does not \
count. Once you have your answer (or have given up), respond with ONLY a JSON object in this \
exact shape: {_EXAMPLE}. Set resolved=false if nothing explicitly matched after trying - do not \
force-fit the closest available result - otherwise resolved=true and give the fix concisely."""

    EXTRACT = """Extract support-case details from the full conversation below. Only fill a \
field if the user has actually stated it - leave it null if not mentioned, do not guess. Set \
severity to one of "low", "medium", "high", or "critical" based on urgency: "critical" for \
production down/data loss/security issues, "high" for a broken feature with no workaround, \
"medium" for a broken feature with a workaround, "low" for a minor/cosmetic issue.

Conversation:
{history}"""

    FIELD_QUESTIONS = {
        "issue_summary": "a one-sentence summary of the issue",
        "feature": "which feature or area is affected",
        "repro_steps": "what steps lead to this happening",
        "email": "the best email to reach them at",
    }


@tool
def search_support_kb(query: str) -> str:
    """Search Aurora's support knowledge base for a fix relevant to the query."""
    hits = search("support", query)
    if not hits:
        return "No results found."
    return "\n\n".join(f"[{h['fields']['section']}] {h['fields']['content']}" for h in hits)


_react_agent = react_json_agent.build(search_support_kb, Prompts.SYSTEM)


async def describe_screenshot(image_b64: str) -> str:
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Describe any error message or broken UI state visible in this screenshot."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
        ]
    )
    response = await vision_llm.ainvoke([message])
    return response.content


async def augment_with_screenshot(message: str, image_b64: str | None) -> str:
    if not image_b64:
        return message
    description = await describe_screenshot(image_b64)
    return f"{message}\n\nScreenshot shows: {description}"


async def try_resolve(history: list[Turn], message: str) -> str | None:
    resolution = await react_json_agent.run(_react_agent, SupportResolution, history, message)
    return resolution.answer if resolution.resolved else None


class SupportAgent(FieldCollector):
    field_questions = Prompts.FIELD_QUESTIONS
    destination = "log this as a support case"
    fields_cls = CaseFields
    model_cls = Case
    llm = chat_llm
    extract_prompt = Prompts.EXTRACT

    def extra_context(self, case: CaseFields) -> str:
        if case.severity in ("high", "critical"):
            return f" Mention this was marked {case.severity} severity."
        return ""

    async def process(
        self,
        thread_id: str,
        case: CaseFields,
        pending_confirmation: bool,
        history: list[Turn],
        message: str,
        image_b64: str | None = None,
        kb_attempted: bool = False,
    ) -> tuple[CaseFields, bool, str, bool, bool]:
        """Returns (updated_case, updated_pending_confirmation, reply, submitted, kb_attempted)."""
        if not pending_confirmation:
            message = await augment_with_screenshot(message, image_b64)

        if not pending_confirmation and not kb_attempted:
            resolved = await try_resolve(history, message)
            kb_attempted = True
            if resolved:
                return case, False, resolved, False, kb_attempted

        case, confirmation, reply, submitted = await super().process(
            thread_id, case, pending_confirmation, history, message
        )
        return case, confirmation, reply, submitted, False if submitted else kb_attempted


_agent = SupportAgent()
process = _agent.process