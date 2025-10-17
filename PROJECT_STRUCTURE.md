# Project Structure

```
maven-drive-copilot/
│
├── README.md                          # Main project documentation
├── ASSESSMENT.md                      # Assessment details and requirements
├── SETUP_GUIDE.md                     # Step-by-step setup instructions
├── IMPLEMENTATION_EXAMPLE.md          # Example implementations for reference
├── PROJECT_STRUCTURE.md               # This file
├── .gitignore                         # Git ignore rules
│
├── frontend/                          # React Frontend (COMPLETE ✅)
│   ├── package.json                   # Frontend dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── tsconfig.node.json             # TypeScript config for Vite
│   ├── vite.config.ts                 # Vite bundler configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── postcss.config.js              # PostCSS configuration
│   ├── index.html                     # HTML entry point
│   ├── .gitignore                     # Frontend gitignore
│   │
│   └── src/
│       ├── main.tsx                   # Application entry point
│       ├── App.tsx                    # Main App component
│       ├── index.css                  # Global styles
│       │
│       ├── components/                # React components
│       │   ├── ChatInterface.tsx      # Chat UI with message history
│       │   ├── SourceCard.tsx         # Display search result sources
│       │   ├── IngestionPanel.tsx     # Ingestion status and controls
│       │   └── AuthButton.tsx         # Google OAuth button
│       │
│       ├── hooks/                     # React Query hooks
│       │   └── useDrive.ts            # All API hooks (auth, files, search, chat)
│       │
│       ├── lib/                       # Utilities and API client
│       │   └── api.ts                 # Axios API client with typed endpoints
│       │
│       └── types/                     # TypeScript type definitions
│           └── index.ts               # All frontend types
│
└── backend/                           # FastAPI Backend
    ├── requirements.txt               # Python dependencies
    ├── .env.example                   # Environment variables template
    ├── .gitignore                     # Backend gitignore
    │
    └── src/
        ├── __init__.py                # Package marker
        ├── main.py                    # FastAPI app entry point ✅
        │
        ├── routes/                    # API route handlers (ALL COMPLETE ✅)
        │   ├── __init__.py
        │   ├── auth.py                # Google OAuth endpoints
        │   ├── drive.py               # Drive file/folder listing
        │   ├── ingest.py              # Ingestion control endpoints
        │   ├── search.py              # Search endpoint
        │   └── chat.py                # Chat endpoint
        │
        ├── services/                  # Business logic services
        │   ├── __init__.py
        │   ├── drive_service.py       # Google Drive integration ✅ COMPLETE
        │   ├── ingestion_service.py   # ⚠️  TODO: Implement ingestion logic
        │   ├── retrieval_service.py   # ⚠️  TODO: Implement search logic
        │   └── chat_service.py        # ⚠️  TODO: Implement chat logic (optional)
        │
        ├── types/                     # Pydantic models (COMPLETE ✅)
        │   └── __init__.py            # All type definitions
        │
        └── utils/                     # Utility functions
            └── __init__.py            # Helper functions
```

## File Descriptions

### Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Main project overview and quick start | ✅ Complete |
| `ASSESSMENT.md` | Detailed assessment requirements | ✅ Complete |
| `SETUP_GUIDE.md` | Step-by-step setup instructions | ✅ Complete |
| `IMPLEMENTATION_EXAMPLE.md` | Reference implementation examples | ✅ Complete |
| `PROJECT_STRUCTURE.md` | This file | ✅ Complete |

### Frontend Files (All Complete ✅)

| File | Purpose | Lines | Complexity |
|------|---------|-------|------------|
| `src/main.tsx` | App entry, React Query setup | ~20 | Simple |
| `src/App.tsx` | Main layout and routing | ~50 | Simple |
| `src/components/ChatInterface.tsx` | Chat UI with context selection | ~180 | Medium |
| `src/components/SourceCard.tsx` | Source attribution display | ~60 | Simple |
| `src/components/IngestionPanel.tsx` | Ingestion status UI | ~100 | Simple |
| `src/components/AuthButton.tsx` | OAuth button | ~30 | Simple |
| `src/hooks/useDrive.ts` | React Query hooks for all APIs | ~80 | Medium |
| `src/lib/api.ts` | Axios client with typed endpoints | ~60 | Simple |
| `src/types/index.ts` | TypeScript type definitions | ~60 | Simple |

### Backend Files

#### Complete Files ✅

| File | Purpose | Lines | Key Functions |
|------|---------|-------|---------------|
| `src/main.py` | FastAPI app setup, CORS, routes | ~60 | App initialization |
| `src/routes/auth.py` | OAuth flow endpoints | ~30 | `/auth/google`, `/auth/callback` |
| `src/routes/drive.py` | File/folder listing | ~120 | `/drive/files`, `/drive/folders` |
| `src/routes/ingest.py` | Ingestion endpoints | ~40 | `/ingest/start`, `/ingest/status` |
| `src/routes/search.py` | Search endpoint | ~30 | `/search` |
| `src/routes/chat.py` | Chat endpoint | ~30 | `/chat` |
| `src/services/drive_service.py` | Google Drive integration | ~150 | File listing, download, export |
| `src/types/__init__.py` | Pydantic models | ~100 | All type definitions |

#### Files to Implement ⚠️

