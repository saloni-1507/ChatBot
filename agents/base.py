from pydantic import BaseModel

from core.db import get_session
from core.llm import chat_llm
from core.utils import first_missing_field, is_confirmed, merge_fields, with_retry
from schemas.state import Turn

ASK_PROMPT = """You're mid-conversation collecting information from a user. So far you know: \
{known}. You still need to find out: {missing_description}. In ONE short, natural sentence, ask \
the user for that - don't repeat what you already know, and don't sound like a form."""

CONFIRM_PROMPT = """You're about to {destination}. Here's exactly what was collected: {data}. In a \
short, natural sentence or two, summarize this back to the user and ask if it's okay to proceed. \
You MUST mention every value listed - do not omit or change any of them.{extra}"""

SUCCESS_PROMPT = """You just successfully {destination}. Write ONE short, warm, natural sentence \
confirming this to the user.{extra}"""


class FieldCollector:
    """Shared confirm-then-collect-then-submit flow for Lead/Support/Escalation agents."""

    field_questions: dict[str, str]
    destination: str
    fields_cls: type[BaseModel]
    model_cls: type
    llm: object
    extract_prompt: str

    async def extract(self, history: list[Turn], message: str) -> BaseModel:
        full_history = history + [Turn(role="user", content=message)]
        history_text = "\n".join(f"{t.role}: {t.content}" for t in full_history)
        llm = self.llm.with_structured_output(self.fields_cls, method="json_schema")
        prompt = self.extract_prompt.format(history=history_text)
        return await with_retry(lambda: llm.ainvoke(prompt))

    async def submit(self, thread_id: str, fields: BaseModel) -> None:
        async for session in get_session():
            session.add(self.model_cls(thread_id=thread_id, **fields.model_dump()))
            await session.commit()
            break

    def extra_context(self, fields: BaseModel) -> str:
        """Optional hook: extra instruction appended to confirm/success prompts (e.g. severity note)."""
        return ""

    def _known(self, fields: BaseModel) -> dict:
        return {k: v for k, v in fields.model_dump().items() if v is not None}

    async def ask_for(self, fields: BaseModel, missing: str) -> str:
        prompt = ASK_PROMPT.format(known=self._known(fields), missing_description=self.field_questions[missing])
        response = await with_retry(lambda: chat_llm.ainvoke(prompt))
        return response.content

    async def confirm_prompt(self, fields: BaseModel) -> str:
        prompt = CONFIRM_PROMPT.format(
            destination=self.destination, data=self._known(fields), extra=self.extra_context(fields)
        )
        response = await with_retry(lambda: chat_llm.ainvoke(prompt))
        return response.content

    async def success_message(self, fields: BaseModel) -> str:
        prompt = SUCCESS_PROMPT.format(destination=self.destination, extra=self.extra_context(fields))
        response = await with_retry(lambda: chat_llm.ainvoke(prompt))
        return response.content

    async def try_confirm(self, thread_id: str, fields: BaseModel, message: str) -> str | None:
        if await is_confirmed(message):
            await self.submit(thread_id, fields)
            return await self.success_message(fields)
        return None

    async def collect(
        self, thread_id: str, fields: BaseModel, history: list[Turn], message: str
    ) -> tuple[BaseModel, bool, str, bool]:
        fields = merge_fields(fields, await self.extract(history, message))
        missing = first_missing_field(fields)
        if missing:
            return fields, False, await self.ask_for(fields, missing), False
        return fields, True, await self.confirm_prompt(fields), False

    async def process(
        self, thread_id: str, fields: BaseModel, pending_confirmation: bool, history: list[Turn], message: str
    ) -> tuple[BaseModel, bool, str, bool]:
        """Returns (updated_fields, updated_pending_confirmation, reply, submitted)."""
        if pending_confirmation:
            reply = await self.try_confirm(thread_id, fields, message)
            if reply:
                return fields, False, reply, True

        return await self.collect(thread_id, fields, history, message)