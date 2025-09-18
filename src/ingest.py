# src/ingest.py
import os
import chromadb
from dotenv import load_dotenv
from tqdm import tqdm
from .utils import chunk_code, get_embedding

load_dotenv()

# Initialize Chroma client
client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_or_create_collection(
    name="codebase",
    embedding_function=None  # We handle embeddings manually
)

# Support more file types — configs, docs, etc.
SUPPORTED_EXTENSIONS = (
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs',
    '.cpp', '.c', '.h', '.hpp', '.cs',
    '.md', '.txt', '.log',
    '.json', '.yaml', '.yml', '.toml', '.env',
    '.html', '.css', '.scss', '.vue', '.svelte'
)

def ingest_codebase(root_path):
    """
    Ingest all supported files in root_path into ChromaDB using local embeddings.
    """
    documents = []
    metadatas = []
    ids = []

    print(f"📂 Scanning codebase at: {root_path}")

    file_count = 0
    for dirpath, _, filenames in os.walk(root_path):
        # Skip virtual environments, node_modules, etc.
        if any(skip in dirpath for skip in ['__pycache__', 'node_modules', '.git', 'venv', '.venv']):
            continue

        for filename in filenames:
            if not filename.endswith(SUPPORTED_EXTENSIONS):
                continue

            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️  Skipping {filepath}: {e}")
                continue

            if not content.strip():
                continue

            file_count += 1
            chunks = chunk_code(content, chunk_size=500, filename=filename, filepath=filepath)

            for i, chunk in enumerate(chunks):
                doc_id = f"{filename}_{i}"
                documents.append(chunk["text"])
                metadatas.append({
                    "filename": filename,
                    "filepath": filepath,
                    "chunk_index": i,
                    "language": filename.split('.')[-1] if '.' in filename else 'txt',
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"]
                })
                ids.append(doc_id)

    if not documents:
        print("❌ No documents found to ingest.")
        return

    print(f"✅ Found {file_count} files → {len(documents)} chunks")
    print(f"🧠 Generating local embeddings for {len(documents)} chunks...")

    embeddings = []
    for doc in tqdm(documents, desc="Embedding", unit="chunk"):
        embeddings.append(get_embedding(doc))

    print(f"💾 Storing in ChromaDB...")
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("🎉 Ingestion complete!")