# Implementation Checklist

Use this checklist to track your progress through the assessment.

## Setup Phase (15-30 minutes)

### Google Cloud Setup
- [ ] Create Google Cloud project
- [ ] Enable Google Drive API
- [ ] Create OAuth 2.0 credentials
- [ ] Add yourself as test user
- [ ] Copy Client ID and Client Secret

### Project Setup
- [ ] Clone/download project
- [ ] Review project structure
- [ ] Read README.md and ASSESSMENT.md

### Backend Setup
- [ ] Create Python virtual environment
- [ ] Install base requirements: `pip install -r requirements.txt`
- [ ] Choose vector database (ChromaDB/Pinecone/Qdrant)
- [ ] Install vector DB: `pip install chromadb` (or your choice)
- [ ] Choose embedding provider (OpenAI/Sentence Transformers/Cohere)
- [ ] Install embedding library: `pip install openai` (or your choice)
- [ ] Copy `.env.example` to `.env`
- [ ] Add Google OAuth credentials to `.env`
- [ ] Add API keys for vector DB and embeddings to `.env`
- [ ] Test backend starts: `python -m src.main`

### Frontend Setup
- [ ] Navigate to frontend directory
- [ ] Install dependencies: `npm install`
- [ ] Test frontend starts: `npm run dev`
- [ ] Verify http://localhost:3000 loads

### Integration Test
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Click "Connect Google Drive"
- [ ] Complete OAuth flow
- [ ] Return to app successfully

## Implementation Phase (90-120 minutes)

### Phase 1: Ingestion Service (60-90 min)

File: `backend/src/services/ingestion_service.py`

#### Basic Setup
- [ ] Initialize vector database client in `__init__`
- [ ] Initialize embedding model in `__init__`
- [ ] Verify clients connect successfully

#### Extract Text Method
- [ ] Implement `_extract_text_from_file()` for Google Docs
- [ ] Handle `application/vnd.google-apps.document` MIME type
- [ ] Use `drive_service.export_google_doc()` to get content
- [ ] Decode bytes to UTF-8 string
- [ ] (Bonus) Handle Google Sheets
- [ ] (Bonus) Handle plain text files
- [ ] Test with a sample file

#### Chunking Method
- [ ] Implement `_chunk_text()` with fixed-size chunks
- [ ] Set chunk size (recommended: 500 characters)
- [ ] Set overlap (recommended: 100 characters)
- [ ] Include metadata in each chunk:
  - [ ] `file_id`
  - [ ] `file_name`
  - [ ] `mime_type`
  - [ ] `path` (use `drive_service.build_file_path()`)
  - [ ] `modified_time`
  - [ ] `web_view_link`
  - [ ] `chunk_index`
- [ ] Test chunking with sample text

#### Embedding Method
- [ ] Implement `_generate_embeddings()`
- [ ] Call your chosen embedding API/model
- [ ] Handle batch processing if needed
- [ ] Return list of embedding vectors
- [ ] Test with sample texts

#### Storage Method
- [ ] Implement `_store_in_vector_db()`
- [ ] Format data for your vector DB
- [ ] Store embeddings with metadata
- [ ] Handle batch inserts
- [ ] Test storage and verify in DB

#### Main Ingestion Logic
- [ ] Implement `start_ingestion()`
- [ ] Set `self.is_ingesting = True` at start
- [ ] Fetch files using `drive_service.list_files()`
- [ ] Set `self.total_files`
- [ ] Loop through each file:
  - [ ] Update `self.current_file`
  - [ ] Extract text
  - [ ] Skip if text is empty/too short
  - [ ] Chunk text
  - [ ] Generate embeddings
  - [ ] Store in vector DB
  - [ ] Increment `self.processed_files`
- [ ] Handle errors gracefully
- [ ] Set `self.is_ingesting = False` when done
- [ ] Return success message

#### Ingestion Testing
- [ ] Create 2-3 test documents in Google Drive
- [ ] Start backend server
- [ ] Start frontend
- [ ] Click "Start Ingestion"
- [ ] Verify progress bar updates
- [ ] Check all files are processed
- [ ] Verify no errors
- [ ] Check data exists in vector DB

### Phase 2: Retrieval Service (45-60 min)

File: `backend/src/services/retrieval_service.py`

#### Basic Setup
- [ ] Initialize vector database client in `__init__`
- [ ] Initialize embedding model in `__init__`
- [ ] Should use same DB as ingestion service

#### Query Embedding Method
- [ ] Implement `_generate_query_embedding()`
- [ ] Use same model as ingestion
- [ ] Handle single query string
- [ ] Return embedding vector
- [ ] Test with sample query

#### Search Method
- [ ] Implement `search()`
- [ ] Generate query embedding
- [ ] Prepare metadata filters
- [ ] Query vector database:
  - [ ] Use query embedding
  - [ ] Apply `file_id` filter if provided
  - [ ] Apply `folder_id` filter if provided
  - [ ] Limit results to `request.limit`
- [ ] Format results using `_format_results()`
- [ ] Return list of SearchResult objects

#### Format Results Method
- [ ] Implement `_format_results()`
- [ ] Extract raw results from vector DB response
- [ ] For each result:
  - [ ] Build `DriveFile` object from metadata
  - [ ] Create snippet using `_create_snippet()`
  - [ ] Convert distance to relevance score (0-1)
  - [ ] Extract highlights using `_extract_highlights()`
  - [ ] Build `SearchResult` object
- [ ] Return formatted results

#### Snippet Creation Method
- [ ] Implement `_create_snippet()`
- [ ] Set max length (recommended: 200 characters)
- [ ] Find query terms in text
- [ ] Center snippet around query if found
- [ ] Truncate at word boundaries
- [ ] Add ellipsis where appropriate
- [ ] Return snippet string

