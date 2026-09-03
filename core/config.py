from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    port: int
    groq_api_key: str
    jwt_secret: str
    database_url: str
    pinecone_api_key: str
    pinecone_index: str
    opik_api_key: str
    opik_workspace: str

    session_ttl_seconds: int = 3600
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    embed_model: str = "llama-text-embed-v2"
    rerank_model: str = "pinecone-rerank-v0"
    retrieval_top_k: int = 10
    retrieval_top_n: int = 2
    recent_turns: int = 10


settings = Settings()