import React from 'react';
import { AgentResponse } from '@/types';
import { FlightCard } from './flight-card';
import { HotelCard } from './hotel-card';
import { BookingDetailsCard } from './booking-details';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface ResultsViewProps {
  response: AgentResponse;
}

export function ResultsView({ response }: ResultsViewProps) {
  if (response.error) {
    return (
      <Alert variant="destructive" className="mb-4">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{response.error}</AlertDescription>
      </Alert>
    );
  }
  
  const hasDepartureFlights = response.departure_flights && response.departure_flights.length > 0;
  const hasReturnFlights = response.return_flights && response.return_flights.length > 0;
  const hasHotels = response.hotels && response.hotels.length > 0;
  
  return (
    <div className="space-y-4">
      <BookingDetailsCard details={response.booking_details} />
      
      <Tabs defaultValue="flights" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="flights">Flights</TabsTrigger>
          <TabsTrigger 
            value="hotels" 
            disabled={!hasHotels}
          >
            Hotels
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="flights" className="space-y-4">
          {hasDepartureFlights ? (
            <>
              <h3 className="text-lg font-semibold">Departure Flights</h3>
              {response.departure_flights?.map((flight) => (
                <FlightCard 
                  key={flight.flight_id} 
                  flight={flight} 
                  type="departure" 
                />
              ))}
            </>
          ) : (
            <Alert className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>No departure flights found</AlertTitle>
            </Alert>
          )}
          
          {hasReturnFlights && (
            <>
              <h3 className="text-lg font-semibold mt-6">Return Flights</h3>
              {response.return_flights?.map((flight) => (
                <FlightCard 
                  key={flight.flight_id} 
                  flight={flight} 
                  type="return" 
                />
              ))}
            </>
          )}
        </TabsContent>
        
        <TabsContent value="hotels" className="space-y-4">
          {hasHotels ? (
            <>
              <h3 className="text-lg font-semibold">Available Hotels</h3>
              {response.hotels?.map((hotel, index) => (
                <HotelCard key={index} hotel={hotel} />
              ))}
            </>
          ) : (
            <Alert className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>No hotels found</AlertTitle>
            </Alert>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}