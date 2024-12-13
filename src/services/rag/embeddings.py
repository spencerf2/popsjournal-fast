from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    """Configure embedding model."""
    return HuggingFaceEmbeddings(
        encode_kwargs={'normalize_embeddings': False}
    )
