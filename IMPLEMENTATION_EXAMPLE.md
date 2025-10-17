# Implementation Example

This guide shows a minimal working implementation using ChromaDB and OpenAI. Use this as reference for your own implementation.

## Example: Ingestion Service with ChromaDB + OpenAI

```python
# backend/src/services/ingestion_service.py

from typing import List, Dict
import chromadb
from chromadb.config import Settings
from openai import OpenAI
import os
from .drive_service import drive_service
from ..types import IngestionStatus

class IngestionService:
    def __init__(self):
        # Initialize ChromaDB client
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False
        ))

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="drive_documents",
            metadata={"hnsw:space": "cosine"}
        )

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Status tracking
        self.is_ingesting = False
        self.total_files = 0
        self.processed_files = 0
        self.current_file = None
        self.error = None

    async def start_ingestion(self) -> Dict[str, str]:
        """Main ingestion logic"""
        self.is_ingesting = True
        self.processed_files = 0
        self.error = None

        try:
            # Step 1: Get all files from Drive
            files = drive_service.list_files()
            self.total_files = len(files)

            # Step 2: Process each file
            for file in files:
                try:
                    self.current_file = file['name']

                    # Extract text based on file type
                    text = self._extract_text_from_file(file)

                    if not text or len(text.strip()) < 10:
                        # Skip empty files
                        self.processed_files += 1
                        continue

                    # Chunk the text
                    chunks = self._chunk_text(text, file)

                    # Generate embeddings and store
                    if chunks:
                        self._store_chunks(chunks, file)

                    self.processed_files += 1

                except Exception as e:
                    print(f"Error processing {file['name']}: {str(e)}")
                    # Continue with next file
                    self.processed_files += 1
                    continue

            return {"message": f"Successfully ingested {self.processed_files} files"}

        except Exception as e:
            self.error = str(e)
            raise
        finally:
            self.is_ingesting = False
            self.current_file = None

    def _extract_text_from_file(self, file_metadata: dict) -> str:
        """Extract text from different file types"""
        mime_type = file_metadata['mimeType']
        file_id = file_metadata['id']

        try:
            # Handle Google Docs
            if mime_type == 'application/vnd.google-apps.document':
                content = drive_service.export_google_doc(file_id, 'text/plain')
                return content.decode('utf-8')

            # Handle Google Sheets
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                content = drive_service.export_google_doc(file_id, 'text/csv')
                return content.decode('utf-8')

            # Handle plain text
            elif mime_type.startswith('text/'):
                content = drive_service.download_file(file_id)
                return content.decode('utf-8')

            # Skip other types for now
            else:
                return ""

        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""

    def _chunk_text(self, text: str, file_metadata: dict) -> List[Dict]:
        """Simple fixed-size chunking with overlap"""
        chunk_size = 500
        overlap = 100
        chunks = []

        # Clean the text
        text = text.strip()

        # Create chunks
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            # Build file path
            path = drive_service.build_file_path(
                file_metadata['id'],
                file_metadata['name'],
                file_metadata.get('parents')
            )

            chunks.append({
                'text': chunk_text,
                'file_id': file_metadata['id'],
                'file_name': file_metadata['name'],
                'mime_type': file_metadata['mimeType'],
                'path': path,
                'modified_time': file_metadata['modifiedTime'],
                'web_view_link': file_metadata.get('webViewLink'),
                'chunk_index': chunk_index,
                'start_char': start,
                'end_char': end
            })

            chunk_index += 1
            start += chunk_size - overlap

        return chunks

    def _store_chunks(self, chunks: List[Dict], file_metadata: dict):
        """Store chunks in ChromaDB"""
        # Prepare data for ChromaDB
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [{
            'file_id': chunk['file_id'],
            'file_name': chunk['file_name'],
            'mime_type': chunk['mime_type'],
            'path': chunk['path'],
            'modified_time': chunk['modified_time'],
            'web_view_link': chunk.get('web_view_link', ''),
            'chunk_index': chunk['chunk_index']
        } for chunk in chunks]
        ids = [f"{file_metadata['id']}_chunk_{chunk['chunk_index']}"
               for chunk in chunks]

        # Generate embeddings
        embeddings = self._generate_embeddings([chunk['text'] for chunk in chunks])

        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",  # or "text-embedding-ada-002"
            input=texts
        )
        return [item.embedding for item in response.data]

    def get_status(self) -> IngestionStatus:
        """Get current status"""
        return IngestionStatus(
            isIngesting=self.is_ingesting,
            totalFiles=self.total_files,
            processedFiles=self.processed_files,
            currentFile=self.current_file,
            error=self.error
        )

# Global instance
ingestion_service = IngestionService()
```

