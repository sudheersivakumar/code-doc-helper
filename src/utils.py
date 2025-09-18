# src/utils.py
from sentence_transformers import SentenceTransformer

# Load embedding model ONCE at import
_local_embedder = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Generate embedding using local SentenceTransformer model.
    Returns list of floats (compatible with ChromaDB).
    """
    if not text.strip():
        return _local_embedder.encode("empty document", convert_to_numpy=True).tolist()
    return _local_embedder.encode(text, convert_to_numpy=True).tolist()

def chunk_code(text, chunk_size=500, filename="", filepath=""):
    """
    Split code/documentation into chunks by lines.
    Larger chunk_size = fewer embedding calls = faster + cheaper.
    """
    if not text.strip():
        return []

    lines = text.splitlines()
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_text = "\n".join(chunk_lines)
        chunks.append({
            "text": chunk_text,
            "start_line": i,
            "end_line": i + len(chunk_lines) - 1,
            "filename": filename,
            "filepath": filepath
        })
    return chunks

def format_context(retrieved_data):
    """
    Format retrieved documents and metadata into readable context string for LLM.
    """
    if not retrieved_data or not retrieved_data.get('documents') or not retrieved_data['documents'][0]:
        return "No relevant context found."

    contexts = []
    for i, doc in enumerate(retrieved_data['documents'][0]):
        meta = retrieved_data['metadatas'][0][i] if retrieved_data['metadatas'] and len(retrieved_data['metadatas'][0]) > i else {}
        filename = meta.get('filename', 'unknown')
        start = meta.get('start_line', '?')
        end = meta.get('end_line', '?')
        header = f"📄 {filename} (lines {start}-{end})"
        contexts.append(f"{header}\n{doc}\n{'─' * 50}")
    return "\n\n".join(contexts)