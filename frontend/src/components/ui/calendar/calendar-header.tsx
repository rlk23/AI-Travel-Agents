import React from 'react';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { CalendarViewType } from '@/types/calendar';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from '@/components/ui/select';
import { format } from 'date-fns';

interface CalendarHeaderProps {
  viewType: CalendarViewType;
  currentDate: Date;
  onViewChange: (view: CalendarViewType) => void;
  onPrevious: () => void;
  onNext: () => void;
  onToday: () => void;
}

export function CalendarHeader({
  viewType,
  currentDate,
  onViewChange,
  onPrevious,
  onNext,
  onToday
}: CalendarHeaderProps) {
  // Format the date range shown in the header
  const getHeaderText = () => {
    switch (viewType) {
      case 'day':
        return format(currentDate, 'EEEE, MMMM d, yyyy');
      case 'week':
        return `Week of ${format(currentDate, 'MMMM d, yyyy')}`;
      case 'month':
        return format(currentDate, 'MMMM yyyy');
      case 'agenda':
        return 'Agenda View';
    }
  };

  return (
    <div className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center space-x-2">
        <Button 
          variant="outline" 
          size="sm" 
          onClick={onToday}
        >
          Today
        </Button>
        
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={onPrevious}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={onNext}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
        
        <h2 className="text-xl font-semibold ml-2">
          {getHeaderText()}
        </h2>
      </div>
      
      <div className="flex items-center space-x-2">
        <Select 
          value={viewType} 
          onValueChange={(value) => onViewChange(value as CalendarViewType)}
        >
          <SelectTrigger className="w-[130px]">
            <SelectValue placeholder="Select view" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="day">Day</SelectItem>
            <SelectItem value="week">Week</SelectItem>
            <SelectItem value="month">Month</SelectItem>
            <SelectItem value="agenda">Agenda</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}