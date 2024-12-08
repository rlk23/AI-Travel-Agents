import React from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";

const localizer = momentLocalizer(moment);

const CalendarPage = () => {
  return (
    <div style={{ height: "90vh", padding: "20px" }}>
      <Calendar
        localizer={localizer}
        events={[]} // No events for now
        startAccessor="start"
        endAccessor="end"
        defaultView="week" // Default view is Week
        views={["month", "week", "day"]} // Enable Month, Week, and Day views
        style={{
          height: "100%",
          backgroundColor: "#fff",
          borderRadius: "8px",
          boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
        }}
      />
    </div>
  );
};

export default CalendarPage;
