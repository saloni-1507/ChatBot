from langchain_core.tools import tool

from core import react_json_agent
from core.utils import json_shape_example
from core.vectorstore import search
from schemas.knowledge import KnowledgeAnswer
from schemas.state import Turn

_EXAMPLE = json_shape_example(KnowledgeAnswer)


class Prompts:
    SYSTEM = f"""You answer questions about Aurora's product using ONLY the search_kb tool - \
never answer from your own knowledge. Call search_kb with the user's question; if the results \
don't clearly answer it, call it again with a differently-phrased query (up to 3 attempts total) \
before giving up. Once you have your answer (or have given up), respond with ONLY a JSON object \
in this exact shape: {_EXAMPLE}. Set low_confidence=true if you couldn't find a clear answer \
after trying, otherwise false and give a concise answer mentioning which section it came from."""


@tool
def search_kb(query: str) -> str:
    """Search Aurora's product knowledge base for information relevant to the query."""
    hits = search("knowledge", query)
    if not hits:
        return "No results found."
    return "\n\n".join(f"[{h['fields']['section']}] {h['fields']['content']}" for h in hits)


_agent = react_json_agent.build(search_kb, Prompts.SYSTEM)


async def answer(history: list[Turn], message: str) -> KnowledgeAnswer:
    return await react_json_agent.run(_agent, KnowledgeAnswer, history, message)