import logging
from pathlib import Path

from rag_basics.logging_config import setup_logging
from rag_basics.models import Document

logger = logging.getLogger(__name__)


def load_documents(path: str | Path) -> list[Document]:
    data_dir = Path(path)

    if not data_dir.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {data_dir}")

    md_files = sorted(data_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"No .md files found in {data_dir}")

    logger.info("Scanning directory: %s", data_dir)
    documents: list[Document] = []
    for filepath in md_files:
        try:
            doc = load_document(filepath)
        except (ValueError, UnicodeDecodeError) as exc:
            logger.warning("Skipping %s: %s", filepath.name, exc)
            continue
        documents.append(doc)

    logger.info("Loaded %d documents", len(documents))
    return documents


def load_document(filepath: str | Path) -> Document:
    path = Path(filepath)

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        logger.warning("Skipping empty file: %s", path.name)
        raise ValueError(f"File is empty: {path}")

    metadata = {
        "filename": path.name,
        "source_path": str(path.resolve()),
        "doc_id": path.stem,
        "char_count": len(text),
    }

    logger.debug("Loaded: %s (%d chars)", path.name, len(text))
    return Document(text=text, metadata=metadata)


def main() -> None:
    setup_logging()
    docs = load_documents("data")
    # for doc in docs:
    #     print(f"  [{doc.metadata['doc_id']}] {doc.metadata['filename']}  ({doc.metadata['char_count']} chars)")


if __name__ == "__main__":
    main()
