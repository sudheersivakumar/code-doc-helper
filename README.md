# 🧠 Code Documentation Helper
> _Ask your codebase natural language questions — and get accurate, contextual answers with code snippets._
> _No more Ctrl+F hell. No more asking “Where is this defined?”_
### Built with Local Embeddings (no quota limits) + Gemini 1.5 Flash + CRAG-inspired correction loop for maximum accuracy.

## Code Documentation Helper Screenshot
<img width="1913" height="860" alt="Image" src="https://github.com/user-attachments/assets/34b63ce8-82b5-4e5a-a5b4-7e96f92a89ad" />

## 🚀 Why This Exists
#### Ever spent 30 minutes searching for where a config variable is loaded?
#### Or asked a teammate “Where’s the auth middleware?” — only to get “I think it’s in utils/… or maybe middleware/?”
#### This tool fixes that.
#### You ask:
> _"" Where is the JWT secret key loaded?""_
#### It answers:
> _"" In config/auth.py, line 42. Loaded from environment variable JWT_SECRET_KEY.""_
#### ...and shows you the actual code snippet
## ✅ Features
- 💬 Natural Language Q&A — Ask questions in plain English.
- 🧩 Code + Docs Aware — Understands `.py`, `.js`, `.ts`, `.md`, `.json`, `.yaml`, and more.
- 🧠 Local Embeddings — Uses `all-MiniLM-L6-v2` → No API quotas. No rate limits. Works offline.
- 🔁 CRAG Correction Loop — If unsure, retries or says “I don’t know” — no hallucinations.
- 🎨 Beautiful Streamlit UI — Drag, drop, ask, done.
- 📁 Auto-Skips Noise — Ignores `node_modules`, `__pycache__`, `.git`, etc.
## 🛠️ Tech Stack
<pre>|Component   |Technology                                              |
|------------|--------------------------------------------------------|
|LLM         |Google Gemini 1.5 Flash                                 |
|Embeddings  |sentence-transformers/all-MiniLM-L6-v2 (Local)          |
|Vector DB   |ChromaDB                                                |
|UI Framework|Streamlit                                               |
|Correction  |Custom CRAG-inspired logic                              |
|Lang Support|Python, JS, TS, Java, Go, Rust, C/C++, configs, Markdown|</pre>
## ⚙️ Setup & Installation
### 1. Clone the Repo 
```bash 
git clone https://github.com/sudheersivakumar/code-doc-helper.git
cd code-doc-helper
```

### 2.Set up virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3.Install dependencies 
```bash
pip install -r requirements.txt
```

### 4. Get your Gemini API Key
1. Go to Google AI Studio: [https://ai.google.dev/](https://ai.google.dev/)
2. Create an API key.
3. Add it to a .env file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```
>_💡Tip: Link billing to unlock Tier 1 limits (15 RPM → 2,000 RPM). Free to upgrade!_

## 🏃‍♂️ How to Run
### Start the Web 
```bash
streamlit run main.py
```
→ Opens at http://localhost:8501

### Ingest Your Codebase
1. Via UI: Upload files or point to a local folder (e.g., ./data/codebase).
2. Click “Ingest”.
3. Wait for embeddings to generate (local → fast & free).

#### Ask Questions!
#### Type:
> _“How is user login handled?”_
#### Get:
> _"" Precise answer + code snippet + file path.""_
## 📂 Project Structure
```
code-doc-helper/
│── .env
│── requirements.txt
│── main.py             # Streamlit UI
│
├── data/
│     └──codebase/      # Put your codes here
│   
├── chroma_db/          # Local vector DB (auto-created)
│   
├── src/
    ├── ingest.py        # Code ingestion + chunking
    ├── query.py         # Handle questions + retrieval
    ├── rag_pipeline.py  # CRAG correction logic
    └── utils.py         # Embeddings, chunking, formatting

```
## 🔄 CRAG Logic (Simplified)
#### Your question → Retrieve top code snippets → Ask Gemini →
#### If answer contains “I don’t know” or “insufficient context” → Retry →
#### Still unsure? → Returns fallback message.
> _"Goal: Better to say “I don’t know” than give you wrong code."_

## 🤝 Contributing
#### Found a bug? Want to add syntax highlighting or Git integration?
#### PRs welcome!
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License
#### MIT License — Use it freely for personal or commercial projects.



