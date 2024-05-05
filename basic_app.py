import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma as ChromaDB
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from scrape_any_url import scrape_site, keywords
from store_any_url import store_in_chroma
from extract_VC_info import extract_vc_details

openai_api_key = st.secrets["OPENAI_API_KEY"] if 'OPENAI_API_KEY' in st.secrets else os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("API key not found. Please set it as an environment variable or in secrets.toml.")
    st.stop()


st.title('VC Information Extraction and Comparison Tool')
vc_url_input = st.text_input('Enter the URL of the VC firm:', '')
submit_button = st.button('Extract and Compare VC Information')

vectorstore = ChromaDB(persist_directory="chromadb/", embedding_function=OpenAIEmbeddings(api_key=openai_api_key))
index = VectorStoreIndexWrapper(vectorstore=vectorstore)

def compare_vc_content(current_vc_name):
    """Compare the VC content against other entries in the database and retrieve the top 3 similar VCs."""
    try:
        results = index.most_similar(current_vc_name, top_n=3)
        return results
    except Exception as e:
        st.error(f"Error during similarity comparison: {e}")
        return []

if submit_button and vc_url_input:
    if not openai_api_key.startswith('sk-'):
        st.error('Please enter a valid OpenAI API key.')
    else:
        filename = scrape_site(vc_url_input, keywords)
        store_in_chroma(filename)
        vc_details = extract_vc_details(filename)
        st.json(vc_details)

        similar_vcs = compare_vc_content(filename.rsplit('.', 1)[0])
        st.subheader("Similar VC Firms:")
        for vc in similar_vcs:
            st.text(vc['name'])




