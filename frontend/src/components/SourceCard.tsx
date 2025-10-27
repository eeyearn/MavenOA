import type { SearchResult } from '@/types';
import { FileText, ExternalLink } from 'lucide-react';

interface SourceCardProps {
  source: SearchResult;
}

export const SourceCard = ({ source }: SourceCardProps) => {
  const snippet = source.text.length > 200 ? `${source.text.substring(0, 200)}...` : source.text;

  return (
    <div className="border border-black rounded-lg p-3 text-sm max-w-xs bg-white">
      <div className="flex items-center gap-2 mb-2">
        <FileText className="w-4 h-4 text-black flex-shrink-0" />
        <a
          href={source.metadata.web_view_link || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className="font-semibold text-black truncate hover:underline"
          title={source.metadata.file_name}
        >
          {source.metadata.file_name}
        </a>
        <a
          href={source.metadata.web_view_link || '#'}
          target="_blank"
          rel="noopener noreferrer"
        >
          <ExternalLink className="w-4 h-4 text-gray-500 hover:text-black" />
        </a>
      </div>
      <p className="text-gray-700 italic">"{snippet}"</p>
    </div>
  );
};
