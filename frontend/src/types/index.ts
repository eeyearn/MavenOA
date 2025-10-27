export interface DriveFile {
  id: string;
  name: string;
  mimeType: string;
  path: string;
  modifiedTime: string;
  size?: number;
  webViewLink?: string;
}

export interface DriveFolder {
  id: string;
  name: string;
  path: string;
  fileCount: number;
}

export interface SearchResult {
    id: string;
    score: number;
    text: string;
    metadata: { [key: string]: any };
    highlights: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: SearchResult[];
  timestamp: Date;
}

export interface IngestionStatus {
    is_ingesting: boolean;
    total_files: number;
    processed_files: number;
    current_file: string | null;
    error?: string;
}

export interface SearchRequest {
  query: string;
  folderId?: string;
  fileId?: string;
  limit?: number;
}

export interface ChatRequest {
  message: string;
  conversationHistory?: ChatMessage[];
  folderId?: string;
  fileId?: string;
}

export interface ChatResponse {
  message: string;
  sources: SearchResult[];
}
