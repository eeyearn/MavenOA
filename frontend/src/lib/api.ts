import axios from 'axios';
import type {
  DriveFile,
  DriveFolder,
  SearchRequest,
  SearchResult,
  ChatRequest,
  ChatResponse,
  IngestionStatus,
} from '@/types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const driveApi = {
  // Google Drive Authentication
  getAuthUrl: async (): Promise<{ url: string }> => {
    const response = await api.get('/auth/google');
    return response.data;
  },

  getAuthStatus: async (): Promise<{ isAuthenticated: boolean }> => {
    const response = await api.get('/auth/status');
    return response.data;
  },

  // File and Folder Listing
  listFiles: async (): Promise<DriveFile[]> => {
    const response = await api.get('/drive/files');
    return response.data;
  },

  listFolders: async (): Promise<DriveFolder[]> => {
    const response = await api.get('/drive/folders');
    return response.data;
  },

  getFolder: async (folderId: string): Promise<DriveFolder> => {
    const response = await api.get(`/drive/folders/${folderId}`);
    return response.data;
  },

  // Ingestion endpoints
  startIngestion: async (): Promise<{ message: string }> => {
    const response = await api.post('/ingest/start');
    return response.data;
  },

  getIngestionStatus: async (): Promise<IngestionStatus> => {
    const response = await api.get('/ingest/status');
    return response.data;
  },

  // Search endpoints
  searchDocuments: async (request: SearchRequest): Promise<SearchResult[]> => {
    const response = await api.post('/search', request);
    return response.data;
  },

  // Chat endpoint
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat', request);
    return response.data;
  },
};
