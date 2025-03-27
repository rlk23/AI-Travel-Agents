import React, { useState } from 'react';
import { CalendarLayout } from '@/components/ui/calendar/calendar-layout';
import { CalendarEvent, EventType } from '@/types/calendar';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogDescription
} from '@/components/ui/dialog';
import { format } from 'date-fns';

// Sample travel plans converted to calendar events format
const generateSampleEvents = (): CalendarEvent[] => {
  // Miami trip
  const miamiDeparture = new Date(2025, 3, 15, 10, 0);
  const miamiDepartureEnd = new Date(2025, 3, 15, 13, 30);
  const miamiReturn = new Date(2025, 3, 20, 15, 0);
  const miamiReturnEnd = new Date(2025, 3, 20, 18, 30);
  const miamiHotelStart = new Date(2025, 3, 15, 15, 0);
  const miamiHotelEnd = new Date(2025, 3, 20, 11, 0);
  
  // London trip
  const londonDeparture = new Date(2025, 5, 10, 19, 30);
  const londonDepartureEnd = new Date(2025, 5, 11, 8, 0);
  const londonHotelStart = new Date(2025, 5, 11, 10, 0);
  const londonHotelEnd = new Date(2025, 5, 15, 12, 0);
  
  // Activities for Miami
  const miamiActivities = [
    {
      id: 'act-1',
      title: 'South Beach Visit',
      start: new Date(2025, 3, 16, 10, 0),
      end: new Date(2025, 3, 16, 14, 0),
      type: 'activity' as EventType,
      location: 'South Beach, Miami',
      details: 'Relaxing day at the famous South Beach'
    },
    {
      id: 'act-2',
      title: 'Dinner at Versace Mansion',
      start: new Date(2025, 3, 17, 19, 0),
      end: new Date(2025, 3, 17, 21, 0),
      type: 'restaurant' as EventType,
      location: 'Ocean Drive, Miami Beach',
      details: 'Fine dining experience at the former Versace Mansion'
    },
    {
      id: 'act-3',
      title: 'Everglades Tour',
      start: new Date(2025, 3, 18, 9, 0),
      end: new Date(2025, 3, 18, 15, 0),
      type: 'sightseeing' as EventType,
      location: 'Everglades National Park',
      details: 'Airboat tour of the Everglades with wildlife spotting'
    }
  ];
  
  // Activities for London
  const londonActivities = [
    {
      id: 'act-4',
      title: 'British Museum Visit',
      start: new Date(2025, 5, 11, 13, 0),
      end: new Date(2025, 5, 11, 17, 0),
      type: 'sightseeing' as EventType,
      location: 'Great Russell St, London',
      details: 'Exploring the British Museum collections'
    },
    {
      id: 'act-5',
      title: 'London Eye Experience',
      start: new Date(2025, 5, 12, 16, 0),
      end: new Date(2025, 5, 12, 17, 30),
      type: 'activity' as EventType,
      location: 'South Bank, London',
      details: 'Panoramic views of London from the iconic London Eye'
    },
    {
      id: 'act-6',
      title: 'Dinner at The Shard',
      start: new Date(2025, 5, 13, 19, 0),
      end: new Date(2025, 5, 13, 21, 30),
      type: 'restaurant' as EventType,
      location: 'London Bridge, London',
      details: 'Fine dining with spectacular views at The Shard'
    }
  ];
  
  return [
    {
      id: 'flight-1',
      title: 'Flight to Miami',
      start: miamiDeparture,
      end: miamiDepartureEnd,
      type: 'flight',
      location: 'JFK to MIA',
      details: 'American Airlines, Flight AA123'
    },
    {
      id: 'flight-2',
      title: 'Return from Miami',
      start: miamiReturn,
      end: miamiReturnEnd,
      type: 'flight',
      location: 'MIA to JFK',
      details: 'American Airlines, Flight AA456'
    },
    {
      id: 'hotel-1',
      title: 'Oceanview Resort',
      start: miamiHotelStart,
      end: miamiHotelEnd,
      type: 'hotel',
      location: 'Miami Beach',
      details: '5 nights, Ocean View Room'
    },
    {
      id: 'flight-3',
      title: 'Flight to London',
      start: londonDeparture,
      end: londonDepartureEnd,
      type: 'flight',
      location: 'JFK to LHR',
      details: 'British Airways, Flight BA112'
    },
    {
      id: 'hotel-2',
      title: 'Downtown Hotel',
      start: londonHotelStart,
      end: londonHotelEnd,
      type: 'hotel',
      location: 'London City Center',
      details: '4 nights, Executive Suite'
    },
    ...miamiActivities,
    ...londonActivities
  ];
};

export function CalendarView() {
  const [events] = useState<CalendarEvent[]>(generateSampleEvents());
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  
  // Dialog open/close state
  const [dialogOpen, setDialogOpen] = useState(false);
  
  // Handle event click to show details
  const handleEventClick = (event: CalendarEvent) => {
    setSelectedEvent(event);
    setDialogOpen(true);
  };
  
  // Create a new event when a time slot is selected
  const handleNewEvent = (start: Date, end: Date) => {
    // In a real app, you would show a form to create an event
    console.log('Create event:', { start, end });
  };
  
  return (
    <div className="h-full">
      <CalendarLayout
        events={events}
        onEventClick={handleEventClick}
        onNewEvent={handleNewEvent}
      />
      
      {/* Event details dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          {selectedEvent && (
            <>
              <DialogHeader>
                <DialogTitle className="text-xl">{selectedEvent.title}</DialogTitle>
                <DialogDescription>
                  {format(selectedEvent.start, 'PPP')} • {format(selectedEvent.start, 'p')} - {format(selectedEvent.end, 'p')}
                </DialogDescription>
              </DialogHeader>
              
              <div className="space-y-4 mt-4">
                {selectedEvent.location && (
                  <div className="flex items-start">
                    <MapPin className="h-5 w-5 mr-2 mt-0.5 text-muted-foreground" />
                    <div>
                      <div className="font-medium">Location</div>
                      <div>{selectedEvent.location}</div>
                    </div>
                  </div>
                )}
                
                {selectedEvent.details && (
                  <div className="flex items-start">
                    <div className="h-5 w-5 mr-2"></div> {/* Spacer for alignment */}
                    <div>
                      <div className="font-medium">Details</div>
                      <div>{selectedEvent.details}</div>
                    </div>
                  </div>
                )}
                
                <div className="flex items-start">
                  <div className="h-5 w-5 mr-2"></div> {/* Spacer for alignment */}
                  <div>
                    <div className="font-medium">Event Type</div>
                    <div className="capitalize">{selectedEvent.type}</div>
                  </div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
