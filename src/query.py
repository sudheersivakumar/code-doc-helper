# src/query.py
import os
import chromadb
from google.generativeai import GenerativeModel
import google.generativeai as genai
from dotenv import load_dotenv
from .utils import format_context, get_embedding
from .rag_pipeline import crag_generate_answer

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 1.5 Flash — generous free tier (15 RPM, 1M TPM, 200 RPD)
model = GenerativeModel('gemini-1.5-flash')

# Initialize Chroma client
client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection("codebase")

def ask_question(question: str, n_results=3):
    """
    Retrieve context using local embedding, generate answer using Gemini + CRAG.
    """
    if not question.strip():
        return "Please ask a valid question."

    # Step 1: Embed query locally
    print("🔍 Embedding query locally...")
    query_embedding = get_embedding(question)

    # Step 2: Retrieve from ChromaDB
    print(f"📚 Retrieving top {n_results} relevant chunks...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas"]  # Explicitly include what we need
    )

    # Step 3: Format context
    context = format_context(results)

    # Step 4: Generate answer with CRAG loop
    print("💬 Generating answer with Gemini...")
    answer = crag_generate_answer(question, context, model)

    return answer