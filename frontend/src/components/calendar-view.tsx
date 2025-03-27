import React, { useState } from 'react';
import { Calendar } from '@/components/ui/calendar';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { Plane, Hotel } from 'lucide-react';

// Sample travel plans for demonstration
const travelPlans = [
  {
    id: 1,
    type: 'flight',
    title: 'Flight to Miami',
    date: new Date(2025, 3, 15), // April 15, 2025
    details: 'JFK to MIA, American Airlines'
  },
  {
    id: 2,
    type: 'flight',
    title: 'Return from Miami',
    date: new Date(2025, 3, 20), // April 20, 2025
    details: 'MIA to JFK, American Airlines'
  },
  {
    id: 3,
    type: 'hotel',
    title: 'Oceanview Resort',
    date: new Date(2025, 3, 15), // April 15, 2025
    endDate: new Date(2025, 3, 20), // April 20, 2025
    details: 'Miami Beach, 5 nights'
  },
  {
    id: 4,
    type: 'flight',
    title: 'Flight to London',
    date: new Date(2025, 5, 10), // June 10, 2025
    details: 'JFK to LHR, British Airways'
  },
  {
    id: 5,
    type: 'hotel',
    title: 'Downtown Hotel',
    date: new Date(2025, 5, 10), // June 10, 2025
    endDate: new Date(2025, 5, 15), // June 15, 2025
    details: 'London, 5 nights'
  }
];

export function CalendarView() {
  const [date, setDate] = useState<Date | null>(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  
  // Filter travel plans for the selected date
  const filteredPlans = selectedDate 
    ? travelPlans.filter(plan => {
        if (plan.type === 'hotel' && plan.endDate) {
          // For hotels, check if selected date is within the stay period
          return (
            selectedDate >= new Date(plan.date) && 
            selectedDate <= new Date(plan.endDate)
          );
        } else {
          // For flights, just check the exact date
          return (
            selectedDate.getDate() === new Date(plan.date).getDate() &&
            selectedDate.getMonth() === new Date(plan.date).getMonth() &&
            selectedDate.getFullYear() === new Date(plan.date).getFullYear()
          );
        }
      })
    : [];

  return (
    <div className="p-4 h-full flex flex-col">
      <h1 className="text-2xl font-bold mb-4">Travel Calendar</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
        <Card>
          <CardHeader>
            <CardTitle>Your Trips</CardTitle>
            <CardDescription>View and manage your upcoming travel plans</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
          <Calendar
            mode="single"
            selected={date}
            onSelect={(newDate) => {
                setDate(newDate);
                setSelectedDate(newDate);
            }}
            className="rounded-md"
            disabled={{ before: new Date(2023, 0, 1) }}
            classNames={{
                day_selected: "bg-primary text-primary-foreground",
                day_today: "bg-accent text-accent-foreground",
                day: travelPlans.some(plan => 
                new Date(plan.date).toDateString() === date?.toDateString()
                ) ? "font-bold bg-primary/10 text-primary" : undefined
            }}
            />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>
              {selectedDate ? (
                <>Plans for {selectedDate.toLocaleDateString()}</>
              ) : (
                <>Select a date to view plans</>
              )}
            </CardTitle>
            <CardDescription>
              {filteredPlans.length} items scheduled
            </CardDescription>
          </CardHeader>
          <CardContent>
            {filteredPlans.length > 0 ? (
              <div className="space-y-4">
                {filteredPlans.map(plan => (
                  <div 
                    key={plan.id} 
                    className="flex items-start border-l-4 pl-3 py-1"
                    style={{
                      borderColor: plan.type === 'flight' 
                        ? 'hsl(var(--primary))' 
                        : 'hsl(var(--secondary))'
                    }}
                  >
                    <div className="mr-3 mt-1">
                      {plan.type === 'flight' ? (
                        <Plane className="h-5 w-5 text-primary" />
                      ) : (
                        <Hotel className="h-5 w-5 text-secondary" />
                      )}
                    </div>
                    <div>
                      <h3 className="font-medium">{plan.title}</h3>
                      <p className="text-sm text-muted-foreground">{plan.details}</p>
                      {plan.type === 'hotel' && plan.endDate && (
                        <Badge variant="outline" className="mt-1">
                          {new Date(plan.date).toLocaleDateString()} - {new Date(plan.endDate).toLocaleDateString()}
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : selectedDate ? (
              <p className="text-muted-foreground">No travel plans for this date.</p>
            ) : (
              <p className="text-muted-foreground">Click a date on the calendar to view your plans.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}