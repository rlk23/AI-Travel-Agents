import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Box } from "@mui/material";
import Sidebar from "./components/Sidebar/Sidebar";
import ChatWindow from "./components/Chat/ChatWindow";
import Booking from "./pages/booking"; 
import Itinerary from "./pages/itinerary";
import Calendar from "./pages/calendar";
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
            <Route path="../pages/booking" element={<Booking />} />
            <Route path="../pages/itinerary" element={<Itinerary />} />
            <Route path="../pages/calendar" element={<Calendar />} />
            <Route path="../pages/settings" element={<Settings />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App;
