import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
  MessageSquare,
  Calendar,
  Settings,
  Plane,
  Menu,
  X
} from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

interface SidebarProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

interface SidebarItemProps {
  icon: React.ReactNode;
  text: string;
  active?: boolean;
  onClick?: () => void;
}

const SidebarItem = ({ icon, text, active, onClick }: SidebarItemProps) => {
  return (
    <Button
      variant={active ? "secondary" : "ghost"}
      size="lg"
      className={cn(
        "w-full justify-start gap-2 mb-1",
        active && "font-semibold"
      )}
      onClick={onClick}
    >
      {icon}
      <span>{text}</span>
    </Button>
  );
};

export function Sidebar({ currentTab, onTabChange }: SidebarProps) {
  return (
    <>
      {/* Mobile Sidebar */}
      <div className="lg:hidden flex items-center p-4 border-b">
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="h-6 w-6" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="p-0">
            <div className="flex flex-col h-full">
              <div className="p-4 border-b flex items-center">
                <Plane className="h-6 w-6 mr-2" />
                <h1 className="font-bold text-xl">Travel Assistant</h1>
              </div>
              <div className="p-4 flex flex-col flex-1">
                <SidebarItem 
                  icon={<MessageSquare className="h-5 w-5" />} 
                  text="Chat" 
                  active={currentTab === 'chat'}
                  onClick={() => onTabChange('chat')}
                />
                <SidebarItem 
                  icon={<Calendar className="h-5 w-5" />} 
                  text="Calendar" 
                  active={currentTab === 'calendar'}
                  onClick={() => onTabChange('calendar')}
                />
                <SidebarItem 
                  icon={<Settings className="h-5 w-5" />} 
                  text="Settings" 
                  active={currentTab === 'settings'}
                  onClick={() => onTabChange('settings')}
                />
              </div>
            </div>
          </SheetContent>
        </Sheet>
        <div className="ml-2 flex items-center">
          <Plane className="h-6 w-6 mr-2" />
          <h1 className="font-bold text-xl">Travel Assistant</h1>
        </div>
      </div>
      
      {/* Desktop Sidebar */}
      <div className="hidden lg:flex lg:flex-col w-64 h-full border-r">
        <div className="p-4 border-b flex items-center">
          <Plane className="h-6 w-6 mr-2" />
          <h1 className="font-bold text-xl">Travel Assistant</h1>
        </div>
        <div className="p-4 flex flex-col flex-1">
          <SidebarItem 
            icon={<MessageSquare className="h-5 w-5" />} 
            text="Chat" 
            active={currentTab === 'chat'}
            onClick={() => onTabChange('chat')}
          />
          <SidebarItem 
            icon={<Calendar className="h-5 w-5" />} 
            text="Calendar" 
            active={currentTab === 'calendar'}
            onClick={() => onTabChange('calendar')}
          />
          <SidebarItem 
            icon={<Settings className="h-5 w-5" />} 
            text="Settings" 
            active={currentTab === 'settings'}
            onClick={() => onTabChange('settings')}
          />
        </div>
      </div>
    </>
  );
}