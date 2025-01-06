from pathlib import Path

import pytest

from src.services.rag.processor import process_document


FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures"


def test_processed_pdf_has_metadata():
    path = f"{FIXTURE_DIR}/douglass_ch1.pdf"
    result = process_document(file_path=path)
    assert 'source' in result[0].metadata
    assert 'page' in result[0].metadata

    assert len(result) > 30
    assert all(len(chunk.page_content) <= 500 for chunk in result)

@pytest.mark.skip(reason="DOCX support not yet implemented")
def test_processed_docx_has_metadata():
    pass
