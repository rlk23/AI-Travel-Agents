// src/components/ui/calendar/views/week-view.tsx
import React from 'react';
import { cn } from '@/lib/utils';
import { CalendarEvent } from '@/types/calendar';
import { 
  format, 
  startOfWeek, 
  addDays, 
  isSameDay, 
  isToday,
  addMinutes
} from 'date-fns';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface WeekViewProps {
  currentDate: Date;
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onTimeSlotSelect?: (start: Date, end: Date) => void;
}

export function WeekView({
  currentDate,
  events,
  onEventClick,
  onTimeSlotSelect
}: WeekViewProps) {
  // Generate time slots (1-hour intervals)
  const hours = Array.from({ length: 24 }, (_, i) => i);
  
  // Generate days for the week
  const startDay = startOfWeek(currentDate, { weekStartsOn: 0 });
  const weekDays = Array.from({ length: 7 }, (_, i) => addDays(startDay, i));
  
  // Filter events for the current week
  const weekEvents = events.filter(event => {
    const eventDate = new Date(event.start);
    return weekDays.some(day => isSameDay(day, eventDate));
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
    
    // Find which day column this event belongs to
    const dayIndex = weekDays.findIndex(day => isSameDay(day, event.start));
    
    return {
      top: `${topPercentage}%`,
      height: `${Math.max(heightPercentage, 1.5)}%`, // Minimum height
      left: `${(dayIndex / 7) * 100}%`,
      width: `${100 / 7}%`
    };
  };
  
  // Handle time slot click to create new event
  const handleTimeSlotClick = (hour: number, day: Date) => {
    if (onTimeSlotSelect) {
      const start = new Date(day);
      start.setHours(hour, 0, 0, 0);
      const end = addMinutes(start, 60);
      onTimeSlotSelect(start, end);
    }
  };
  
  return (
    <div className="relative overflow-y-auto h-full">
      {/* Header row with days */}
      <div className="grid grid-cols-8 sticky top-0 z-10 bg-background border-b">
        <div className="border-r p-2 text-center text-sm font-medium"></div>
        {weekDays.map((day, index) => (
          <div 
            key={index} 
            className={cn(
              "border-r p-2 text-center",
              isToday(day) && "bg-primary/10"
            )}
          >
            <div className="font-medium">{format(day, 'EEE')}</div>
            <div className={cn(
              "text-2xl",
              isToday(day) && "text-primary font-bold"
            )}>
              {format(day, 'd')}
            </div>
          </div>
        ))}
      </div>
      
      {/* Time grid */}
      <div className="grid grid-cols-8 relative">
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
        
        {/* Day columns */}
        <div className="col-span-7 grid grid-cols-7 relative">
          {/* Hour rows for each day */}
          {weekDays.map((day, dayIndex) => (
            <div key={dayIndex} className={cn(
              "col-span-1 relative",
              isToday(day) && "bg-primary/5"
            )}>
              {hours.map((hour) => (
                <div 
                  key={hour} 
                  className="h-14 border-b border-r cursor-pointer hover:bg-muted/50"
                  onClick={() => handleTimeSlotClick(hour, day)}
                >
                  {/* Cell content goes here */}
                </div>
              ))}
              
              {/* Current time indicator */}
              {isToday(day) && (
                <div 
                  className="absolute left-0 right-0 border-t border-red-500 z-10"
                  style={{ 
                    top: `${(new Date().getHours() * 60 + new Date().getMinutes()) / (24 * 60) * 100}%`
                  }}
                >
                  <div className="w-2 h-2 bg-red-500 rounded-full relative -top-1 -left-1"></div>
                </div>
              )}
            </div>
          ))}
          
          {/* Events */}
          <TooltipProvider>
            {weekEvents.map((event) => (
              <Tooltip key={event.id}>
                <TooltipTrigger asChild>
                  <div
                    className="absolute rounded px-1 py-1 overflow-hidden text-white cursor-pointer text-xs"
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