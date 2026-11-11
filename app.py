"""Interface Streamlit: streamlit run app.py"""
import streamlit as st

from rag.chunking import load_corpus
from rag.embedders import get_embedder
from rag.generate import answer
from rag.retriever import Retriever


@st.cache_resource
def get_retriever(embedder_name: str):
    return Retriever(load_corpus(), get_embedder(embedder_name))


st.title("Assistente de Frameworks de Segurança")
embedder_name = st.sidebar.selectbox("Embeddings", ["st", "tfidf"])
k = st.sidebar.slider("Trechos recuperados (k)", 1, 8, 4)

question = st.text_input("Pergunte sobre NIST CSF, CIS Controls ou OWASP Top 10")
if question:
    hits = get_retriever(embedder_name).search(question, k)
    st.markdown(answer(question, hits))
    with st.expander("Fontes recuperadas"):
        for c, score in hits:
            st.caption(f"{c.source} | {c.heading} | similaridade {score:.2f}")
            st.write(c.text)
