from agents.base import FieldCollector
from core.llm import chat_llm
from models import Escalation
from schemas.state import EscalationFields, Turn


class Prompts:
    EXTRACT = """Extract escalation details from the full conversation below. Only fill a \
field if the user has actually stated it - leave it null if not mentioned, do not guess.

Conversation:
{history}"""

    FIELD_QUESTIONS = {
        "reason": "what's going on that they need help with - ask gently, they may be upset",
        "email": "the best email for the team to follow up at",
    }


class EscalationAgent(FieldCollector):
    field_questions = Prompts.FIELD_QUESTIONS
    destination = "flag this for our team to follow up on"
    fields_cls = EscalationFields
    model_cls = Escalation
    llm = chat_llm
    extract_prompt = Prompts.EXTRACT

    async def process(
        self,
        thread_id: str,
        info: EscalationFields,
        pending_confirmation: bool,
        history: list[Turn],
        message: str,
        trigger_reason: str | None = None,
    ) -> tuple[EscalationFields, bool, str, bool]:
        if not pending_confirmation and trigger_reason and info.reason is None:
            info = EscalationFields(reason=trigger_reason, email=info.email)
        return await super().process(thread_id, info, pending_confirmation, history, message)


_agent = EscalationAgent()
process = _agent.process