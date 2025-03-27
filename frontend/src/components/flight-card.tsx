import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Flight } from '@/types';
import { formatCurrency, formatDate, formatDuration } from '@/lib/utils';
import { Plane, Clock } from 'lucide-react';

interface FlightCardProps {
  flight: Flight;
  type: 'departure' | 'return';
}

export function FlightCard({ flight, type }: FlightCardProps) {
  const firstSegment = flight.segments[0];
  const lastSegment = flight.segments[flight.segments.length - 1];
  
  return (
    <Card className="w-full mb-4">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">{flight.airline}</CardTitle>
          <CardDescription className="text-lg font-bold">
            {formatCurrency(flight.price, flight.currency)}
          </CardDescription>
        </div>
        <CardDescription className="flex items-center gap-1">
          <Clock className="h-4 w-4" /> 
          {formatDuration(flight.duration)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between items-center">
          <div className="text-center">
            <p className="text-xl font-bold">{firstSegment.departure_airport}</p>
            <p className="text-sm">{formatDate(firstSegment.departure_time)}</p>
          </div>
          
          <div className="flex-1 mx-4 flex flex-col items-center">
            <div className="w-full flex items-center">
              <div className="h-0.5 flex-1 bg-muted"></div>
              <Plane className={`h-5 w-5 mx-2 ${type === 'return' ? 'rotate-180' : ''}`} />
              <div className="h-0.5 flex-1 bg-muted"></div>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {flight.segments.length > 1 
                ? `${flight.segments.length} stops` 
                : 'Direct flight'}
            </p>
          </div>
          
          <div className="text-center">
            <p className="text-xl font-bold">{lastSegment.arrival_airport}</p>
            <p className="text-sm">{formatDate(lastSegment.arrival_time)}</p>
          </div>
        </div>
      </CardContent>
      <CardFooter className="pt-0">
        <p className="text-sm text-muted-foreground">
          Flight {flight.segments.map(s => s.flight_number).join(', ')}
        </p>
      </CardFooter>
    </Card>
  );
}
