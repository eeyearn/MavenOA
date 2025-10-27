"""
Ingestion Service - Handles ingesting Google Drive files into vector database

This service:
1. Connects to Google Drive using the DriveService
2. Fetches all files and their content
3. Processes and chunks the content appropriately
4. Generates embeddings for each chunk
5. Stores chunks and embeddings in ChromaDB
"""

from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from .drive_service import drive_service
from ..types import IngestionStatus, MimeType
import PyPDF2
import io
import asyncio

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize ChromaDB client (persistent)
chroma_client = chromadb.PersistentClient(path="./chroma_db")


class IngestionService:
    """
    Service responsible for ingesting Google Drive files into a vector database.
    """

    def __init__(self):
        # Initialize vector database collection
        try:
            self.collection = chroma_client.get_collection(name="drive_documents")
        except:
            self.collection = chroma_client.create_collection(
                name="drive_documents",
                metadata={"hnsw:space": "cosine"}
            )

        # Status tracking
        self.is_ingesting = False
        self.total_files = 0
        self.processed_files = 0
        self.current_file = None
        self.error = None
        
    async def start_ingestion(self) -> Dict[str, str]:
        if self.is_ingesting:
            raise ValueError("Ingestion is already in progress.")

        try:
            print("==================================================")
            print("Starting ingestion process...")
            self.is_ingesting = True
            self.processed_files = 0
            self.total_files = 0
            self.current_file = "Fetching files from Drive..."
            self.error = None
            
            if not drive_service.is_authenticated():
                raise ValueError("Drive service is not authenticated. Please connect to Google Drive first.")

            print("Fetching files from Google Drive...")
            all_files = await asyncio.to_thread(drive_service.list_files)
            
            # =================================================================
            # FOR DEVELOPMENT: Filter for a specific folder to speed up testing
            # To use, set a folder name. To disable, set to None.
            # =================================================================
            target_folder_name = "Testing scripts" # <-- SET YOUR FOLDER NAME HERE
            # =================================================================

            files_to_process = []
            if target_folder_name:
                print(f"DEV MODE: Filtering for folder named '{target_folder_name}'")
                folders = [f for f in all_files if f['mimeType'] == 'application/vnd.google-apps.folder' and f['name'] == target_folder_name]
                if not folders:
                    print(f"WARNING: Could not find a folder named '{target_folder_name}'. Ingesting all files instead.")
                    files_to_process = all_files
                else:
                    target_folder_id = folders[0]['id']
                    print(f"Found folder '{target_folder_name}' with ID: {target_folder_id}")
                    files_to_process = [f for f in all_files if target_folder_id in f.get('parents', [])]
            else:
                files_to_process = all_files
            
            print(f"Successfully fetched {len(files_to_process)} total files to process from Drive")

            # --- THIS IS THE CORRECTED PART ---
            supported_mime_types = [
                'application/vnd.google-apps.document',  # Google Docs
                'application/vnd.google-apps.spreadsheet', # Google Sheets
                'application/pdf'                        # PDFs
            ]
            # ------------------------------------

            supported_files = [
                f for f in files_to_process
                if f.get('mimeType') in supported_mime_types
            ]
            
            self.total_files = len(supported_files)
            if self.total_files == 0:
                print("No supported files found to ingest in the target folder.")
                self.is_ingesting = False
                return {"message": "No supported files found to ingest."}

            print(f"Found {self.total_files} supported files to process")

            for i, file in enumerate(supported_files):
                self.current_file = file['name']
                self.processed_files = i + 1
                print(f"Processing: {self.current_file} ({self.processed_files}/{self.total_files})")
                
                text = await asyncio.to_thread(self._extract_text_from_file, file)

                if not text:
                    print(f"  Skipping '{self.current_file}' due to empty content.")
                    continue

                try:
                    file_path = await asyncio.to_thread(
                        drive_service.build_file_path,
                        file['id'],
                        file['name'],
                        file.get('parents')
                    )
                    
                    chunks = self._chunk_text(text, file, file_path)
                    if not chunks:
                        print(f"  No chunks created for '{self.current_file}'.")
                        continue
                    
                    print(f"  Created {len(chunks)} chunks")
                    
                    embeddings = await asyncio.to_thread(self._generate_embeddings, chunks)
                    print(f"  Generated embeddings")
                    
                    await asyncio.to_thread(self._store_in_vector_db, chunks, embeddings)
                    print(f"  Stored in vector database")

                except Exception as e:
                    print(f"  Error processing file {self.current_file}: {e}")

            print(f"Ingestion completed! Processed {self.processed_files}/{self.total_files} files")
            
        except Exception as e:
            self.error = str(e)
            print(f"Ingestion error: {self.error}")
        finally:
            self.is_ingesting = False
            self.current_file = None

        return {"message": "Ingestion completed successfully"}

    def get_status(self) -> IngestionStatus:
        """Get the current ingestion status."""
        return IngestionStatus(
            is_ingesting=self.is_ingesting,
            total_files=self.total_files,
            processed_files=self.processed_files,
            current_file=self.current_file,
            error=self.error
        )

    def _extract_text_from_file(self, file_metadata: dict) -> str:
        """
        Extract text content from a file based on its MIME type.
        
        Supports:
        - Google Docs (exported as plain text)
        - PDFs (using PyPDF2)
        - Google Sheets (exported as CSV)
        """
        mime_type = file_metadata.get('mimeType')
        file_id = file_metadata['id']
        
        try:
            if mime_type == MimeType.DOCUMENT:
                # Google Doc - export as plain text
                content_bytes = drive_service.export_google_doc(file_id, 'text/plain')
                return content_bytes.decode('utf-8', errors='ignore')
            
            elif mime_type == MimeType.SPREADSHEET:
                # Google Sheet - export as CSV
                content_bytes = drive_service.export_google_doc(file_id, 'text/csv')
                return content_bytes.decode('utf-8', errors='ignore')
            
            elif mime_type == MimeType.PDF:
                # PDF - use PyPDF2
                content_bytes = drive_service.download_file(file_id)
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content_bytes))
                
                text_parts = []
                for page in pdf_reader.pages:
                    text_parts.append(page.extract_text())
                
                return '\n\n'.join(text_parts)
            
            else:
                print(f"Unsupported MIME type: {mime_type}")
                return ""
                
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""

    def _chunk_text(self, text: str, file_metadata: dict, file_path: str) -> List[Dict[str, any]]:
        """
        Chunk text into smaller pieces for embedding.
        """
        chunk_size = 800
        chunk_overlap = 200
        
        final_chunks = []
        if not text or len(text.strip()) < 10:
            return final_chunks

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunk_data = {
                "text": chunk_text.strip(),
                "file_id": file_metadata['id'],
                "file_name": file_metadata['name'],
                "chunk_number": len(final_chunks),
                "path": file_path,
                "mime_type": file_metadata.get('mimeType'),
                "modified_time": file_metadata.get('modifiedTime'),
                "size": file_metadata.get('size'),
                "web_view_link": file_metadata.get('webViewLink'),
            }
            if 'parents' in file_metadata and file_metadata['parents']:
                chunk_data['folder_id'] = file_metadata['parents'][0]

            final_chunks.append(chunk_data)
            start += chunk_size - chunk_overlap
            
        return final_chunks

    def _generate_embeddings(self, chunks: List[Dict[str, any]]) -> List[List[float]]:
        """
        Generate embeddings for text chunks using OpenAI.
        """
        embeddings = []
        batch_size = 100
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk['text'] for chunk in batch]
            
            try:
                response = openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=texts
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error generating embeddings: {e}")
                embeddings.extend([[0.0] * 1536] * len(batch))
        
        return embeddings

    def _store_in_vector_db(self, chunks: List[Dict[str, any]], embeddings: List[List[float]]) -> None:
        """
        Store chunks and embeddings in ChromaDB.
        """
        try:
            ids = [f"{chunk['file_id']}_chunk_{chunk['chunk_number']}" for chunk in chunks]
            documents = [chunk['text'] for chunk in chunks]
            
            # Prepare metadata, ensuring all values are of a supported type
            metadatas = []
            for chunk in chunks:
                meta = {k: v for k, v in chunk.items() if k != 'text' and v is not None}
                metadatas.append(meta)

            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        except Exception as e:
            print(f"Error storing in vector DB: {e}")
            raise


# Global instance
ingestion_service = IngestionService()
