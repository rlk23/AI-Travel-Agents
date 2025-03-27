import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookingDetails } from '@/types';
import { CalendarDays, MapPin, Users, Building } from 'lucide-react';

interface BookingDetailsCardProps {
  details: BookingDetails;
}

export function BookingDetailsCard({ details }: BookingDetailsCardProps) {
  return (
    <Card className="w-full mb-4">
      <CardHeader>
        <CardTitle>Booking Details</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {details['Origin city'] && (
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Origin</p>
                <p>{details['Origin city']}</p>
              </div>
            </div>
          )}
          
          {details['Destination city'] && (
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Destination</p>
                <p>{details['Destination city']}</p>
              </div>
            </div>
          )}
          
          {details['Trip type'] && (
            <div className="flex items-center gap-2">
              <CalendarDays className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Trip Type</p>
                <p>{details['Trip type']}</p>
              </div>
            </div>
          )}
          
          {details['Number of passengers'] && (
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Passengers</p>
                <p>{details['Number of passengers']}</p>
              </div>
            </div>
          )}
          
          {details['Departure date'] && (
            <div className="flex items-center gap-2">
              <CalendarDays className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Departure</p>
                <p>{details['Departure date']}</p>
              </div>
            </div>
          )}
          
          {details['Return date'] && (
            <div className="flex items-center gap-2">
              <CalendarDays className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Return</p>
                <p>{details['Return date']}</p>
              </div>
            </div>
          )}
          
          {details['Hotel stay required'] === 'yes' && (
            <div className="flex items-center gap-2">
              <Building className="h-4 w-4 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Hotel Stay</p>
                <p>{details['Hotel check-in date']} to {details['Hotel check-out date']}</p>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}