# Take Home Assessment - Google Drive Copilot

## Objective

Build backend services for a Google Drive copilot that can:
1. Ingest files from Google Drive into a vector database
2. Retrieve relevant document chunks based on queries
3. (Optional) Generate intelligent responses with source citations

**Time estimate: 2-3 hours**

## What's Already Built

### Frontend (Complete - No Changes Needed)
- Modern React UI with chat interface
- React Query hooks for API calls
- Folder/file selection
- Real-time ingestion progress
- Source attribution display

### Backend Infrastructure (Complete)
- FastAPI application setup
- Google OAuth flow (complete)
- API route handlers (complete)
- Type definitions (complete)

## Your Task

Implement **two core services** in the backend:

### 1. Ingestion Service (60-90 minutes)

**File:** `backend/src/services/ingestion_service.py`

**What to implement:**
- `start_ingestion()` - Main ingestion logic
- `_extract_text_from_file()` - Extract text from different file types
- `_chunk_text()` - Chunk documents intelligently
- `_generate_embeddings()` - Generate vector embeddings
- `_store_in_vector_db()` - Store chunks in vector database

**Requirements:**
- Connect to Google Drive using the provided `drive_service`
- Handle at minimum: Google Docs (other formats are bonus)
- Implement smart chunking (consider overlap, semantic boundaries)
- Generate embeddings using your choice of model
- Store in vector database with metadata (file_id, path, etc.)
- Update progress status during ingestion

**Deliverable:**
Users should be able to click "Start Ingestion" and see their Drive files processed into a searchable database.

### 2. Retrieval Service (45-60 minutes)

**File:** `backend/src/services/retrieval_service.py`

**What to implement:**
- `search()` - Search vector database for relevant chunks
- `_generate_query_embedding()` - Convert query to embedding
- `_format_results()` - Format results with source attribution
- `_create_snippet()` - Generate informative snippets
- `_extract_highlights()` - Highlight relevant terms

**Requirements:**
- Search vector database using query embeddings
- Support filtering by `folder_id` and `file_id`
- Return results with proper source attribution
- Include relevance scores
- Generate useful snippets (not too short/long)
- Limit results (default: 10)

**Deliverable:**
Users should be able to search and get relevant results with clear source attribution.

### 3. Chat Service (Optional - 30-45 minutes)

**File:** `backend/src/services/chat_service.py`

**What to implement:**
- `chat()` - Handle chat messages with context
- `_build_context()` - Build context from search results
- `_generate_response()` - Generate LLM response

**Requirements:**
- Use retrieval service to find relevant chunks
- Build context for LLM
- Generate accurate responses
- Cite sources in responses
- Handle conversation history

**Deliverable:**
Users should be able to ask questions and get intelligent answers citing specific documents.

## Technical Choices

You need to choose:

### Vector Database (pick one)
- **ChromaDB** - Easiest, runs locally, no signup needed
- **Pinecone** - Cloud-hosted, requires API key
- **Qdrant** - Can run locally or cloud
- **Weaviate** - Feature-rich option

### Embedding Model (pick one)
- **OpenAI Embeddings** - Best quality, requires API key
- **Sentence Transformers** - Free, runs locally
- **Cohere** - Good alternative to OpenAI

### LLM for Chat (pick one, if implementing chat)
- **OpenAI GPT-4/3.5** - Most popular
- **Anthropic Claude** - Great for long context
- **Cohere** - Good alternative

## Implementation Tips

### Minimum Viable Implementation

For a 2-hour implementation, focus on:

1. **Ingestion:**
   - Google Docs only (use `drive_service.export_google_doc()`)
   - Simple fixed-size chunks (500 chars, 100 char overlap)
   - Basic metadata (file_id, file_name, path)

2. **Retrieval:**
   - Basic semantic search
   - Top 5-10 results
   - Simple snippets (first 200 chars of chunk)

3. **Skip:**
   - Complex file type handling
   - Advanced chunking strategies
   - Chat service (implement search first)

### Suggested Order

1. **Setup** (15 min)
   - Choose vector DB and embedding model
   - Install dependencies
   - Configure API keys

2. **Basic Ingestion** (45 min)
   - Fetch files from Drive
   - Extract text from Google Docs
   - Simple chunking
   - Store in vector DB

3. **Basic Retrieval** (30 min)
   - Query embedding generation
   - Vector search
   - Format results

4. **Testing** (15 min)
   - Create test files in Drive
   - Run ingestion
   - Test searches

5. **Polish** (15 min)
   - Add filtering support
   - Improve snippets
   - Error handling

## Evaluation Criteria

### Core Functionality (50%)
- ✅ Ingestion completes successfully
- ✅ Search returns relevant results
- ✅ Source attribution is accurate
- ✅ Filtering by folder/file works

### Code Quality (30%)
- ✅ Clean, readable code
- ✅ Good abstractions
- ✅ Proper error handling
- ✅ Type hints used correctly

### Retrieval Quality (20%)
- ✅ Results are relevant to query
- ✅ Folder hierarchy respected
- ✅ Good snippet quality
- ✅ Reasonable relevance scores

## What We're NOT Evaluating

- Frontend changes (use the provided UI)
- Production-readiness (this is a prototype)
- Authentication persistence (in-memory is fine)
- Handling all file types (focus on Docs)
- Advanced re-ranking algorithms
- Scalability to millions of documents

## Testing Your Work

### 1. Setup Test Data

Create these files in your Google Drive:
```
My Drive/
├── Projects/
│   ├── Project Alpha.docx - "Project Alpha is our Q1 initiative..."
│   └── Project Beta.docx - "Project Beta focuses on..."
└── Notes/
    └── Meeting Notes.docx - "Today's meeting covered..."
```

### 2. Test Ingestion

1. Start the app and authenticate
2. Click "Start Ingestion"
3. Verify all files are processed
4. Check progress updates work

### 3. Test Search

1. Query: "Project Alpha"
   - Should return Project Alpha.docx
2. Query: "meeting"
   - Should return Meeting Notes.docx
3. Select "Projects" folder
   - Should only return project files

### 4. Test Edge Cases

1. Empty query
2. Query with no results
3. Very long query
4. Special characters

## Common Pitfalls

1. **Forgetting metadata** - Store file path, name, ID with each chunk
2. **No chunking** - Embedding entire documents reduces quality
3. **Ignoring filters** - Support folder_id and file_id filtering
4. **Poor snippets** - Don't just return raw chunk text
5. **Missing error handling** - Handle API failures gracefully

## Submission Checklist

Before submitting, ensure:

- [ ] Code is committed to GitHub
- [ ] README includes setup instructions
- [ ] Dependencies are listed in requirements.txt
- [ ] .env.example shows required variables
- [ ] Code is commented where needed
- [ ] Basic error handling is implemented
- [ ] Ingestion works end-to-end
- [ ] Search returns relevant results
- [ ] You've logged your hours

## Questions During Assessment?

If you encounter setup issues or have clarifying questions:
- Email: yuv2bindal@gmail.com, sultan.shayaan@gmail.com
- We'll respond quickly to unblock you

## After Submission

We'll review your code and:
1. Test it on our own Google Drive
2. Evaluate based on criteria above
3. Schedule a follow-up discussion

During the discussion, be ready to:
- Walk through your implementation
- Explain technical choices
- Discuss trade-offs you made
- Suggest improvements

## Good Luck!

Remember:
- Focus on core functionality first
- Simple implementations are fine
- We value clean code over complex features
- It's okay if you don't finish everything

We're excited to see your approach to this problem!
