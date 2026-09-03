import asyncio
from contextlib import asynccontextmanager

import jwt
from fastapi import FastAPI, Header

from agents.graph import graph
from core.auth import create_session_token, decode_session_token
from core.db import init_db
from core.tracing import get_tracer, redact_traces
from schemas.chat import ChatRequest, ChatResponse
from schemas.state import SessionState


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="aurora-chat-api", lifespan=lifespan)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest, authorization: str | None = Header(None)) -> ChatResponse:
    token = authorization.removeprefix("Bearer ") if authorization else None
    try:
        thread_id = decode_session_token(token).thread_id if token else None
    except jwt.PyJWTError:
        thread_id = None

    if thread_id is None:
        token = create_session_token()
        thread_id = decode_session_token(token).thread_id

    tracer = get_tracer(thread_id)
    config = {"configurable": {"thread_id": thread_id}, "callbacks": [tracer]}
    existing = await graph.aget_state(config)
    update = {"message": request.message, "image_b64": request.image_b64}
    if existing.values:
        result = await graph.ainvoke(update, config)
    else:
        result = await graph.ainvoke(SessionState(thread_id=thread_id, **update), config)

    asyncio.create_task(asyncio.to_thread(redact_traces, tracer))
    return ChatResponse(reply=result["reply"], token=token)