| File | Purpose | Est. Lines | Key Methods to Implement |
|------|---------|-----------|--------------------------|
| `src/services/ingestion_service.py` | Ingest files to vector DB | ~150-200 | `start_ingestion()`, `_extract_text_from_file()`, `_chunk_text()`, `_generate_embeddings()`, `_store_in_vector_db()` |
| `src/services/retrieval_service.py` | Search vector DB | ~100-150 | `search()`, `_generate_query_embedding()`, `_format_results()`, `_create_snippet()` |
| `src/services/chat_service.py` | Generate responses with LLM | ~80-120 | `chat()`, `_build_context()`, `_generate_response()` |

## API Endpoints

### Complete Endpoints ✅

| Method | Endpoint | Purpose | Handler |
|--------|----------|---------|---------|
| GET | `/` | Health check | `main.py:root()` |
| GET | `/api/health` | Detailed health | `main.py:health()` |
| GET | `/api/auth/google` | Get OAuth URL | `auth.py:get_auth_url()` |
| GET | `/api/auth/callback` | OAuth callback | `auth.py:auth_callback()` |
| GET | `/api/drive/files` | List all files | `drive.py:list_files()` |
| GET | `/api/drive/folders` | List all folders | `drive.py:list_folders()` |
| GET | `/api/drive/folders/{id}` | Get folder details | `drive.py:get_folder()` |
| POST | `/api/ingest/start` | Start ingestion | `ingest.py:start_ingestion()` |
| GET | `/api/ingest/status` | Get ingestion status | `ingest.py:get_ingestion_status()` |

### Endpoints Needing Implementation ⚠️

| Method | Endpoint | Purpose | Service Method |
|--------|----------|---------|----------------|
| POST | `/api/search` | Search documents | `retrieval_service.search()` |
| POST | `/api/chat` | Chat with documents | `chat_service.chat()` |

## Type Definitions

### Frontend Types (`frontend/src/types/index.ts`)

- `DriveFile` - Google Drive file metadata
- `DriveFolder` - Folder with file count
- `SearchResult` - Search result with snippet and relevance
- `ChatMessage` - Chat message with sources
- `IngestionStatus` - Ingestion progress
- `SearchRequest` - Search query parameters
- `ChatRequest` - Chat message with context
- `ChatResponse` - Response with sources

### Backend Types (`backend/src/types/__init__.py`)

- `MimeType` - Google Drive MIME types enum
- `DriveFile` - Pydantic model for files
- `DriveFolder` - Pydantic model for folders
- `SearchResult` - Search result model
- `ChatMessage` - Chat message model
- `IngestionStatus` - Ingestion status model
- `SearchRequest` - Search request model
- `ChatRequest` - Chat request model
- `ChatResponse` - Chat response model

## Data Flow

### Ingestion Flow
```
User clicks "Start Ingestion"
  ↓
Frontend: POST /api/ingest/start
  ↓
Backend: ingest.py:start_ingestion()
  ↓
Backend: ingestion_service.start_ingestion() ⚠️ YOU IMPLEMENT
  ↓
  - Fetch files from Drive (drive_service)
  - Extract text from each file
  - Chunk text
  - Generate embeddings
  - Store in vector DB
  ↓
Frontend polls: GET /api/ingest/status
  ↓
Display progress to user
```

### Search Flow
```
User types query and hits search
  ↓
Frontend: POST /api/search
  ↓
Backend: search.py:search_documents()
  ↓
Backend: retrieval_service.search() ⚠️ YOU IMPLEMENT
  ↓
  - Generate query embedding
  - Search vector DB
  - Apply filters (folder/file)
  - Format results
  ↓
Frontend displays results with sources
```

### Chat Flow
```
User sends chat message
  ↓
Frontend: POST /api/chat
  ↓
Backend: chat.py:chat()
  ↓
Backend: chat_service.chat() ⚠️ YOU IMPLEMENT
  ↓
  - Use retrieval_service to find context
  - Build prompt with context
  - Call LLM
  - Format response
  ↓
Frontend displays message with sources
```

## Dependencies

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Query** - Server state management
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend (Installed)
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Google Auth** - OAuth integration
- **Google API Client** - Drive API

### Backend (You Choose)
- **Vector DB**: ChromaDB / Pinecone / Qdrant / Weaviate
- **Embeddings**: OpenAI / Sentence Transformers / Cohere
- **LLM**: OpenAI / Anthropic / Cohere

## Configuration

### Environment Variables

Required in `backend/.env`:
```env
GOOGLE_CLIENT_ID=<from Google Cloud Console>
GOOGLE_CLIENT_SECRET=<from Google Cloud Console>
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/callback
```

Optional (based on your choices):
```env
OPENAI_API_KEY=<if using OpenAI>
PINECONE_API_KEY=<if using Pinecone>
COHERE_API_KEY=<if using Cohere>
```

## Quick Reference

### What's Done
- ✅ Complete frontend with React Query
- ✅ All API routes and endpoints
- ✅ Google OAuth integration
- ✅ Type definitions (frontend & backend)
- ✅ Google Drive service (list, download, export)
- ✅ Project documentation

### What You Do
- ⚠️ Choose vector DB and embedding model
- ⚠️ Implement `ingestion_service.py`
- ⚠️ Implement `retrieval_service.py`
- ⚠️ (Optional) Implement `chat_service.py`
- ⚠️ Test with your Google Drive

### Time Breakdown (2-3 hours)
- Setup: 15-30 min
- Ingestion: 60-90 min
- Retrieval: 45-60 min
- Testing: 15-30 min

Good luck with your implementation!
