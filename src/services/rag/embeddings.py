from langchain_huggingface.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    """Configure embedding model. Using default: all-mpnet-base-v2"""
    return HuggingFaceEmbeddings(
        encode_kwargs={'normalize_embeddings': True}
    )
