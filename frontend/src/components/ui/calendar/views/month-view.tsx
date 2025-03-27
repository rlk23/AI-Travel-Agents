import React from 'react';
import { cn } from '@/lib/utils';
import { CalendarEvent } from '@/types/calendar';
import { 
  format, 
  startOfMonth, 
  endOfMonth, 
  startOfWeek, 
  endOfWeek, 
  isSameMonth, 
  isSameDay, 
  isToday,
  addDays
} from 'date-fns';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface MonthViewProps {
  currentDate: Date;
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onDateSelect?: (date: Date) => void;
}

export function MonthView({
  currentDate,
  events,
  onEventClick,
  onDateSelect
}: MonthViewProps) {
  // Generate days for the month view (includes days from previous/next month to fill grid)
  const getDaysForMonthView = () => {
    const start = startOfWeek(startOfMonth(currentDate), { weekStartsOn: 0 });
    const end = endOfWeek(endOfMonth(currentDate), { weekStartsOn: 0 });
    
    const days = [];
    let day = start;
    
    while (day <= end) {
      days.push(day);
      day = addDays(day, 1);
    }
    
    // Create a 2D array of weeks
    const weeks = [];
    for (let i = 0; i < days.length; i += 7) {
      weeks.push(days.slice(i, i + 7));
    }
    
    return weeks;
  };
  
  const weeks = getDaysForMonthView();
  
  // Get events for a specific date
  const getEventsForDate = (date: Date) => {
    return events.filter(event => {
      const eventDate = new Date(event.start);
      return isSameDay(eventDate, date);
    });
  };
  
  return (
    <div className="h-full overflow-y-auto">
      <div className="grid grid-cols-7 text-center py-2 border-b sticky top-0 bg-background z-10">
        <div>Sun</div>
        <div>Mon</div>
        <div>Tue</div>
        <div>Wed</div>
        <div>Thu</div>
        <div>Fri</div>
        <div>Sat</div>
      </div>
      
      <div className="grid grid-cols-7">
        {weeks.map((week, weekIndex) => (
          <React.Fragment key={weekIndex}>
            {week.map((day, dayIndex) => {
              const dayEvents = getEventsForDate(day);
              const isCurrentMonth = isSameMonth(day, currentDate);
              
              return (
                <div 
                  key={dayIndex}
                  className={cn(
                    "border-b border-r min-h-[100px] p-1 relative",
                    !isCurrentMonth && "bg-muted/20 text-muted-foreground",
                    isToday(day) && "bg-primary/5"
                  )}
                  onClick={() => onDateSelect?.(day)}
                >
                  <div className={cn(
                    "text-right p-1",
                    isToday(day) && "text-primary font-bold"
                  )}>
                    {format(day, 'd')}
                  </div>
                  
                  <div className="space-y-1">
                    <TooltipProvider>
                      {dayEvents.slice(0, 3).map((event) => (
                        <Tooltip key={event.id}>
                          <TooltipTrigger asChild>
                            <div
                              className="px-1 py-0.5 text-xs rounded truncate cursor-pointer"
                              style={{
                                backgroundColor: getEventTypeColor(event.type) + '33', // Add transparency
                                color: getEventTypeColor(event.type)
                              }}
                              onClick={(e) => {
                                e.stopPropagation();
                                onEventClick?.(event);
                              }}
                            >
                              {format(event.start, 'h:mm a')} {event.title}
                            </div>
                          </TooltipTrigger>
                          <TooltipContent>
                            <div className="space-y-1 p-1">
                              <p className="font-medium">{event.title}</p>
                              <p className="text-xs">
                                {format(event.start, 'h:mm a')} - {format(event.end, 'h:mm a')}
                              </p>
                              {event.location && <p className="text-xs">{event.location}</p>}
                            </div>
                          </TooltipContent>
                        </Tooltip>
                      ))}
                    </TooltipProvider>
                    
                    {dayEvents.length > 3 && (
                      <div className="text-xs text-center text-muted-foreground cursor-pointer hover:underline">
                        +{dayEvents.length - 3} more
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}