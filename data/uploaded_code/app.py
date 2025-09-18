# app.py
"""
MindVault — Personal Knowledge Base with Semantic Search
Powered by ChromaDB + Google Gemini Embeddings
Beautiful Streamlit UI for querying your documents by meaning.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from src.query import search
from src.utils import truncate_text, format_similarity_score
import time

# === Page Config ===
st.set_page_config(
    page_title="🧠 MindVault — Semantic Search",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# === Custom CSS for Professional Look ===
st.markdown("""
    <style>
    .result-box {
        background-color: #f8f9fa;
        border-left: 4px solid #0d6efd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .source-tag {
        background-color: #e9ecef;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .similarity-badge {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# === Header ===
st.title("🧠 MindVault")
st.markdown("### Your Personal Semantic Knowledge Base")
st.markdown("Ask in natural language — find what you *mean*, not just what you *type*.")
st.divider()

# === Search Input ===
query = st.text_input(
    "🔍 Ask anything about your documents:",
    placeholder="e.g., 'How do I manage my time effectively?'",
    help="Uses Google Gemini Embeddings for semantic understanding"
)

# === Search Logic ===
if query:
    with st.spinner("🧠 Searching your knowledge vault..."):
        time.sleep(0.3)  # Optional: improves perceived responsiveness
        results = search(query, n_results=5)

    if not results or len(results['documents'][0]) == 0:
        st.warning("📭 No relevant results found. Try rephrasing your question.")
    else:
        st.success(f"✅ Found {len(results['documents'][0])} relevant chunks", icon="🧠")
        st.divider()

        for i, (doc, meta, dist) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            similarity_str = format_similarity_score(dist)
            preview = truncate_text(doc, max_length=500)

            # Create unique expandable section for each result
            with st.expander(f"💎 Result {i+1} — {similarity_str} Match", expanded=(i == 0)):
                # Metadata bar
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f'<span class="source-tag">📄 {meta.get("source", "Unknown")}</span>', unsafe_allow_html=True)
                with col2:
                    chunk_info = f'Chunk {meta.get("chunk", "?")}'
                    if "total_chunks" in meta:
                        chunk_info += f'/{meta["total_chunks"]}'
                    st.markdown(f'<span class="source-tag">{chunk_info}</span>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<span class="similarity-badge">{similarity_str}</span>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(preview)

                # Optional: Show full text in tooltip or code block
                with st.popover("👁️ View Full Chunk"):
                    st.text(doc)

                # Optional: Add copy button
                st.code(doc[:200] + "...", language="text")
                st.button("📋 Copy", key=f"copy_{i}", on_click=lambda t=doc: st.write(f"Copied!"), type="secondary")

# === Sidebar ===
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Gemini_Logo.png", width=120)
    st.header("⚙️ MindVault")
    st.markdown("Powered by:")
    st.markdown("- **ChromaDB** — Vector Database")
    st.markdown("- **Google Gemini Embeddings** — Semantic Understanding")
    st.markdown("- **Streamlit** — Beautiful UI")
    st.divider()
    st.caption("📁 Documents indexed: Check `./data` folder")
    st.caption("🔐 Your data never leaves your machine.")
    st.caption("💡 Tip: Use natural language — 'ideas about productivity' works even if those words aren't in the doc!")

    if st.button("🔄 Reload DB (if you added new files)"):
        st.cache_data.clear()
        st.success("Cache cleared. Re-ingest via CLI: `python src/ingest.py`")

# === Footer ===
st.markdown("---")
st.caption("🧠 Built with ChromaDB + Gemini Embeddings | Personal Knowledge Base for Humans")