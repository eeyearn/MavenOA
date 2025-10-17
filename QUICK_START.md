# Quick Start Guide - 5 Minutes to Running

Get up and running as fast as possible.

## Prerequisites Check

```bash
node --version   # Need 18+
python3 --version  # Need 3.9+
```

## 1. Google OAuth (Do This First!)

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create project → Enable "Google Drive API"
3. Credentials → Create OAuth Client → Web Application
4. Redirect URI: `http://localhost:8000/api/auth/callback`
5. Copy Client ID and Secret

## 2. Backend Setup

```bash
cd backend

# Create & activate venv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install everything (quickest option)
pip install -r requirements.txt
pip install chromadb openai  # Simplest stack

# Configure
cp .env.example .env
nano .env  # Add your Google OAuth and OpenAI API key

# Start
python -m src.main
```

## 3. Frontend Setup

New terminal:

```bash
cd frontend
npm install
npm run dev
```

## 4. Test It Works

1. Open http://localhost:3000
2. Click "Connect Google Drive"
3. Authorize with Google
4. You should see the main interface

## 5. Create Test Data

In Google Drive, create:
- A folder "Test Docs"
- A Google Doc "Project Plan" with some text
- Another Doc "Meeting Notes" with different text

## 6. Now Implement!

You need to code these files:

### Priority 1: Ingestion (60-90 min)
**File:** `backend/src/services/ingestion_service.py`

Quick implementation guide:
```python
# 1. Init vector DB
self.chroma_client = chromadb.Client()
self.collection = self.chroma_client.get_or_create_collection("drive_documents")
self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. In start_ingestion():
files = drive_service.list_files()
for file in files:
    text = drive_service.export_google_doc(file['id'], 'text/plain').decode('utf-8')
    chunks = chunk_text(text)  # 500 chars, 100 overlap
    embeddings = openai_client.embeddings.create(model="text-embedding-3-small", input=chunks)
    collection.add(documents=chunks, embeddings=embeddings.data, ids=...)
```

### Priority 2: Retrieval (45-60 min)
**File:** `backend/src/services/retrieval_service.py`

Quick implementation guide:
```python
# In search():
query_embedding = openai_client.embeddings.create(model="text-embedding-3-small", input=query)
results = collection.query(query_embeddings=[query_embedding.data[0].embedding], n_results=10)
return format_results(results)  # Build SearchResult objects
```

### Priority 3: Chat (Optional, 30-45 min)
**File:** `backend/src/services/chat_service.py`

## 7. Test Your Implementation

1. Click "Start Ingestion" → Should process your files
2. Search "project" → Should find Project Plan
3. Search "meeting" → Should find Meeting Notes
4. Select folder → Should filter results

## 8. Submit

```bash
git init
git add .
git commit -m "Initial implementation"
git remote add origin <your-repo-url>
git push -u origin main

# Add @yuvbindal and @shayaansultan as collaborators
# Email with link and hours spent
```

## Recommended Stack (Simplest)

- **Vector DB:** ChromaDB (no setup needed)
- **Embeddings:** OpenAI text-embedding-3-small
- **LLM:** OpenAI GPT-3.5-turbo (for chat)

Only requires one API key: OpenAI

## Need Help?

- Setup issues? See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Implementation help? See [IMPLEMENTATION_EXAMPLE.md](IMPLEMENTATION_EXAMPLE.md)
- Stuck? Email yuv2bindal@gmail.com or sultan.shayaan@gmail.com

## Time Budget

- Setup: 30 min
- Ingestion: 75 min
- Retrieval: 50 min
- Testing: 25 min
- **Total: 3 hours**

Good luck! Focus on getting something working end-to-end first, then polish.
