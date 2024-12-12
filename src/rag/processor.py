from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_document(file_path: str):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text = " ".join(doc.page_content for doc in docs)
    else:
        with open(file_path) as f:
            text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=25,
        length_function=len,
    )
    return text_splitter.create_documents([text])
