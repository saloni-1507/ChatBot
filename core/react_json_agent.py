import json

from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from core.llm import chat_llm
from core.utils import with_retry
from schemas.state import Turn


def build(tool, prompt: str):
    return create_react_agent(chat_llm, tools=[tool], prompt=prompt)


async def run(agent, schema_cls: type[BaseModel], history: list[Turn], message: str) -> BaseModel:
    messages = [{"role": t.role, "content": t.content} for t in history]
    messages.append({"role": "user", "content": message})

    async def call():
        result = await agent.ainvoke({"messages": messages})
        final = result["messages"][-1].content
        return schema_cls.model_validate(json.loads(final))

    return await with_retry(call)