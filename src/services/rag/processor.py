from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def process_document(file_path: str):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    else:
        # TODO: Make work for docx via tests/fixtures/douglass_ch1.docx
        with open(file_path) as f:
            text = f.read()
            docs = [Document(page_content=text, metadata={})]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    return text_splitter.split_documents(docs)
