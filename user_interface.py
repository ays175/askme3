# user_interface.py
import streamlit as st
from textblob import TextBlob
from utils import limit_context_by_tokens, load_llm, search_faiss

def user_interface():
    """
    User side: pick an LLM, pick a doc, ask questions.
    Must have st.session_state["faiss_index"] built in admin.
    """
    st.header("User Interface")

    if "documents" not in st.session_state or not st.session_state["documents"]:
        st.warning("No documents available. Please ask Admin to upload and build store.")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        user_llm_choice = st.selectbox(
            "Select an LLM for QA",
            ["GPT 01pro", "Claude Sonnet", "Gemini 1.5"],
            key="user_llm_choice"
        )

        # Dropdown to select a specific document
        doc_list = [doc_name for (doc_name, _) in st.session_state["documents"]]
        selected_doc_name = st.selectbox("Select a document to query", doc_list)

        # Slider to choose answer length
        answer_length = st.slider(
            "Choose desired answer length (words):",
            min_value=100,
            max_value=600,
            value=300,
            step=50
        )

        user_question = st.text_area("Ask a question:")

        if st.button("Get Answer"):
            if "faiss_index" not in st.session_state or st.session_state["faiss_index"] is None:
                st.error("No FAISS index found. Ask Admin to build it.")
                return

            # Retrieve the content for the selected document
            selected_content = [doc_text for doc_name, doc_text in st.session_state["documents"] if doc_name == selected_doc_name]

            if not selected_content:
                st.error("No content found for the selected document.")
                return

            results = search_faiss(st.session_state["faiss_index"], user_question, st.session_state["metadata"], top_k=5)

            # Limit context to the selected document
            combined_context = limit_context_by_tokens(selected_content + [r["content"] for r in results], max_tokens=2000)

            llm = load_llm(user_llm_choice)
            final_prompt = (
                f"You are an AI assistant with a thorough knowledge of the selected document '{selected_doc_name}'.\n"
                f"Deliver an answer that is approximately {answer_length} words.\n"
                f"Question: {user_question}\n\nContext: {combined_context}\n\nAnswer:"
            )

            raw_answer = llm.invoke(final_prompt)
            answer_text = raw_answer.content if hasattr(raw_answer, "content") else str(raw_answer)

            sentiment = TextBlob(answer_text).sentiment

            st.subheader("Answer:")
            st.write(answer_text)
            st.write(f"**Sentiment**: Polarity={sentiment.polarity:.2f}, Subjectivity={sentiment.subjectivity:.2f}")

    with col2:
        st.subheader("Document Viewer")
        if "documents" in st.session_state and st.session_state["documents"]:
            selected_content = [doc_text for doc_name, doc_text in st.session_state["documents"] if doc_name == selected_doc_name]
            if selected_content:
                st.text_area("Selected Document Content:", selected_content[0], height=500)