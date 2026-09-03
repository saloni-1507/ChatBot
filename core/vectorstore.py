from pinecone import Pinecone

from core.config import settings

_pc = Pinecone(api_key=settings.pinecone_api_key)
index = _pc.Index(settings.pinecone_index)


def search(namespace: str, query_text: str) -> list[dict]:
    result = index.search_records(
        namespace=namespace,
        query={"inputs": {"text": query_text}, "top_k": settings.retrieval_top_k},
    )
    return result["result"]["hits"][: settings.retrieval_top_n]