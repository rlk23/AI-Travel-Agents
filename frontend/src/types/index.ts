// src/types/index.ts
export interface Message {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
  }
  
  export interface Flight {
    flight_id: string;
    airline: string;
    price: string;
    currency: string;
    duration: string;
    segments: FlightSegment[];
  }
  
  export interface FlightSegment {
    departure_airport: string;
    departure_time: string;
    arrival_airport: string;
    arrival_time: string;
    carrier_code: string;
    airline_name: string;
    flight_number: string;
    duration: string;
  }
  
  export interface Hotel {
    hotel_name: string;
    price: string;
    currency: string;
    check_in: string;
    check_out: string;
  }
  
  export interface BookingDetails {
    'Origin city'?: string;
    'Destination city'?: string;
    'Departure date'?: string;
    'Return date'?: string;
    'Trip type'?: string;
    'Number of passengers'?: number;
    'Hotel stay required'?: string;
    'Hotel check-in date'?: string;
    'Hotel check-out date'?: string;
    [key: string]: any;
  }
  
  export interface AgentResponse {
    departure_flights: Flight[];
    return_flights?: Flight[];
    hotels?: Hotel[];
    booking_details: BookingDetails;
    error?: string;
  }