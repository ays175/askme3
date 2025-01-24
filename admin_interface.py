# admin_interface.py
import streamlit as st
from utils import load_txt, load_pdf, load_doc, chunk_and_embed

def admin_interface():
    st.header("Admin Interface")

    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, type=["txt", "pdf", "doc", "docx"])
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".txt"):
                documents.append((uploaded_file.name, load_txt(uploaded_file)))
            elif uploaded_file.name.endswith(".pdf"):
                documents.append((uploaded_file.name, load_pdf(uploaded_file)))
            elif uploaded_file.name.endswith(".doc") or uploaded_file.name.endswith(".docx"):
                documents.append((uploaded_file.name, load_doc(uploaded_file)))

        if st.button("Build/Refresh Vector Store"):
            index, metadata = chunk_and_embed(documents)
            st.session_state["faiss_index"] = index
            st.session_state["metadata"] = metadata
            st.session_state["documents"] = documents
            st.success("FAISS index created successfully!")
