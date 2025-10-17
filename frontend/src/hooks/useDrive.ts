import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { driveApi } from '@/lib/api';
import type { SearchRequest, ChatRequest } from '@/types';

export const useDrive = () => {
  const queryClient = useQueryClient();

  // Get Google Auth URL
  const useAuthUrl = () => {
    return useQuery({
      queryKey: ['authUrl'],
      queryFn: driveApi.getAuthUrl,
      staleTime: Infinity,
    });
  };

  // List files
  const useFiles = () => {
    return useQuery({
      queryKey: ['files'],
      queryFn: driveApi.listFiles,
      staleTime: 5 * 60 * 1000, // 5 minutes
    });
  };

  // List folders
  const useFolders = () => {
    return useQuery({
      queryKey: ['folders'],
      queryFn: driveApi.listFolders,
      staleTime: 5 * 60 * 1000, // 5 minutes
    });
  };

  // Get folder details
  const useFolder = (folderId: string) => {
    return useQuery({
      queryKey: ['folder', folderId],
      queryFn: () => driveApi.getFolder(folderId),
      enabled: !!folderId,
      staleTime: 5 * 60 * 1000,
    });
  };

  // Ingestion status (polling)
  const useIngestionStatus = () => {
    return useQuery({
      queryKey: ['ingestionStatus'],
      queryFn: driveApi.getIngestionStatus,
      refetchInterval: (data) => {
        // Poll every 2 seconds while ingesting, otherwise don't poll
        return data?.isIngesting ? 2000 : false;
      },
    });
  };

  // Start ingestion mutation
  const useStartIngestion = () => {
    return useMutation({
      mutationFn: driveApi.startIngestion,
      onSuccess: () => {
        // Invalidate and refetch ingestion status
        queryClient.invalidateQueries({ queryKey: ['ingestionStatus'] });
      },
    });
  };

  // Search mutation
  const useSearch = () => {
    return useMutation({
      mutationFn: (request: SearchRequest) => driveApi.searchDocuments(request),
    });
  };

  // Chat mutation
  const useChat = () => {
    return useMutation({
      mutationFn: (request: ChatRequest) => driveApi.chat(request),
    });
  };

  return {
    useAuthUrl,
    useFiles,
    useFolders,
    useFolder,
    useIngestionStatus,
    useStartIngestion,
    useSearch,
    useChat,
  };
};
