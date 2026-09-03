import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_text_splitters import (  # noqa: E402
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from pinecone import Pinecone  # noqa: E402

from core.config import settings  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DOCS = {
    "knowledge": ROOT / "public/docs/knowledge_docs.md",
    "support": ROOT / "public/docs/support_docs.md",
}
HEADERS_TO_SPLIT_ON = [("#", "h1"), ("##", "h2")]
MAX_CHUNK_CHARS = 800
CHUNK_OVERLAP = 100


def ensure_index(pc: Pinecone) -> None:
    if settings.pinecone_index not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index_for_model(
            name=settings.pinecone_index,
            cloud=settings.pinecone_cloud,
            region=settings.pinecone_region,
            embed={"model": settings.embed_model, "field_map": {"text": "text"}},
        )


def chunk_doc(path: Path) -> list[dict]:
    text = path.read_text()
    header_splitter = MarkdownHeaderTextSplitter(HEADERS_TO_SPLIT_ON)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_CHARS, chunk_overlap=CHUNK_OVERLAP
    )
    sections = header_splitter.split_text(text)

    records = []
    i = 0
    for section_doc in sections:
        section = section_doc.metadata.get("h2") or section_doc.metadata.get("h1") or "General"
        for piece in char_splitter.split_text(section_doc.page_content):
            records.append(
                {
                    "_id": f"{path.stem}-{i}",
                    "text": f"{section}: {piece}",
                    "content": piece,
                    "section": section,
                }
            )
            i += 1
    return records


def main() -> None:
    pc = Pinecone(api_key=settings.pinecone_api_key)
    ensure_index(pc)
    index = pc.Index(settings.pinecone_index)

    for namespace, path in DOCS.items():
        records = chunk_doc(path)
        index.upsert_records(namespace=namespace, records=records)
        print(f"upserted {len(records)} chunks into namespace '{namespace}'")


if __name__ == "__main__":
    main()