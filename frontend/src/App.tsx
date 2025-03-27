import React, { useState } from 'react';
import { Chat } from '@/components/chat';
import { Sidebar } from '@/components/sidebar';
import { CalendarView } from '@/components/calendar-view';
import { SettingsView } from '@/components/settings-view';
import { ThemeProvider } from '@/components/theme-provider';

function App() {
  const [currentTab, setCurrentTab] = useState<string>('chat');
  
  const renderContent = () => {
    switch (currentTab) {
      case 'chat':
        return <Chat />;
      case 'calendar':
        return <CalendarView />;
      case 'settings':
        return <SettingsView />;
      default:
        return <Chat />;
    }
  };
  
  return (
    <ThemeProvider defaultTheme="system" storageKey="travel-app-theme">
      <div className="flex flex-col lg:flex-row h-screen bg-background">
        <Sidebar currentTab={currentTab} onTabChange={setCurrentTab} />
        
        <div className="flex-1 flex flex-col h-full overflow-hidden">
          <main className="flex-1 overflow-auto">
            {renderContent()}
          </main>
          
          <footer className="border-t py-3 px-4 text-center text-sm text-muted-foreground">
            © 2025 AI Travel Assistant
          </footer>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;