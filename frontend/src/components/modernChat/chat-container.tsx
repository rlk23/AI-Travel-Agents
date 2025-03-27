// src/components/modernChat/chat-container.tsx
import React, { useState, useRef, useEffect } from 'react';
import { ModernChatMessage } from './modern-chat-message';
import { ModernMessageInput } from './modern-message-input';
import { Message, AgentResponse } from '@/types';
import { v4 as uuidv4 } from 'uuid';
import { ResultsView } from '@/components/results-view';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, Info } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';

export function ModernChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      content: "Hi there! I'm your AI travel assistant. I can help you book flights and hotels. Just tell me where you want to go, when, and any other details! For example, try asking: 'I want to fly from New York to Miami on March 15th and return on March 20th. I need a hotel too.'",
      role: 'assistant',
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [latestResponse, setLatestResponse] = useState<AgentResponse | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: uuidv4(),
      content,
      role: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    setLatestResponse(null);
    
    try {
      const response = await fetch('http://localhost:5002/api/ai-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: content })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }
      
      setLatestResponse(data);
      
      let responseContent = "Here's what I found based on your request:";
      
      if (data.booking_details) {
        const origin = data.booking_details['Origin city'];
        const destination = data.booking_details['Destination city'];
        const departDate = data.booking_details['Departure date'];
        const returnDate = data.booking_details['Return date'];
        
        responseContent = `I found ${data.departure_flights?.length || 0} flights from ${origin} to ${destination} on ${departDate}`;
        
        if (returnDate) {
          responseContent += ` and ${data.return_flights?.length || 0} return flights on ${returnDate}`;
        }
        
        if (data.hotels?.length) {
          responseContent += `. I also found ${data.hotels.length} hotels available for your stay.`;
        } else {
          responseContent += `.`;
        }
      }
      
      const assistantMessage: Message = {
        id: uuidv4(),
        content: responseContent,
        role: 'assistant',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (err) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      
      const errorMessage: Message = {
        id: uuidv4(),
        content: `Sorry, I encountered an error: ${err instanceof Error ? err.message : 'An unexpected error occurred'}. Please try again.`,
        role: 'assistant',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div ref={chatContainerRef} className="flex flex-col h-full w-full max-w-4xl mx-auto bg-background">
      {/* Empty state when no messages */}
      {messages.length === 1 && (
        <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
          <h1 className="text-3xl font-bold mb-6">Travel AI Assistant</h1>
          <p className="text-muted-foreground max-w-md mb-8">
            Ask me about booking flights, finding hotels, or planning your next trip!
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
            <div className="border rounded-lg p-4 hover:bg-muted/50 cursor-pointer transition">
              <h3 className="font-medium mb-1">Find flights and hotels</h3>
              <p className="text-sm text-muted-foreground">
                "I need a flight from NYC to London next week"
              </p>
            </div>
            <div className="border rounded-lg p-4 hover:bg-muted/50 cursor-pointer transition">
              <h3 className="font-medium mb-1">Plan an itinerary</h3>
              <p className="text-sm text-muted-foreground">
                "Help me plan a 3-day trip to Paris"
              </p>
            </div>
            <div className="border rounded-lg p-4 hover:bg-muted/50 cursor-pointer transition">
              <h3 className="font-medium mb-1">Compare options</h3>
              <p className="text-sm text-muted-foreground">
                "What's cheaper, flying to Miami or San Diego in June?"
              </p>
            </div>
            <div className="border rounded-lg p-4 hover:bg-muted/50 cursor-pointer transition">
              <h3 className="font-medium mb-1">Find activities</h3>
              <p className="text-sm text-muted-foreground">
                "What are must-see attractions in Tokyo?"
              </p>
            </div>
          </div>
        </div>
      )}
      
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto">
        <AnimatePresence initial={false}>
          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <ModernChatMessage message={message} />
              
              {/* Show response data after the assistant message */}
              {message.role === 'assistant' && 
               latestResponse && 
               index === messages.length - 1 && 
               !isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="px-4 pb-4 pt-1"
                >
                  <ResultsView response={latestResponse} />
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Error message */}
        {error && (
          <div className="px-4 py-2">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </div>
        )}
        
        {/* Loading indicator */}
        {isLoading && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-start gap-3 py-4 px-4"
          >
            <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md bg-primary/20 text-primary">
              <div className="h-4 w-4 relative">
                <div className="animate-pulse absolute inset-0 rounded-full bg-current opacity-75"></div>
              </div>
            </div>
            <div className="flex-1">
              <div className="flex space-x-2">
                <div className="h-2 w-24 bg-muted-foreground/20 rounded animate-pulse"></div>
                <div className="h-2 w-32 bg-muted-foreground/20 rounded animate-pulse"></div>
                <div className="h-2 w-16 bg-muted-foreground/20 rounded animate-pulse"></div>
              </div>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area */}
      <div className="border-t p-4">
        <ModernMessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        <div className="mt-2 text-center text-xs text-muted-foreground flex items-center justify-center">
          <Info className="h-3 w-3 mr-1" />
          <span>AI travel assistant may make mistakes. Verify all suggestions before booking.</span>
        </div>
      </div>
    </div>
  );
}
