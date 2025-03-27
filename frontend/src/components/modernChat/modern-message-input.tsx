import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { SendHorizontal, Loader2, Mic, Plus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModernMessageInputProps {
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export function ModernMessageInput({ onSendMessage, isLoading }: ModernMessageInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [message]);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end rounded-lg border bg-background">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="flex-shrink-0 h-10 w-10 rounded-full"
          disabled={isLoading}
        >
          <Plus className="h-5 w-5" />
        </Button>
        
        <Textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message Travel Assistant..."
          className={cn(
            "flex-1 min-h-[40px] resize-none border-0 p-3 shadow-none focus-visible:ring-0",
            message.length > 0 ? "pr-20" : "pr-10"
          )}
          rows={1}
          disabled={isLoading}
        />
        
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="flex-shrink-0 h-10 w-10 rounded-full mr-1"
          disabled={isLoading}
        >
          <Mic className="h-5 w-5" />
        </Button>
        
        <Button
          type="submit"
          variant="ghost"
          size="icon"
          className={cn(
            "absolute right-12 bottom-1 h-8 w-8 rounded-full",
            message.length === 0 && "opacity-0"
          )}
          disabled={isLoading || !message.trim()}
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <SendHorizontal className="h-4 w-4" />
          )}
        </Button>
      </div>
    </form>
  );
}
