// src/components/ui/calendar/views/agenda-view.tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { CalendarEvent } from '@/types/calendar';
import { 
  format, 
  isSameDay, 
  isToday,
  compareAsc,
  startOfDay,
  addDays,
  differenceInDays
} from 'date-fns';
import { Plane, Hotel, MapPin, Calendar as CalendarIcon } from 'lucide-react';

interface AgendaViewProps {
  currentDate: Date;
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onDateSelect?: (date: Date) => void;
  daysToShow?: number;
}

export function AgendaView({
  currentDate,
  events,
  onEventClick,
  onDateSelect,
  daysToShow = 14
}: AgendaViewProps) {
  // Get all days to display
  const getDaysToShow = () => {
    const startDate = startOfDay(currentDate);
    const days = [];
    
    for (let i = 0; i < daysToShow; i++) {
      days.push(addDays(startDate, i));
    }
    
    return days;
  };
  
  const days = getDaysToShow();
  
  // Group events by day
  const eventsByDay = days.map(day => {
    return {
      date: day,
      events: events.filter(event => isSameDay(day, event.start))
    };
  }).filter(day => day.events.length > 0); // Only show days with events
  
  // If there are no events in the range, show a message
  if (eventsByDay.length === 0) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center space-y-2">
          <CalendarIcon className="h-10 w-10 mx-auto text-muted-foreground" />
          <h3 className="text-lg font-medium">No upcoming events</h3>
          <p className="text-muted-foreground">
            There are no events scheduled for the next {daysToShow} days.
          </p>
        </div>
      </div>
    );
  }
  
  // Get icon for event type
  const getEventIcon = (type: string) => {
    switch (type) {
      case 'flight':
        return <Plane className="h-4 w-4" />;
      case 'hotel':
        return <Hotel className="h-4 w-4" />;
      default:
        return <MapPin className="h-4 w-4" />;
    }
  };
  
  return (
    <div className="h-full overflow-y-auto p-4">
      <div className="space-y-6">
        {eventsByDay.map(({ date, events }) => (
          <div key={date.toString()}>
            <div 
              className={cn(
                "flex justify-between items-center mb-2 sticky top-0 py-2 px-4 -mx-4 bg-background z-10",
                isToday(date) && "bg-primary/10"
              )}
            >
              <h3 
                className={cn(
                  "text-lg font-medium",
                  isToday(date) && "text-primary"
                )}
              >
                {isToday(date) ? 'Today' : format(date, 'EEEE, MMMM d')}
              </h3>
              <button 
                className="text-sm text-muted-foreground hover:text-foreground"
                onClick={() => onDateSelect?.(date)}
              >
                View in calendar
              </button>
            </div>
            
            <div className="space-y-2">
              {events.sort((a, b) => compareAsc(a.start, b.start)).map(event => (
                <div 
                  key={event.id}
                  className="border rounded-md p-3 hover:bg-muted/50 cursor-pointer"
                  onClick={() => onEventClick?.(event)}
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center space-x-2">
                      <div 
                        className="rounded-full p-1"
                        style={{ 
                          backgroundColor: getEventTypeColor(event.type) + '33', // Add transparency
                          color: getEventTypeColor(event.type)
                        }}
                      >
                        {getEventIcon(event.type)}
                      </div>
                      <span className="font-medium">{event.title}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      {format(event.start, 'h:mm a')} - {format(event.end, 'h:mm a')}
                    </span>
                  </div>
                  
                  {event.location && (
                    <div className="text-sm text-muted-foreground flex items-center ml-7">
                      <MapPin className="h-3 w-3 mr-1" />
                      {event.location}
                    </div>
                  )}
                  
                  {event.details && (
                    <div className="text-sm ml-7 mt-1">
                      {event.details}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}