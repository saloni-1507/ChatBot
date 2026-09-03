from langchain_groq import ChatGroq

from core.config import settings

chat_llm = ChatGroq(model="openai/gpt-oss-20b", api_key=settings.groq_api_key)
vision_llm = ChatGroq(
    model="qwen/qwen3.6-27b", api_key=settings.groq_api_key, reasoning_effort="none"
)
guard_llm = ChatGroq(model="openai/gpt-oss-safeguard-20b", api_key=settings.groq_api_key)
# narrow injection/jailbreak detector, separate from guard_llm's general moderation
prompt_guard_llm = ChatGroq(
    model="meta-llama/llama-prompt-guard-2-22m", api_key=settings.groq_api_key
)