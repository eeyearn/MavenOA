import { ChatInterface } from '@/components/ChatInterface';
import { IngestionPanel } from '@/components/IngestionPanel';
import { AuthButton } from '@/components/AuthButton';
import { useAuthStatus } from '@/hooks/useAuthStatus';
import { Loader2 } from 'lucide-react';

function App() {
  const { data: authStatus, isLoading } = useAuthStatus();
  const isAuthenticated = authStatus?.isAuthenticated ?? false;

  // Show a loading spinner while we check the auth status
  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center bg-white">
        <Loader2 className="w-10 h-10 text-black animate-spin" />
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* Header */}
      <header className="bg-white border-b border-black px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-black">Maven Drive Copilot</h1>
          {!isAuthenticated && <AuthButton />}
        </div>
      </header>

      {/* Main Content */}
      {isAuthenticated ? (
        <div className="flex-1 flex overflow-hidden">
          {/* Sidebar */}
          <aside className="w-80 bg-white border-r border-black p-4 overflow-y-auto">
            <IngestionPanel />
          </aside>

          {/* Chat Area */}
          <main className="flex-1 flex flex-col bg-white">
            <ChatInterface />
          </main>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center bg-white">
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold text-black">
              Welcome to Maven Drive Copilot
            </h2>
            <p className="text-gray-700 max-w-md">
              Connect your Google Drive to start searching and chatting with your documents
            </p>
            <div className="pt-4">
              <AuthButton />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
