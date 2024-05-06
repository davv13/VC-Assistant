__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma as ChromaDB
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from scrape_any_url import scrape_site, keywords
from extract_VC_info import extract_vc_details
from langchain.vectorstores.chroma import Chroma


openai_api_key = st.secrets["OPENAI_API_KEY"] if 'OPENAI_API_KEY' in st.secrets else os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("API key not found. Please set it as an environment variable or in secrets.toml.")
    st.stop()


st.title('VC Information Extraction and Comparison Tool')
vc_url_input = st.text_input('Enter the URL of the VC firm:', '')
submit_button = st.button('Extract and Compare VC Information')

vectorstore = ChromaDB(persist_directory="chromadb/", embedding_function=OpenAIEmbeddings(api_key=openai_api_key))
index = VectorStoreIndexWrapper(vectorstore=vectorstore)

if submit_button and vc_url_input:
    if not openai_api_key.startswith('sk-'):
        st.error('Please enter a valid OpenAI API key.')
    else:
        filename = scrape_site(vc_url_input, keywords)
        vc_details = extract_vc_details(filename)
        st.json(vc_details)

        similarity = vectorstore.similarity_search_with_relevance_scores(filename, k = 3)
        st.subheader("Similar VC Firms:")
        for doc, score in similarity:
            title = doc.metadata['title'].rstrip('md')
            st.write(f"{title} - Similarity Score: {score:.3f}")



