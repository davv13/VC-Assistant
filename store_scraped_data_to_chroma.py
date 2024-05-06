import os
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHROMA_PATH = "chromadb"
DATA_PATH = "Data"

def initialize_api_key():
    with open('openai_api_key.txt', 'r') as f:
        os.environ["OPENAI_API_KEY"] = f.read().strip()

def load_documents(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Markdown file not found: '{file_path}'")
    with open(file_path, 'r', encoding='utf-8') as file:
        page_content = file.read()
    document = Document(metadata={"title": os.path.basename(file_path)}, page_content=page_content)
    return [document]

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)

def save_to_chroma(chunks: list[Document], db):
    db.add_documents(chunks)
    db.persist()

def process_files():
    initialize_api_key()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
    
    for filename in os.listdir(DATA_PATH):
        if filename.endswith('.md'):
            file_path = os.path.join(DATA_PATH, filename)
            try:
                documents = load_documents(file_path)
                chunks = split_text(documents)
                save_to_chroma(chunks, db)
                print(f"Processed and stored {filename} in ChromaDB.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

process_files()
