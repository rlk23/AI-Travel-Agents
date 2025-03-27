import React from 'react';
import { Message } from '@/types';
import { cn } from '@/lib/utils';
import { Card, CardContent } from '@/components/ui/card';
import { MessagesSquare, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={cn(
      "flex items-start gap-3 py-4",
      isUser ? "justify-end" : "justify-start"
    )}>
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md bg-primary text-primary-foreground">
          <MessagesSquare className="h-4 w-4" />
        </div>
      )}
      
      <Card className={cn(
        "max-w-[80%]",
        isUser ? "bg-primary text-primary-foreground" : ""
      )}>
        <CardContent className="p-4">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </CardContent>
      </Card>
      
      {isUser && (
        <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md bg-muted text-muted-foreground">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  );
}