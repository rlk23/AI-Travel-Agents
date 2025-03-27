// src/components/ui/calendar/calendar-sidebar.tsx
import React, { useState } from 'react';
import { Calendar } from '@/components/ui/calendar';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { CalendarEvent } from '@/types/calendar';
import { Button } from '@/components/ui/button';
import { Plus, ChevronDown, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { isSameDay } from 'date-fns';

interface CalendarSidebarProps {
  events: CalendarEvent[];
  currentDate: Date;
  onDateSelect: (date: Date) => void;
}

export function CalendarSidebar({
  events,
  currentDate,
  onDateSelect
}: CalendarSidebarProps) {
  const [date, setDate] = useState<Date | undefined>(currentDate);
  const [showUpcoming, setShowUpcoming] = useState(true);
  
  // Find days that have events
  const daysWithEvents = events.map(event => event.start);
  
  // Get upcoming events (next 7 days)
  const upcomingEvents = events.filter(event => {
    const eventDate = new Date(event.start);
    const now = new Date();
    const sevenDaysLater = new Date();
    sevenDaysLater.setDate(now.getDate() + 7);
    
    return eventDate >= now && eventDate <= sevenDaysLater;
  }).sort((a, b) => a.start.getTime() - b.start.getTime());
  
  // Group upcoming events by date
  const groupedUpcomingEvents: Record<string, CalendarEvent[]> = {};
  
  upcomingEvents.forEach(event => {
    const dateKey = event.start.toDateString();
    if (!groupedUpcomingEvents[dateKey]) {
      groupedUpcomingEvents[dateKey] = [];
    }
    groupedUpcomingEvents[dateKey].push(event);
  });
  
  return (
    <div className="w-64 border-r h-full flex flex-col overflow-auto">
      <div className="p-4">
        <Button className="w-full" size="sm">
          <Plus className="mr-2 h-4 w-4" /> New Event
        </Button>
      </div>
      
      <Card className="mx-2 mb-4 shadow-none">
        <CardContent className="p-2">
          <Calendar
            mode="single"
            selected={date}
            onSelect={(newDate) => {
              setDate(newDate);
              if (newDate) {
                onDateSelect(newDate);
              }
            }}
            modifiers={{
              hasEvent: daysWithEvents
            }}
            modifiersClassNames={{
              hasEvent: "bg-primary/10 font-bold text-primary"
            }}
            className="rounded-md"
          />
        </CardContent>
      </Card>
      
      <div className="px-4 py-2">
        <div 
          className="flex items-center justify-between cursor-pointer mb-2"
          onClick={() => setShowUpcoming(!showUpcoming)}
        >
          <h3 className="font-medium">Upcoming Events</h3>
          {showUpcoming ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
        </div>
        
        {showUpcoming && Object.keys(groupedUpcomingEvents).length > 0 ? (
          <div className="space-y-4">
            {Object.entries(groupedUpcomingEvents).map(([dateKey, dateEvents]) => (
              <div key={dateKey}>
                <h4 className="text-sm font-medium mb-1">
                  {new Date(dateKey).toLocaleDateString(undefined, { 
                    weekday: 'short', 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </h4>
                <div className="space-y-1 pl-2">
                  {dateEvents.map(event => (
                    <div 
                      key={event.id}
                      className="text-xs py-1 px-2 rounded cursor-pointer hover:bg-muted"
                      onClick={() => {
                        onDateSelect(event.start);
                      }}
                    >
                      <div className="flex items-center">
                        <div 
                          className="w-2 h-2 rounded-full mr-2"
                          style={{ 
                            backgroundColor: getEventTypeColor(event.type)
                          }}
                        ></div>
                        <span>
                          {event.start.toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                      <div className="ml-4 truncate">
                        {event.title}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : showUpcoming ? (
          <div className="text-sm text-muted-foreground">
            No upcoming events in the next 7 days.
          </div>
        ) : null}
      </div>
      
      <Separator className="my-4" />
      
      <div className="px-4 py-2 flex-1">
        <h3 className="font-medium mb-2">My Calendars</h3>
        <div className="space-y-2">
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-blue-500 mr-2"></div>
            <label className="text-sm flex items-center">
              <input type="checkbox" className="mr-2" defaultChecked />
              Flights
            </label>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-purple-500 mr-2"></div>
            <label className="text-sm flex items-center">
              <input type="checkbox" className="mr-2" defaultChecked />
              Hotels
            </label>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
            <label className="text-sm flex items-center">
              <input type="checkbox" className="mr-2" defaultChecked />
              Activities
            </label>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
            <label className="text-sm flex items-center">
              <input type="checkbox" className="mr-2" defaultChecked />
              Restaurants
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

// Helper function to get color based on event type
function getEventTypeColor(type: string): string {
  switch (type) {
    case 'flight':
      return '#3b82f6'; // blue-500
    case 'hotel':
      return '#8b5cf6'; // purple-500
    case 'restaurant':
      return '#f97316'; // orange-500
    case 'sightseeing':
      return '#22c55e'; // green-500
    case 'activity':
      return '#f59e0b'; // amber-500
    case 'transport':
      return '#64748b'; // slate-500
    default:
      return '#6b7280'; // gray-500
  }
}