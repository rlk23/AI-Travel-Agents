import React from 'react';
import { Chat } from '@/components/chat';
import { ModeToggle } from './components/mode-toggle';
import { Plane } from 'lucide-react';

function App() {
  return (
    <div className="flex flex-col h-screen bg-background">
      <header className="border-b py-3 px-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Plane className="h-6 w-6" />
          <h1 className="font-bold text-xl">AI Travel Assistant</h1>
        </div>
        <ModeToggle />
      </header>
      
      <main className="flex-1 overflow-hidden container py-4">
        <div className="border rounded-lg shadow-sm h-full overflow-hidden">
          <Chat />
        </div>
      </main>
      
      <footer className="border-t py-3 px-4 text-center text-sm text-muted-foreground">
        © 2025 AI Travel Assistant
      </footer>
    </div>
  );
}

export default App;