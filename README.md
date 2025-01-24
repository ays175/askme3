# Multi-File RAG Streamlit App

This repository contains a **multi-file Streamlit app** demonstrating **Retrieval-Augmented Generation (RAG)** with support for different LLMs (**GPT 01pro**, **Claude Sonnet**, **Gemini 1.5**). It uses a `.env` file to manage API keys, and provides separate admin and user interfaces.

---

## Features

- **Admin Interface**  
  - Upload documents (`.txt`, `.docx`, `.pdf`).  
  - Build a vector store (Chroma) of the uploaded documents.  
  - Choose a default LLM for the system (GPT 4o Mini, Claude Sonnet, or Gemini 1.5).

- **User Interface**  
  - Select one of the available LLMs.  
  - Choose which document to query.  
  - Ask questions, receiving ~500-word answers based on retrieved chunks from all documents.

- **Token Limiting**  
  - Dynamically limit the total chunked context (e.g., 2000 tokens) before sending to the LLM.

- **Basic Authentication**  
  - An optional “Admin Login” to secure the admin interface (username: `admin`, password: `secret` by default).

---

## File Structure

my-rag-app/ ├── .env ├── requirements.txt ├── streamlit_app.py ├── admin_interface.py ├── user_interface.py ├── utils.py └── layout.py

yaml
Copy

- **`.env`**: Stores your API keys for GPT 01pro, Claude Sonnet, and Gemini 1.5.  
- **`requirements.txt`**: Python dependencies for the app.  
- **`streamlit_app.py`**: Main entry point for the Streamlit app, including a simple admin login flow.  
- **`admin_interface.py`**: Code for the admin interface (upload documents, build vector store).  
- **`user_interface.py`**: Code for the user interface (select LLM, select document, ask questions).  
- **`utils.py`**: Utility functions (document loaders, chunking, embeddings, token limiting, LLM routing).  
- **`layout.py`**: Common layout configuration for the Streamlit app.

---

## Requirements

- **Python 3.8+** (recommended)
- **pip** (or another Python package manager)

---

## Setup

1. **Clone this repository** (or download it) and navigate to it:
   
       git clone https://github.com/yourusername/my-rag-app.git
       cd my-rag-app

2. **Create & activate a virtual environment** (optional, but recommended):
   
       python -m venv venv
       # On macOS/Linux:
       source venv/bin/activate
       # On Windows:
       venv\Scripts\activate

3. **Install dependencies**:
   
       pip install -r requirements.txt

4. **Configure `.env`**:
   - Create a file named `.env` in the project root.
   - Add your API keys (replace placeholders with valid keys):
     
        OPENAI_API_KEY=sk-<gpt01pro-key>
         CLAUDE_SONNET_API_KEY=sk-<claude-key>
         GEMINI_15_API_KEY=sk-<gemini-key>

---

## Usage (Local)

1. **Run the Streamlit app**:
   
       streamlit run streamlit_app.py

2. **Open** the URL shown in the terminal (e.g., `http://localhost:8501`) in your browser.
3. **Switch** to “Admin” mode in the sidebar:
   - Login with **username**: `admin`, **password**: `secret` (default credentials).
   - Upload documents and click “Build/Refresh Vector Store.”
4. **Switch** to “User” mode:
   - Select which LLM you want to query.
   - Select which document to focus on.
   - Ask your question, get a ~500-word answer referencing your uploaded docs.

---

## Deployment (Streamlit Community Cloud)

1. **Push** your code to a **public GitHub repository**.
2. Go to [Streamlit Cloud](https://share.streamlit.io) and click **“New app.”**
3. Select your **repo** and **branch**.
4. In **File path**, choose `streamlit_app.py`.
5. In **Advanced Settings**, set up “Secrets” for your API keys (if you prefer that to `.env`), for example:

       GPT_01PRO_API_KEY="sk-<your-key>"
       CLAUDE_SONNET_API_KEY="sk-<your-key>"
       GEMINI_15_API_KEY="sk-<your-key>"

   Then adjust your code to use `st.secrets[...]` instead of `.env` if desired.
6. Click **“Deploy.”** Your app will be available at a Streamlit-provided URL.

> **Note**: Streamlit Community Cloud provides **ephemeral storage**—any files you upload or vector store you create will disappear when the app sleeps or restarts. For persistent storage, integrate an external database or vector DB.

---

## Contributing

- **Fork** this repo, make changes, and open a pull request.
- Or simply open an **issue** to discuss improvements.

---

## License

Licensed under **MIT**. Feel free to adapt and reuse this code as you see fit.

---

## Troubleshooting

- **Missing Dependencies**: Ensure every library you use is in `requirements.txt`.
- **App Not Launching**: Check for syntax errors or a wrong file path.
- **Runtime Errors**: Inspect Streamlit logs or error traces in the UI.
- **No Documents**: Make sure you switch to Admin mode, upload docs, then build the vector store before querying.

Enjoy exploring **Retrieval-Augmented Generation** with multiple LLM choices! If you have an
