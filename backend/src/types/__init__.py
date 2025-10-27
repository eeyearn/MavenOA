from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MimeType(str, Enum):
    """Common Google Drive MIME types"""
    DOCUMENT = "application/vnd.google-apps.document"
    SPREADSHEET = "application/vnd.google-apps.spreadsheet"
    PRESENTATION = "application/vnd.google-apps.presentation"
    PDF = "application/pdf"
    FOLDER = "application/vnd.google-apps.folder"
    VIDEO = "video/mp4"
    AUDIO = "audio/mpeg"


class DriveFile(BaseModel):
    """Represents a Google Drive file"""
    id: str
    name: str
    mimeType: str
    path: str
    modifiedTime: str
    size: Optional[str] = None
    webViewLink: Optional[str] = None
    parents: Optional[List[str]] = None

    class Config:
        populate_by_name = True


class DriveFolder(BaseModel):
    """Represents a Google Drive folder"""
    id: str
    name: str
    path: str
    fileCount: int

    class Config:
        populate_by_name = True


class SearchResult(BaseModel):
    """Represents a search result with source attribution"""
    id: str
    score: float
    text: str
    metadata: Dict[str, Any]
    highlights: List[str]

    class Config:
        populate_by_name = True


class ChatMessage(BaseModel):
    """Represents a chat message"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    sources: Optional[List[SearchResult]] = None
    timestamp: datetime


class IngestionStatus(BaseModel):
    """Represents the status of Drive ingestion"""
    is_ingesting: bool
    total_files: int
    processed_files: int
    current_file: Optional[str] = None
    error: Optional[str] = None

    class Config:
        populate_by_name = True


class SearchRequest(BaseModel):
    """Request model for document search"""
    query: str
    folder_id: Optional[str] = Field(None, alias="folderId")
    file_id: Optional[str] = Field(None, alias="fileId")
    limit: Optional[int] = 10

    class Config:
        populate_by_name = True


class ChatRequest(BaseModel):
    """Request model for chat"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = Field(None, alias="conversationHistory")
    folder_id: Optional[str] = Field(None, alias="folderId")
    file_id: Optional[str] = Field(None, alias="fileId")

    class Config:
        populate_by_name = True


class ChatResponse(BaseModel):
    """Response model for chat"""
    message: str
    sources: List[SearchResult]
