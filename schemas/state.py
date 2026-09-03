from typing import Literal

from pydantic import BaseModel, EmailStr

Route = Literal["fallback", "knowledge_agent", "lead_agent", "support_agent", "escalation_agent"]


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class RouterDecision(BaseModel):
    route: Route
    reason: str


class LeadFields(BaseModel):
    company_size: int | None = None
    current_tool: str | None = None
    use_case: str | None = None
    timeline: str | None = None
    email: EmailStr | None = None


class CaseFields(BaseModel):
    issue_summary: str | None = None
    feature: str | None = None
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    repro_steps: str | None = None
    email: EmailStr | None = None


class EscalationFields(BaseModel):
    reason: str | None = None
    email: EmailStr | None = None


class SessionState(BaseModel):
    # identity + this turn's input/output
    thread_id: str
    history: list[Turn] = []
    message: str = ""
    image_b64: str | None = None
    reply: str = ""

    # safety + routing (all reset per turn in finalize_node)
    injection_flagged: bool = False
    moderation_violation: bool = False
    route: Route | None = None
    route_reason: str | None = None

    # per-agent collection state (persists across turns until submitted)
    lead: LeadFields = LeadFields()
    lead_confirmation: bool = False
    case: CaseFields = CaseFields()
    case_confirmation: bool = False
    case_kb_attempted: bool = False
    escalation: EscalationFields = EscalationFields()
    escalation_confirmation: bool = False