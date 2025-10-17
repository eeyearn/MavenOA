# Maven Drive Copilot - Take Home Assessment

## Overview

This is a **2-3 hour take-home assessment** for building a Google Drive copilot. The frontend is fully implemented, and your task is to implement the backend services for ingestion and retrieval.

## What's Provided

### ✅ Complete Frontend
- React + TypeScript + Vite
- React Query for API integration
- Beautiful UI with Tailwind CSS
- Chat interface with source attribution
- Ingestion status monitoring

### ✅ Complete Backend Infrastructure
- FastAPI application structure
- Google OAuth integration (complete)
- API routes (complete)
- Type definitions (complete)

### ⚠️ What YOU Need to Implement

You need to implement **TWO core services**:

1. **Ingestion Service** ([backend/src/services/ingestion_service.py](backend/src/services/ingestion_service.py))
   - Connect to Google Drive and fetch files
   - Extract text from different file types
   - Chunk content intelligently
   - Generate embeddings
   - Store in vector database

2. **Retrieval Service** ([backend/src/services/retrieval_service.py](backend/src/services/retrieval_service.py))
   - Search vector database for relevant chunks
   - Apply metadata filters
   - Format results with source attribution

3. **Chat Service** ([backend/src/services/chat_service.py](backend/src/services/chat_service.py)) *(Optional for 2-3hr scope)*
   - Use retrieval service to find context
   - Generate responses with LLM
   - Cite sources clearly

## Time Estimate: 2-3 Hours

### Recommended Breakdown:
- **30 min**: Setup & Google OAuth configuration
- **60-90 min**: Implement Ingestion Service
- **45-60 min**: Implement Retrieval Service
- **15-30 min**: Testing & polish

## Quick Start

### Easy Mode: Automated Setup

We provide scripts to automatically install dependencies and run both services:

```bash
# Development mode (recommended) - runs both services with live logs
./dev.sh

# Or background mode - runs services in background
./start.sh

# To stop background services
./stop.sh
```

The scripts will:
- ✅ Check prerequisites (Node.js, Python)
- ✅ Create Python virtual environment
- ✅ Install all dependencies (backend + frontend)
- ✅ Start both services
- ✅ Show combined logs

### Manual Setup

If you prefer manual setup or the scripts don't work on your system:

#### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Google Cloud account (for OAuth)

#### 1. Google OAuth Setup (15 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Drive API**
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/auth/callback`
5. Copy Client ID and Client Secret

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install your chosen vector DB (pick one):
pip install chromadb  # Recommended for simplicity
# OR
pip install pinecone-client
# OR
pip install qdrant-client

# Install embedding provider (pick one):
pip install openai  # Recommended
# OR
pip install sentence-transformers

# Create .env file
cp .env.example .env
```

Edit `.env` with your credentials:
```env
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/callback

# Add your vector DB and embedding API keys
OPENAI_API_KEY=your_openai_key  # If using OpenAI
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will run on http://localhost:3000

### 4. Start Backend

```bash
cd backend

# Activate virtual environment if not already
source venv/bin/activate

# Start server
python -m src.main
```

The backend will run on http://localhost:8000

## Implementation Guide

### Step 1: Choose Your Stack

Pick one from each category:

**Vector Database:**
- ChromaDB (easiest, runs locally)
- Pinecone (cloud-hosted)
- Qdrant (self-hosted or cloud)

**Embedding Model:**
- OpenAI embeddings (best quality)
- Sentence Transformers (free, local)
- Cohere (good alternative)

**LLM for Chat:**
- OpenAI GPT-4/3.5
- Anthropic Claude
- Cohere

### Step 2: Implement Ingestion Service

File: [backend/src/services/ingestion_service.py](backend/src/services/ingestion_service.py)

Key methods to implement:
```python
async def start_ingestion(self):
    # 1. Get files from drive_service.list_files()
    # 2. For each file, extract text
    # 3. Chunk text intelligently
    # 4. Generate embeddings
    # 5. Store in vector DB with metadata
    pass

def _extract_text_from_file(self, file_metadata):
    # Handle Google Docs, PDFs, plain text
    pass

def _chunk_text(self, text, file_metadata):
    # Smart chunking with overlap
    pass
