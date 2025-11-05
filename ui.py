import streamlit as st
from src.search import RAGSearch

# Initialize RAG once
@st.cache_resource
def load_rag():
    return RAGSearch()

st.set_page_config(page_title="RAG Assistant", layout="centered")

st.title("RAG Assistant")
st.markdown("Ask questions based on your uploaded documents")

# Load RAG
rag = load_rag()

query = st.text_input("Enter your question:")

if st.button("Search") and query:
    with st.spinner("Searching and generating summary..."):
        result = rag.search_and_summarize(query, top_k=3)
    
    st.subheader("Answer")
    st.write(result['answer'])

    if result.get("sources"):
        st.subheader("Sources")
        for src in result['sources']:
            st.markdown(f"- `{src.get('source', 'unknown')}` (distance={src['distance']:.4f})")
