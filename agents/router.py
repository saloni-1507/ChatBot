from core.llm import chat_llm
from core.utils import with_retry
from schemas.state import RouterDecision, Turn


class Prompts:
    SYSTEM = """You route incoming support-chat messages to exactly one destination, \
using the full conversation history below plus the latest message.

Routes:
- fallback: greeting/small talk, an ambiguous message, or a multi-part message. Reply asking \
the user to clarify or split it - do not guess.
- knowledge_agent: a product/docs question.
- lead_agent: a sales lead (team size, current tool, use case, timeline, buying interest).
- support_agent: a technical support or account/billing issue.
- escalation_agent: choose this directly, overriding the above, if the history shows either \
(a) repeated negative/frustrated sentiment across turns, or (b) the same question asked and \
left unanswered multiple times in a row.

If told below that a destination has an in-progress, unfinished collection, and the latest message \
looks like it's answering or continuing that - even a short or ambiguous-looking reply - route \
back to that same destination rather than reclassifying it fresh. Only pick a different \
destination if the latest message clearly introduces a new, unrelated topic instead.

If told below that a screenshot was attached, prefer support_agent over fallback even if the \
accompanying text alone is terse or vague (e.g. "solve", "please help") - the screenshot is the \
actual content of the request.
"""


async def classify(history: list[Turn], message: str, active_hint: str | None = None) -> RouterDecision:
    history_text = "\n".join(f"{t.role}: {t.content}" for t in history) or "(none)"
    hint_text = f"\n\nIn progress: {active_hint}" if active_hint else ""
    prompt = f"{Prompts.SYSTEM}{hint_text}\n\nHistory:\n{history_text}\n\nLatest message: {message}"
    llm = chat_llm.with_structured_output(RouterDecision, method="json_schema")
    return await with_retry(lambda: llm.ainvoke(prompt))