import { LogIn, Loader2 } from 'lucide-react';
import { useAuthUrl } from '@/hooks/useAuthUrl';

export const AuthButton = () => {
  const { data, isLoading } = useAuthUrl();

  const className = "bg-black text-white rounded-lg px-6 py-3 hover:bg-gray-800 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg font-medium transition-colors";

  if (isLoading || !data?.url) {
    return (
      <button disabled className={className}>
        <Loader2 className="w-5 h-5 animate-spin" />
        Loading...
      </button>
    );
  }
  
  return (
    <a href={data.url} className={className}>
      <LogIn className="w-5 h-5" />
      Connect Google Drive
    </a>
  );
};
