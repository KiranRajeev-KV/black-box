import logging
from typing import TYPE_CHECKING

from rag_basics.logging_config import setup_logging
from rag_basics.models import Document

if TYPE_CHECKING:
    import tiktoken

logger = logging.getLogger(__name__)

_ENCODING: "tiktoken.Encoding | None" = None


def _get_encoding() -> "tiktoken.Encoding":
    global _ENCODING
    if _ENCODING is None:
        import tiktoken  # lazy: deferred to first chunk call, cached in module

        _ENCODING = tiktoken.get_encoding("o200k_base")
    return _ENCODING


def chunk_document(doc: Document, chunk_size: int = 512) -> list[Document]:
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be > 0, got {chunk_size}")

    encoding = _get_encoding()
    token_ids = encoding.encode(doc.text)
    total_tokens = len(token_ids)

    if total_tokens == 0:
        return []

    chunks: list[Document] = []
    char_offset = 0
    chunk_count = (total_tokens + chunk_size - 1) // chunk_size

    for chunk_index in range(0, total_tokens, chunk_size):
        end = min(chunk_index + chunk_size, total_tokens)
        segment = token_ids[chunk_index:end]
        chunk_text = encoding.decode(segment)

        parent_id = doc.metadata.get("doc_id", "unknown")
        metadata = {
            "filename": doc.metadata.get("filename", ""),
            "source_path": doc.metadata.get("source_path", ""),
            "doc_id": f"{parent_id}_chunk_{chunk_index // chunk_size}",
            "chunk_index": chunk_index // chunk_size,
            "chunk_count": chunk_count,
            "char_offset": char_offset,
        }
        char_offset += len(chunk_text)

        chunks.append(Document(text=chunk_text, metadata=metadata))

    logger.debug(
        "Chunked '%s' into %d chunks (tokens: %d, chunk_size: %d)",
        doc.metadata.get("filename", "?"),
        chunk_count,
        total_tokens,
        chunk_size,
    )
    return chunks


def chunk_documents(docs: list[Document], chunk_size: int = 512) -> list[Document]:
    all_chunks: list[Document] = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc, chunk_size))
    return all_chunks


def main() -> None:
    setup_logging()
    from rag_basics.loader import load_documents

    docs = load_documents("data")
    chunks = chunk_documents(docs)
    total_chunks = len(chunks)
    total_tokens = sum(len(_get_encoding().encode(c.text)) for c in chunks)

    # for chunk in chunks[:5]:
    #     c = chunk.metadata
    #     text_preview = chunk.text[:80].replace("\n", " ")
    logger.info("Total: %d chunks, ~%d tokens", total_chunks, total_tokens)


if __name__ == "__main__":
    main()
