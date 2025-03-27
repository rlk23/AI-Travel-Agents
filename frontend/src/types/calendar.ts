export type CalendarViewType = 'day' | 'week' | 'month' | 'agenda';

export type EventType = 'flight' | 'hotel' | 'activity' | 'restaurant' | 'sightseeing' | 'transport';

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  type: EventType;
  details?: string;
  location?: string;
  color?: string;
  isAllDay?: boolean;
}