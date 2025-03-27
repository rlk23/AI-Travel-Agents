// src/components/ui/calendar/views/day-view.tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { CalendarEvent } from '@/types/calendar';
import { 
  format, 
  isToday,
  addMinutes
} from 'date-fns';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface DayViewProps {
  currentDate: Date;
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onTimeSlotSelect?: (start: Date, end: Date) => void;
}

export function DayView({
  currentDate,
  events,
  onEventClick,
  onTimeSlotSelect
}: DayViewProps) {
  // Generate time slots (1-hour intervals)
  const hours = Array.from({ length: 24 }, (_, i) => i);
  
  // Filter events for the current day
  const dayEvents = events.filter(event => {
    const eventDate = new Date(event.start);
    return eventDate.getDate() === currentDate.getDate() &&
      eventDate.getMonth() === currentDate.getMonth() &&
      eventDate.getFullYear() === currentDate.getFullYear();
  });
  
  // Calculate event position and dimensions
  const getEventStyle = (event: CalendarEvent) => {
    // Calculate top position based on time
    const startHour = event.start.getHours();
    const startMinute = event.start.getMinutes();
    const topPercentage = (startHour * 60 + startMinute) / (24 * 60) * 100;
    
    // Calculate height based on duration
    const durationMinutes = (event.end.getTime() - event.start.getTime()) / (1000 * 60);
    const heightPercentage = (durationMinutes / (24 * 60)) * 100;
    
    return {
      top: `${topPercentage}%`,
      height: `${Math.max(heightPercentage, 1.5)}%` // Minimum height
    };
  };
  
  // Handle time slot click to create new event
  const handleTimeSlotClick = (hour: number) => {
    if (onTimeSlotSelect) {
      const start = new Date(currentDate);
      start.setHours(hour, 0, 0, 0);
      const end = addMinutes(start, 60);
      onTimeSlotSelect(start, end);
    }
  };
  
  return (
    <div className="relative overflow-y-auto h-full">
      {/* Header row */}
      <div className="grid grid-cols-2 sticky top-0 z-10 bg-background border-b">
        <div className="border-r p-2 text-center text-sm font-medium"></div>
        <div 
          className={cn(
            "border-r p-2 text-center",
            isToday(currentDate) && "bg-primary/10"
          )}
        >
          <div className="font-medium">{format(currentDate, 'EEEE')}</div>
          <div className={cn(
            "text-2xl",
            isToday(currentDate) && "text-primary font-bold"
          )}>
            {format(currentDate, 'd')}
          </div>
        </div>
      </div>
      
      {/* Time grid */}
      <div className="grid grid-cols-2 relative">
        {/* Time labels column */}
        <div className="col-span-1">
          {hours.map((hour) => (
            <div 
              key={hour} 
              className="h-14 border-b border-r relative"
            >
              <span className="absolute -top-2.5 right-2 text-xs text-muted-foreground">
                {hour === 0 ? '12 AM' : hour === 12 ? '12 PM' : hour > 12 ? `${hour - 12} PM` : `${hour} AM`}
              </span>
            </div>
          ))}
        </div>
        
        {/* Day column */}
        <div className="col-span-1 relative">
          {hours.map((hour) => (
            <div 
              key={hour} 
              className="h-14 border-b border-r cursor-pointer hover:bg-muted/50"
              onClick={() => handleTimeSlotClick(hour)}
            ></div>
          ))}
          
          {/* Current time indicator */}
          {isToday(currentDate) && (
            <div 
              className="absolute left-0 right-0 border-t border-red-500 z-10"
              style={{ 
                top: `${(new Date().getHours() * 60 + new Date().getMinutes()) / (24 * 60) * 100}%`
              }}
            >
              <div className="w-2 h-2 bg-red-500 rounded-full relative -top-1 -left-1"></div>
            </div>
          )}
          
          {/* Events */}
          <TooltipProvider>
            {dayEvents.map((event) => (
              <Tooltip key={event.id}>
                <TooltipTrigger asChild>
                  <div
                    className="absolute left-0 right-0 mx-1 rounded px-2 py-1 overflow-hidden text-white cursor-pointer text-xs"
                    style={{
                      ...getEventStyle(event),
                      backgroundColor: getEventTypeColor(event.type),
                      zIndex: 5
                    }}
                    onClick={() => onEventClick?.(event)}
                  >
                    <div className="font-medium truncate">{event.title}</div>
                    {event.location && (
                      <div className="truncate opacity-80">{event.location}</div>
                    )}
                  </div>
                </TooltipTrigger>
                <TooltipContent>
                  <div className="space-y-1 p-1">
                    <p className="font-medium">{event.title}</p>
                    <p className="text-xs">
                      {format(event.start, 'h:mm a')} - {format(event.end, 'h:mm a')}
                    </p>
                    {event.location && <p className="text-xs">{event.location}</p>}
                    {event.details && <p className="text-xs">{event.details}</p>}
                  </div>
                </TooltipContent>
              </Tooltip>
            ))}
          </TooltipProvider>
        </div>
      </div>
    </div>
  );
}

// Helper function to get color based on event type (needs to be defined in the same file or imported)
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