import { Play, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { useIngestionStatus } from '@/hooks/useIngestionStatus';
import { useStartIngestion } from '@/hooks/useStartIngestion';

export const IngestionPanel = () => {
  const { data: status, refetch: refetchStatus } = useIngestionStatus();
  const startIngestion = useStartIngestion();

  const handleStartIngestion = () => {
    startIngestion.mutate(undefined, {
      onSuccess: () => {
        // Immediately refetch status after starting ingestion
        setTimeout(() => {
          refetchStatus();
        }, 500);
      }
    });
  };

  const isIngestionComplete = !status?.is_ingesting && (status?.processed_files ?? 0) > 0;
  const isIngesting = status?.is_ingesting;
  const isPristine = !status?.is_ingesting && (status?.processed_files ?? 0) === 0;

  const progress =
    status?.total_files && status.total_files > 0
      ? (status.processed_files / status.total_files) * 100
      : 0;

  return (
    <div className="border border-black rounded-lg p-4 bg-white">
      <h3 className="text-lg font-semibold mb-4 text-black">Drive Ingestion</h3>

      {/* Initial state or Ingestion complete */}
      {(isPristine || isIngestionComplete) && (
        <div className="space-y-3">
          {isPristine ? (
            <p className="text-sm text-gray-700">
              Start ingesting your Google Drive files into the vector database for semantic search.
            </p>
          ) : (
            <>
              <div className="flex items-center gap-2 text-black">
                <CheckCircle className="w-5 h-5" />
                <span className="font-medium">Ingestion complete</span>
              </div>
              <p className="text-sm text-gray-700">
                Successfully processed {status.processed_files} files
              </p>
            </>
          )}

          <button
            onClick={handleStartIngestion}
            disabled={startIngestion.isPending || isIngesting}
            className="w-full bg-black text-white rounded-lg px-4 py-2 hover:bg-gray-800 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {startIngestion.isPending || isIngesting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                {isIngestionComplete ? 'Re-ingesting...' : 'Starting...'}
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                {isIngestionComplete ? 'Re-ingest Drive' : 'Start Ingestion'}
              </>
            )}
          </button>
        </div>
      )}
      
      {/* Ingestion in progress */}
      {isIngesting && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-black">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span className="font-medium">Ingesting files...</span>
          </div>

          {status.total_files > 0 && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-700">
                <span>
                  {status.processed_files} / {status.total_files} files
                </span>
                <span>{progress.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-black h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}

          {status.current_file && (
            <p className="text-sm text-gray-700 truncate">
              {status.total_files === 0 ? (
                <span className="font-medium">{status.current_file}</span>
              ) : (
                <>
                  Processing: <span className="font-medium">{status.current_file}</span>
                </>
              )}
            </p>
          )}
        </div>
      )}

      {status?.error && (
        <div className="mt-3 p-3 bg-gray-100 border border-black rounded-lg">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-5 h-5 text-black flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-black">Ingestion Error</p>
              <p className="text-sm text-gray-700 mt-1">{status.error}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
