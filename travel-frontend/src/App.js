import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Box } from "@mui/material";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatWindow from "./components/Chat/ChatWindow";
import Booking from "./pages/booking"; 
import Itinerary from "./pages/itinerary";
import CalendarPage from "./pages/CalendarPage"; // Import the corrected CalendarPage component
import Settings from "./pages/Settings";

const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleSidebarToggle = () => {
    setSidebarOpen((prev) => !prev);
  };

  return (
    <Router>
      <Box sx={{ display: "flex", height: "100vh" }}>
        {/* Sidebar */}
        <Sidebar toggle={sidebarOpen} handleDrawerToggle={handleSidebarToggle} />

        {/* Main Content Area */}
        <Box sx={{ flexGrow: 1 }}>
          <Routes>
            <Route path="/" element={<ChatWindow />} />
            <Route path="/booking" element={<Booking />} />
            <Route path="/itinerary" element={<Itinerary />} />
            <Route path="/calendar" element={<CalendarPage />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App;
