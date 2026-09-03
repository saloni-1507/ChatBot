from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph

from agents.escalation import process as escalation_process
from agents.fallback import respond as fallback_respond
from agents.knowledge import answer as knowledge_answer
from agents.lead import process as lead_process
from agents.router import classify
from agents.safety import check_content, check_injection
from agents.support import process as support_process
from core.config import settings
from schemas.state import CaseFields, EscalationFields, LeadFields, SessionState, Turn

REFUSAL = "I can't help with that request."


def active_hint(state: SessionState) -> str | None:
    """Ground-truth state for the router to disambiguate against, never a hard bypass."""
    hints = []
    if state.image_b64:
        hints.append("The user attached a screenshot with this message, which usually means a technical support issue.")
    if state.lead_confirmation or state.lead != LeadFields():
        hints.append(f"lead_agent has an unfinished sales-lead collection - collected so far: {state.lead.model_dump()}")
    elif state.case_confirmation or state.case != CaseFields():
        hints.append(f"support_agent has an unfinished support case - collected so far: {state.case.model_dump()}")
    elif state.escalation_confirmation or state.escalation != EscalationFields():
        hints.append(
            f"escalation_agent has an unfinished escalation - collected so far: {state.escalation.model_dump()}"
        )
    return " ".join(hints) or None


async def safety_node(state: SessionState) -> dict:
    if await check_injection(state.message):
        return {"injection_flagged": True}
    verdict = await check_content(state.message)
    return {"moderation_violation": verdict.violation}


def route_after_safety(state: SessionState) -> str:
    if state.injection_flagged:
        return "refuse"
    if state.moderation_violation:
        return "escalation_agent"
    return "router"


def refuse_node(state: SessionState) -> dict:
    return {"reply": REFUSAL}


async def router_node(state: SessionState) -> dict:
    try:
        decision = await classify(state.history, state.message, active_hint(state))
        return {"route": decision.route, "route_reason": decision.reason}
    except Exception:
        return {"route": "escalation_agent", "route_reason": "Router failed to classify this message."}


def route_after_router(state: SessionState) -> str:
    return state.route


async def fallback_node(state: SessionState) -> dict:
    return {"reply": await fallback_respond(state.message)}


async def knowledge_node(state: SessionState) -> dict:
    result = await knowledge_answer(state.history, state.message)
    return {"reply": result.answer}


async def lead_node(state: SessionState) -> dict:
    lead, confirmation, reply, submitted = await lead_process(
        state.thread_id, state.lead, state.lead_confirmation, state.history, state.message
    )
    return {"lead": LeadFields() if submitted else lead, "lead_confirmation": confirmation, "reply": reply}


async def support_node(state: SessionState) -> dict:
    case, confirmation, reply, submitted, kb_attempted = await support_process(
        state.thread_id,
        state.case,
        state.case_confirmation,
        state.history,
        state.message,
        image_b64=state.image_b64,
        kb_attempted=state.case_kb_attempted,
    )
    return {
        "case": CaseFields() if submitted else case,
        "case_confirmation": confirmation,
        "case_kb_attempted": kb_attempted,
        "reply": reply,
    }


async def escalation_node(state: SessionState) -> dict:
    trigger_reason = state.message if state.moderation_violation else state.route_reason
    info, confirmation, reply, submitted = await escalation_process(
        state.thread_id,
        state.escalation,
        state.escalation_confirmation,
        state.history,
        state.message,
        trigger_reason=trigger_reason,
    )
    return {
        "escalation": EscalationFields() if submitted else info,
        "escalation_confirmation": confirmation,
        "reply": reply,
    }


def finalize_node(state: SessionState) -> dict:
    new_history = state.history + [
        Turn(role="user", content=state.message),
        Turn(role="assistant", content=state.reply),
    ]
    new_history = new_history[-settings.recent_turns :]
    return {
        "history": new_history,
        "message": "",
        "image_b64": None,
        "route": None,
        "route_reason": None,
        "injection_flagged": False,
        "moderation_violation": False,
    }


def build_graph():
    builder = StateGraph(SessionState)
    builder.add_node("safety", safety_node)
    builder.add_node("refuse", refuse_node)
    builder.add_node("router", router_node)
    builder.add_node("fallback", fallback_node)
    builder.add_node("knowledge_agent", knowledge_node)
    builder.add_node("lead_agent", lead_node)
    builder.add_node("support_agent", support_node)
    builder.add_node("escalation_agent", escalation_node)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "safety")
    builder.add_conditional_edges("safety", route_after_safety)
    builder.add_conditional_edges("router", route_after_router)
    for node in ("refuse", "fallback", "knowledge_agent", "lead_agent", "support_agent", "escalation_agent"):
        builder.add_edge(node, "finalize")
    builder.add_edge("finalize", END)

    serde = JsonPlusSerializer(
        allowed_msgpack_modules=[
            ("schemas.state", "Turn"),
            ("schemas.state", "LeadFields"),
            ("schemas.state", "CaseFields"),
            ("schemas.state", "EscalationFields"),
        ]
    )
    return builder.compile(checkpointer=InMemorySaver(serde=serde))


graph = build_graph()