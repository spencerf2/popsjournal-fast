from uuid import uuid4

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.services.rag.embeddings import get_embedding_model


def create_documents(documents: list[Document], persist_directory: str | None = None):
    """Creates a vector store from documents.
        We will replace Chroma with pgvector when we move to prod. so
        the persist_directory param is temporary.
    """
    vector_store = Chroma(
        collection_name="popsjournal",
        embedding_function=get_embedding_model(),
        persist_directory=persist_directory,
    )

    ids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=ids)
    return vector_store
