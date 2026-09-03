from core.llm import chat_llm


class Prompts:
    RESPOND = "You are Aurora's assistant. The user's message doesn't clearly fit a specific \
category (greeting/small talk, ambiguous, or multiple questions at once). Respond naturally - if \
it's a greeting, greet back and ask how you can help; if it's ambiguous or multi-part, ask them \
to clarify or ask one thing at a time. Message: {message}"


async def respond(message: str) -> str:
    response = await chat_llm.ainvoke(Prompts.RESPOND.format(message=message))
    return response.content