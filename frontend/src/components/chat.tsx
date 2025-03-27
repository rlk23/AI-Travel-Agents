import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './chat-message';
import { MessageInput } from './message-input';
import { Message, AgentResponse } from '@/types';
import { v4 as uuidv4 } from 'uuid';
import { ResultsView } from './results-view';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

export function Chat() {
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
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4">
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        <div className="space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          
          {latestResponse && (
            <>
              <Separator className="my-6" />
              <ResultsView response={latestResponse} />
            </>
          )}
        </div>
        
        <div ref={messagesEndRef} />
      </div>
      
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
