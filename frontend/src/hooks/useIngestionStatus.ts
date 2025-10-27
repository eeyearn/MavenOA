import { useQuery } from '@tanstack/react-query';
import { driveApi } from '@/lib/api';

export const useIngestionStatus = () => {
  return useQuery({
    queryKey: ['ingestionStatus'],
    queryFn: driveApi.getIngestionStatus,
    refetchInterval: (query) => {
      // If ingestion is complete or has an error, stop refetching
      const data = query.state.data;
      if (data && (!data.is_ingesting && data.total_files > 0)) {
        return false;
      }
      if (data?.error) {
        return false;
      }
      // Otherwise, refetch every 2 seconds
      return 2000;
    },
    refetchIntervalInBackground: false,
  });
};
