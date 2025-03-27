// src/components/ui/calendar/calendar-layout.tsx
import React, { useState } from 'react';
import { CalendarHeader } from './calendar-header';
import { CalendarSidebar } from './calendar-sidebar';
import { DayView } from './views/day-view';
import { WeekView } from './views/week-view';
import { MonthView } from './views/month-view';
import { AgendaView } from './views/agenda-view';
import { CalendarViewType, CalendarEvent } from '@/types/calendar';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { addDays, addMonths, addWeeks, startOfDay, startOfMonth, startOfWeek } from 'date-fns';

interface CalendarLayoutProps {
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onDateSelect?: (date: Date) => void;
  onNewEvent?: (start: Date, end: Date) => void;
}

export function CalendarLayout({
  events,
  onEventClick,
  onDateSelect,
  onNewEvent
}: CalendarLayoutProps) {
  // Use local storage to remember user's view preference
  const [viewType, setViewType] = useLocalStorage<CalendarViewType>('calendarViewType', 'week');
  const [currentDate, setCurrentDate] = useState<Date>(new Date());
  
  // Navigation functions
  const goToToday = () => setCurrentDate(new Date());
  
  const goToPrevious = () => {
    if (viewType === 'day') {
      setCurrentDate(addDays(currentDate, -1));
    } else if (viewType === 'week') {
      setCurrentDate(addWeeks(currentDate, -1));
    } else {
      setCurrentDate(addMonths(currentDate, -1));
    }
  };
  
  const goToNext = () => {
    if (viewType === 'day') {
      setCurrentDate(addDays(currentDate, 1));
    } else if (viewType === 'week') {
      setCurrentDate(addWeeks(currentDate, 1));
    } else {
      setCurrentDate(addMonths(currentDate, 1));
    }
  };
  
  // Navigate to a specific date
  const goToDate = (date: Date) => {
    setCurrentDate(date);
  };
  
  // Create a new event when time slot is selected
  const handleTimeSlotSelect = (start: Date, end: Date) => {
    if (onNewEvent) {
      onNewEvent(start, end);
    }
  };
  
  // Render active view
  const renderView = () => {
    switch (viewType) {
      case 'day':
        return (
          <DayView
            currentDate={currentDate}
            events={events}
            onEventClick={onEventClick}
            onTimeSlotSelect={handleTimeSlotSelect}
          />
        );
      case 'week':
        return (
          <WeekView
            currentDate={currentDate}
            events={events}
            onEventClick={onEventClick}
            onTimeSlotSelect={handleTimeSlotSelect}
          />
        );
      case 'month':
        return (
          <MonthView
            currentDate={currentDate}
            events={events}
            onEventClick={onEventClick}
            onDateSelect={(date) => {
              if (onDateSelect) {
                onDateSelect(date);
              } else {
                // If no handler provided, switch to day view on date click
                setCurrentDate(date);
                setViewType('day');
              }
            }}
          />
        );
      case 'agenda':
        return (
          <AgendaView
            currentDate={currentDate}
            events={events}
            onEventClick={onEventClick}
            onDateSelect={(date) => {
              setCurrentDate(date);
              setViewType('day');
            }}
          />
        );
    }
  };
  
  return (
    <div className="flex h-full overflow-hidden">
      <CalendarSidebar
        events={events}
        currentDate={currentDate}
        onDateSelect={goToDate}
      />
      <div className="flex flex-col flex-1 overflow-hidden">
        <CalendarHeader
          viewType={viewType}
          currentDate={currentDate}
          onViewChange={setViewType}
          onPrevious={goToPrevious}
          onNext={goToNext}
          onToday={goToToday}
        />
        <div className="flex-1 overflow-hidden">
          {renderView()}
        </div>
      </div>
    </div>
  );
}
