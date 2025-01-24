# utils.py
import os
import streamlit as st
import PyPDF2
from docx import Document as DocxDocument
import tiktoken
from typing import List
import numpy as np
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai.chat_models import ChatOpenAI
import faiss



# Retrieve secrets from the Streamlit Cloud panel
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

def load_txt(file) -> str:
    """Load a .txt file (from BytesIO) and return its text."""
    return file.read().decode("utf-8").strip()

def load_pdf(file) -> str:
    """Load a .pdf file (from BytesIO) and return its text."""
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text.strip()

def load_doc(file) -> str:
    """Load a .doc/.docx file (from BytesIO) and return its text."""
    document = DocxDocument(file)
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

def chunk_and_embed(documents):
    """
    Splits each doc into chunks, creates embeddings using OpenAIEmbeddings,
    and stores them in a FAISS index. Returns the FAISS index and metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    doc_chunks = []
    metadata = []

    for doc_name, doc_text in documents:
        if not doc_text.strip():
            print(f"Document {doc_name} is empty or invalid!")
            continue

        chunks = text_splitter.split_text(doc_text)
        for chunk in chunks:
            doc_chunks.append(chunk)
            metadata.append({"source": doc_name})

    if not doc_chunks:
        raise ValueError("No valid chunks were generated from the documents!")

    embedding_model = OpenAIEmbeddings(
        openai_api_key=st.secrets["OPENAI_API_KEY"]
    )

    embeddings = embedding_model.embed_documents(doc_chunks)
    embeddings = np.array(embeddings, dtype="float32")

    if embeddings.shape[0] == 0:
        raise ValueError("Embeddings array is empty! Ensure the documents are valid and embeddings are being generated.")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, metadata

def search_faiss(index, query, metadata, top_k=5):
    """
    Search the FAISS index and return the top_k results with metadata.
    """
    embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    query_embedding = np.array(embedding_model.embed_query(query), dtype="float32").reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            results.append({"content": metadata[idx]["source"], "distance": distances[0][i]})

    return results

def approximate_token_count(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

def limit_context_by_tokens(
    chunks, max_tokens=2000, model_name="gpt-3.5-turbo"
) -> str:
    """
    Combine chunk strings until we reach (or approach) the max_tokens limit.
    """
    combined_text = ""
    for chunk in chunks:
        chunk = str(chunk) if not isinstance(chunk, str) else chunk
        proposed = combined_text + "\n" + chunk
        if approximate_token_count(proposed, model_name=model_name) <= max_tokens:
            combined_text = proposed
        else:
            break
    return combined_text.strip()

def load_llm(llm_name: str):
    """
    Load an LLM based on the provided name. Adjust configurations as needed.
    """
    if llm_name == "GPT 01pro":
        model_name = "gpt-4"
    elif llm_name == "Claude Sonnet":
        model_name = "claude-v1"
    elif llm_name == "Gemini 1.5":
        model_name = "gpt-3.5-turbo"
    else:
        model_name = "gpt-3.5-turbo"

    llm = ChatOpenAI(
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        model=model_name,
        temperature=0.7
    )
    return llm
