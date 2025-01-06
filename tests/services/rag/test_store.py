import tempfile
from pathlib import Path

from langchain_core.documents import Document

from src.services.rag.processor import process_document
from src.services.rag.store import create_documents


FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures"


def test_create_documents_produces_vector_store():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = f"{FIXTURE_DIR}/douglass_ch1.pdf"
        doc_chunks = process_document(file_path=path)
        vector_store = create_documents(
            documents=doc_chunks,
            persist_directory=str(temp_dir)
        )

        assert len(vector_store.get()["ids"]) == len(doc_chunks)
        results = vector_store.similarity_search("childhood", k=1)
        assert len(results) == 1
        assert isinstance(results[0], Document)