```

**Tips:**
- Start with Google Docs only (use `drive_service.export_google_doc()`)
- Use simple fixed-size chunks (500-1000 chars with 100 char overlap)
- Store metadata: `file_id`, `file_name`, `path`, `chunk_index`

### Step 3: Implement Retrieval Service

File: [backend/src/services/retrieval_service.py](backend/src/services/retrieval_service.py)

Key methods to implement:
```python
async def search(self, request: SearchRequest):
    # 1. Generate query embedding
    # 2. Search vector DB
    # 3. Filter by folder_id/file_id if provided
    # 4. Format results
    pass
```

**Tips:**
- Return top 5-10 results
- Include file metadata in results
- Calculate relevance scores (0-1 range)

### Step 4: (Optional) Implement Chat Service

File: [backend/src/services/chat_service.py](backend/src/services/chat_service.py)

```python
async def chat(self, request: ChatRequest):
    # 1. Use retrieval_service.search()
    # 2. Build context from results
    # 3. Call LLM with context
    # 4. Return response with sources
    pass
```

## Testing Your Implementation

### 1. Create Test Files in Google Drive

Create a few documents with different content:
- `Project Plan.docx` - project planning info
- `Meeting Notes.docx` - meeting summaries
- `Budget.xlsx` - financial data

### 2. Test Ingestion

1. Open http://localhost:3000
2. Click "Connect Google Drive"
3. Authorize the app
4. Click "Start Ingestion"
5. Watch the progress bar

### 3. Test Search

1. Type a query related to your documents
2. Verify relevant results appear
3. Check source attribution is correct

### 4. Test Filtering

1. Select a folder from dropdown
2. Search within that folder
3. Verify results are scoped correctly

## Evaluation Criteria

We'll evaluate based on:

1. **Functionality** (40%)
   - Does ingestion work?
   - Does search return relevant results?
   - Are sources properly attributed?

2. **Code Quality** (30%)
   - Clean, readable code
   - Proper error handling
   - Good abstraction

3. **Retrieval Quality** (20%)
   - Relevance of search results
   - Handling of folder hierarchy
   - Quality of snippets

4. **Execution Speed** (10%)
   - How much did you accomplish in 2-3 hours?
   - Good time management

## Helpful Resources

### Vector Databases
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Qdrant Docs](https://qdrant.tech/documentation/)

### Embeddings
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers](https://www.sbert.net/)

### Google Drive API
- [Drive API Reference](https://developers.google.com/drive/api/v3/reference)

## Submission

When you're done:

1. Create a GitHub repository
2. Add `@yuvbindal` and `@shayaansultan` as collaborators
3. Email us with:
   - Link to repository
   - Hours spent
   - Brief description of your approach
   - Any challenges or trade-offs

## FAQ

**Q: What if I can't finish in 2-3 hours?**
A: That's okay! Submit what you have. We care more about code quality and approach than completing everything.

**Q: Can I use AI coding assistants?**
A: Yes, but make sure you understand the code. We'll discuss your implementation.

**Q: Which vector DB should I use?**
A: ChromaDB is easiest for local development. Pinecone is great if you want cloud-hosted.

**Q: Do I need to implement chat?**
A: It's optional. Focus on ingestion and retrieval first. Chat is a bonus.

**Q: Can I modify the frontend?**
A: You can, but it's not necessary. Focus on backend implementation.

**Q: What about authentication persistence?**
A: The current implementation keeps credentials in memory. That's fine for this assessment.

## Project Structure

```
maven-drive-copilot/
├── frontend/                 # Complete React frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── hooks/           # React Query hooks
│   │   ├── types/           # TypeScript types
│   │   └── lib/             # API client
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── src/
│   │   ├── routes/          # API routes (complete)
│   │   ├── services/        # Services (YOU IMPLEMENT)
│   │   │   ├── drive_service.py        ✅ Complete
│   │   │   ├── ingestion_service.py    ⚠️ TODO
│   │   │   ├── retrieval_service.py    ⚠️ TODO
│   │   │   └── chat_service.py         ⚠️ TODO (optional)
│   │   ├── types/           # Pydantic models (complete)
│   │   └── main.py          # FastAPI app (complete)
│   └── requirements.txt
│
└── README.md                # This file
```

## Support

If you have questions about the assessment or run into setup issues, please email:
- yuv2bindal@gmail.com
- sultan.shayaan@gmail.com

Good luck! We're excited to see what you build.