#### Highlights Method
- [ ] Implement `_extract_highlights()`
- [ ] Split query into terms
- [ ] Find terms in text
- [ ] Extract context around each term
- [ ] Return list of highlights (max 3-5)

#### Retrieval Testing
- [ ] Backend running with ingested data
- [ ] Frontend open
- [ ] Test basic search:
  - [ ] Enter query related to your documents
  - [ ] Verify relevant results appear
  - [ ] Check source attribution is correct
  - [ ] Verify snippets are informative
- [ ] Test folder filtering:
  - [ ] Select a folder from dropdown
  - [ ] Verify results are scoped to folder
- [ ] Test file filtering:
  - [ ] Select a specific file
  - [ ] Verify results only from that file
- [ ] Test edge cases:
  - [ ] Query with no results
  - [ ] Very short query
  - [ ] Very long query

### Phase 3: Chat Service (Optional, 30-45 min)

File: `backend/src/services/chat_service.py`

#### Basic Setup
- [ ] Choose LLM provider (OpenAI/Anthropic/Cohere)
- [ ] Initialize LLM client in `__init__`
- [ ] Add API key to `.env`

#### Context Building Method
- [ ] Implement `_build_context()`
- [ ] Format search results into context string
- [ ] Include source attribution
- [ ] Keep context under token limit
- [ ] Return formatted context

#### Response Generation Method
- [ ] Implement `_generate_response()`
- [ ] Build system prompt
- [ ] Add conversation history if provided
- [ ] Add context from documents
- [ ] Add user question
- [ ] Call LLM API
- [ ] Extract response text
- [ ] Return response

#### Main Chat Method
- [ ] Implement `chat()`
- [ ] Create `SearchRequest` from chat message
- [ ] Call `retrieval_service.search()`
- [ ] Build context from results
- [ ] Generate response
- [ ] Return `ChatResponse` with message and sources

#### Chat Testing
- [ ] Test basic question answering
- [ ] Verify sources are cited
- [ ] Test with conversation history
- [ ] Test with folder/file context

## Testing Phase (15-30 minutes)

### Functional Testing
- [ ] End-to-end ingestion works
- [ ] Search returns relevant results
- [ ] Source attribution is accurate
- [ ] Folder filtering works correctly
- [ ] File filtering works correctly
- [ ] (If implemented) Chat generates good responses
- [ ] (If implemented) Chat cites sources correctly

### Error Handling
- [ ] Handle empty Drive gracefully
- [ ] Handle network errors
- [ ] Handle API rate limits
- [ ] Handle invalid queries
- [ ] Display errors to user appropriately

### Edge Cases
- [ ] Very large files
- [ ] Files with no text content
- [ ] Duplicate file names
- [ ] Deep folder hierarchies
- [ ] Special characters in file names

### Code Quality
- [ ] Remove debug print statements
- [ ] Add helpful comments
- [ ] Use type hints consistently
- [ ] Handle exceptions properly
- [ ] Clean up unused imports

## Submission Phase (15 minutes)

### Code Cleanup
- [ ] Remove any hardcoded credentials
- [ ] Remove debug/test code
- [ ] Format code consistently
- [ ] Add docstrings to key methods
- [ ] Update .env.example with new variables

### Documentation
- [ ] Update README if you made changes
- [ ] Document your architecture choices
- [ ] Note any assumptions made
- [ ] List known limitations
- [ ] Add setup instructions for your specific stack

### Repository Setup
- [ ] Create GitHub repository
- [ ] Add all files to git
- [ ] Create .gitignore if not exists
- [ ] Commit all changes
- [ ] Push to GitHub
- [ ] Add @yuvbindal and @shayaansultan as collaborators

### Submission Email
- [ ] Link to GitHub repository
- [ ] Hours spent breakdown:
  - [ ] Setup: ___ hours
  - [ ] Ingestion: ___ hours
  - [ ] Retrieval: ___ hours
  - [ ] Chat: ___ hours (if implemented)
  - [ ] Testing: ___ hours
  - [ ] Total: ___ hours
- [ ] Brief description of approach
- [ ] Vector DB choice and why
- [ ] Embedding model choice and why
- [ ] LLM choice and why (if implemented)
- [ ] Challenges encountered
- [ ] Trade-offs made
- [ ] What you'd improve with more time

## Time Check

After each phase, check your time:
- [ ] Setup complete: ____ min (target: 15-30)
- [ ] Ingestion complete: ____ min (target: 60-90)
- [ ] Retrieval complete: ____ min (target: 45-60)
- [ ] Chat complete: ____ min (target: 30-45, optional)
- [ ] Testing complete: ____ min (target: 15-30)
- [ ] Total time: ____ hours (target: 2-3)

## Quick Wins If Running Out of Time

If you're running short on time, prioritize:

1. **Must Have:**
   - [ ] Ingestion works for Google Docs
   - [ ] Basic search works
   - [ ] Results have file metadata

2. **Should Have:**
   - [ ] Folder filtering
   - [ ] Good snippets
   - [ ] Relevance scores

3. **Nice to Have:**
   - [ ] File filtering
   - [ ] Highlight extraction
   - [ ] Chat service

4. **Bonus:**
   - [ ] Multiple file type support
   - [ ] Advanced chunking
   - [ ] Re-ranking

Remember: A working simple implementation is better than an incomplete complex one!

## Final Checks

Before submitting:
- [ ] Code runs without errors
- [ ] All services work end-to-end
- [ ] No credentials committed to git
- [ ] README is accurate
- [ ] Email is sent with all required info

Good luck! 🚀
