import React from 'react';
import { Message } from '@/types';
import { cn } from '@/lib/utils';
import { Plane, User } from 'lucide-react';

interface ModernChatMessageProps {
  message: Message;
}

export function ModernChatMessage({ message }: ModernChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={cn(
      "group relative px-4 py-6",
      isUser ? "bg-muted/50" : "bg-background", 
      "border-b border-border/40"
    )}>
      <div className="max-w-4xl mx-auto flex items-start gap-4">
        {/* Avatar */}
        <div className={cn(
          "flex-shrink-0 w-8 h-8 rounded-full overflow-hidden flex items-center justify-center",
          isUser ? "bg-primary" : "bg-primary/20"
        )}>
          {isUser ? (
            <User className="h-4 w-4 text-primary-foreground" />
          ) : (
            <Plane className="h-4 w-4 text-primary" />
          )}
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="text-sm pb-1 text-muted-foreground font-medium">
            {isUser ? 'You' : 'Travel Assistant'}
          </div>
          <div className="prose prose-sm dark:prose-invert max-w-none">
            <p className="whitespace-pre-wrap">{message.content}</p>
          </div>
        </div>
        
        {/* Action buttons (only visible on hover) */}
        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
          <button className="text-muted-foreground hover:text-foreground p-1 rounded" title="Copy to clipboard">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
