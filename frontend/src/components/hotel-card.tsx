import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Hotel } from '@/types';
import { formatCurrency } from '@/lib/utils';
import { Building, CalendarRange } from 'lucide-react';

interface HotelCardProps {
  hotel: Hotel;
}

export function HotelCard({ hotel }: HotelCardProps) {
  return (
    <Card className="w-full mb-4">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Building className="h-5 w-5" />
            <CardTitle className="text-lg">{hotel.hotel_name}</CardTitle>
          </div>
          <CardDescription className="text-lg font-bold">
            {formatCurrency(hotel.price, hotel.currency)}
          </CardDescription>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-2">
          <CalendarRange className="h-4 w-4 text-muted-foreground" />
          <p className="text-sm">
            {new Date(hotel.check_in).toLocaleDateString()} - {new Date(hotel.check_out).toLocaleDateString()}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}