## Example: Retrieval Service

```python
# backend/src/services/retrieval_service.py

from typing import List
from openai import OpenAI
import os
import chromadb
from chromadb.config import Settings
from ..types import SearchRequest, SearchResult, DriveFile

class RetrievalService:
    def __init__(self):
        # Use same ChromaDB client
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False
        ))
        self.collection = self.chroma_client.get_or_create_collection(
            name="drive_documents",
            metadata={"hnsw:space": "cosine"}
        )

        # OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Search for relevant documents"""
        # Generate query embedding
        query_embedding = self._generate_query_embedding(request.query)

        # Build metadata filter
        where_filter = {}
        if request.file_id:
            where_filter['file_id'] = request.file_id
        # Note: folder filtering requires checking if path contains folder

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=request.limit or 10,
            where=where_filter if where_filter else None
        )

        # Format results
        return self._format_results(results, request)

    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for query"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return response.data[0].embedding

    def _format_results(self, raw_results: dict, request: SearchRequest) -> List[SearchResult]:
        """Format ChromaDB results"""
        formatted = []

        if not raw_results['ids'] or not raw_results['ids'][0]:
            return []

        # ChromaDB returns lists of lists
        ids = raw_results['ids'][0]
        documents = raw_results['documents'][0]
        metadatas = raw_results['metadatas'][0]
        distances = raw_results['distances'][0]

        for i in range(len(ids)):
            metadata = metadatas[i]

            # Apply folder filter if needed
            if request.folder_id:
                # Simple check: does the path contain the folder?
                # More robust: you'd need to track folder hierarchy
                if request.folder_id not in metadata.get('path', ''):
                    continue

            # Build DriveFile object
            file = DriveFile(
                id=metadata['file_id'],
                name=metadata['file_name'],
                mimeType=metadata['mime_type'],
                path=metadata['path'],
                modifiedTime=metadata['modified_time'],
                webViewLink=metadata.get('web_view_link')
            )

            # Create snippet
            snippet = self._create_snippet(documents[i], request.query)

            # Convert distance to relevance score (0-1)
            # ChromaDB uses cosine distance, lower is better
            relevance = max(0, 1 - distances[i])

            # Extract highlights
            highlights = self._extract_highlights(documents[i], request.query)

            result = SearchResult(
                file=file,
                snippet=snippet,
                relevanceScore=relevance,
                highlights=highlights
            )

            formatted.append(result)

        return formatted

    def _create_snippet(self, text: str, query: str, max_length: int = 200) -> str:
        """Create snippet around query terms"""
        # Simple implementation: truncate to max_length
        if len(text) <= max_length:
            return text

        # Try to find query in text
        query_lower = query.lower()
        text_lower = text.lower()

        # Find query position
        pos = text_lower.find(query_lower)

        if pos == -1:
            # Query not found, return beginning
            return text[:max_length] + "..."

        # Center snippet around query
        start = max(0, pos - max_length // 2)
        end = min(len(text), start + max_length)

        snippet = text[start:end]

        # Add ellipsis
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet

    def _extract_highlights(self, text: str, query: str, max_highlights: int = 3) -> List[str]:
        """Extract highlighted phrases"""
        # Simple implementation: find query terms in text
        highlights = []
        query_terms = query.lower().split()

        for term in query_terms[:max_highlights]:
            if term in text.lower():
                # Find the term with context
                pos = text.lower().find(term)
                start = max(0, pos - 20)
                end = min(len(text), pos + len(term) + 20)
                highlight = text[start:end].strip()
                highlights.append(highlight)

        return highlights[:max_highlights]

# Global instance
retrieval_service = RetrievalService()
```

## Key Points

1. **ChromaDB** runs in-memory by default (no separate setup needed)
2. **OpenAI embeddings** use the `text-embedding-3-small` model (cheaper and faster)
3. **Simple chunking** with fixed size and overlap
4. **Metadata** stored with each chunk for filtering
5. **Distance to relevance** conversion for scores

## Alternative: Using Sentence Transformers (Free)

If you don't want to use OpenAI:

```python
from sentence_transformers import SentenceTransformer

class IngestionService:
    def __init__(self):
        # ... other setup ...
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.embedding_model.encode(texts)
        return embeddings.tolist()
```

## Testing Your Implementation

```python
# Test ingestion
await ingestion_service.start_ingestion()

# Test search
from types import SearchRequest
request = SearchRequest(query="project", limit=5)
results = await retrieval_service.search(request)
print(f"Found {len(results)} results")
```

Good luck with your implementation!
