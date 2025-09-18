# main.py
import streamlit as st
import os
import shutil
from src.ingest import ingest_codebase
from src.query import ask_question

# Page config
st.set_page_config(
    page_title="🧠 Code Documentation Helper",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 Code Documentation Helper")
st.markdown("Ask natural language questions about your codebase. Get precise answers with code snippets & context.")

# Sidebar: Ingestion
st.sidebar.header("📂 Ingest Your Codebase")

# Option 1: Upload Files
uploaded_files = st.sidebar.file_uploader(
    "Upload code files",
    accept_multiple_files=True,
    type=[
        "py", "js", "ts", "jsx", "tsx", "java", "go", "rs", "cpp", "c", "h", "hpp", "cs",
        "md", "txt", "json", "yaml", "yml", "toml", "env", "html", "css", "scss", "vue", "svelte"
    ]
)

if st.sidebar.button("🚀 Ingest Uploaded Files") and uploaded_files:
    temp_dir = "./data/uploaded_code"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    with st.spinner("Ingesting uploaded files..."):
        ingest_codebase(temp_dir)
    st.sidebar.success("✅ Upload & ingestion complete!")

# Option 2: Ingest Local Folder
st.sidebar.markdown("---")
local_path = st.sidebar.text_input("Ingest from local folder:", value="./data/codebase")
if st.sidebar.button("📁 Ingest Local Folder"):
    if os.path.exists(local_path):
        with st.spinner(f"Ingesting from {local_path}..."):
            ingest_codebase(local_path)
        st.sidebar.success(f"✅ Ingested from {local_path}")
    else:
        st.sidebar.error("❌ Path does not exist.")

# Main: Q&A Interface
st.header("💬 Ask a Question")
user_question = st.text_input("Type your question:")

if st.button("🔍 Get Answer") and user_question.strip():
    with st.spinner("Thinking..."):
        try:
            answer = ask_question(user_question)
            st.subheader("💡 Answer")
            st.markdown(answer)

            # Show context (optional)
            with st.expander("📂 Retrieved Context (for transparency)"):
                from src.query import collection
                from src.utils import get_embedding, format_context
                query_embedding = get_embedding(user_question)
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=3,
                    include=["documents", "metadatas"]
                )
                context_display = format_context(results)
                st.code(context_display, language="text")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Tip: Make sure you've ingested code first, and your Gemini API key is set in `.env`")

# Footer
st.markdown("---")
st.caption("Powered by Local Embeddings (all-MiniLM-L6-v2) + Gemini 1.5 Flash | Code Documentation Helper v1.0")