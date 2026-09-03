import json

from core.llm import guard_llm, prompt_guard_llm
from schemas.safety import ModerationVerdict

INJECTION_THRESHOLD = 0.5


class Prompts:
    MODERATION = """Instructions: Classify the user's message for serious safety concerns - \
self-harm, violence, or genuine emotional distress - so it can be routed to a human. This is \
not general content moderation; only flag messages a human should see urgently.

Definitions: "Self-harm" is expressed intent or ideation of harming oneself. "Violence" is \
expressed intent to harm others. "Distress" is clear signs of crisis or hopelessness.

Criteria: Flag (violation=true) only if the message itself expresses one of the above. Do not \
flag academic questions about these topics, or incidental mentions in an unrelated context.

Examples:
- "I don't see the point in anything anymore" -> violation=true, category="distress"
- "What's your refund policy?" -> violation=false, category=null

Respond with ONLY a JSON object: {"violation": bool, "category": str or null, "rationale": str}."""


async def check_injection(message: str) -> bool:
    result = await prompt_guard_llm.ainvoke(message)
    return float(result.content) > INJECTION_THRESHOLD


async def check_content(message: str) -> ModerationVerdict:
    result = await guard_llm.ainvoke(f"{Prompts.MODERATION}\n\nMessage: {message}")
    return ModerationVerdict.model_validate(json.loads(result.content))