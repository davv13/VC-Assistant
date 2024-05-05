import os
import shutil
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_PATH = "chromadb"
DATA_PATH = "Data/"

def initialize_api_key():
    with open('openai_api_key.txt', 'r') as f:
        os.environ["OPENAI_API_KEY"] = f.read().strip()

def generate_data_store(vc_name: str):
    documents = load_documents(vc_name)
    chunks = split_text(documents)
    save_to_chroma(chunks, vc_name)

def load_documents(vc_name: str):
    file_path = os.path.join(DATA_PATH, f"{vc_name}.md")
    print(f"Attempting to load file: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Markdown file not found: '{file_path}'")
    with open(file_path, 'r', encoding='utf-8') as file:
        page_content = file.read()
    document = Document(page_content=page_content, title=vc_name)
    return [document]

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def save_to_chroma(chunks: list[Document], vc_name: str):
    lang_chroma_path = os.path.join(CHROMA_PATH, vc_name)
    if os.path.exists(lang_chroma_path):
        shutil.rmtree(lang_chroma_path)
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=lang_chroma_path
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {lang_chroma_path}.")

def store_in_chroma(vc_filename):
    initialize_api_key()
    vc_name = vc_filename.rsplit('.', 1)[0]
    generate_data_store(vc_name)
