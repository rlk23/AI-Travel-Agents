import React, { useState } from "react";
import { AppBar, Toolbar, Tabs, Tab, Box, Typography, Button } from "@mui/material";
import { Routes, Route, Link, useNavigate } from "react-router-dom";
import AccountSettings from "./Setting/AccountSettings";
import Preferences from "./Setting/Preferences";
import Notifications from "./Setting/Notifications";

const Settings = () => {
  const navigate = useNavigate();
  const [tabIndex, setTabIndex] = useState(0); // Track the selected tab

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);

    // Navigate to the appropriate route
    if (newValue === 0) navigate("account");
    else if (newValue === 1) navigate("preferences");
    else if (newValue === 2) navigate("notifications");
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Top Navigation Bar */}
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Settings
          </Typography>
        </Toolbar>
        <Tabs
          value={tabIndex}
          onChange={handleTabChange}
          centered
          textColor="inherit"
          indicatorColor="secondary"
        >
          <Tab label="Account Settings" />
          <Tab label="Preferences" />
          <Tab label="Notifications" />
        </Tabs>
      </AppBar>

      {/* Content Area */}
      <Box
        sx={{
          p: 3,
          minHeight: "calc(100vh - 64px)", // Adjust for the AppBar height
          backgroundColor: "#f9f9f9",
        }}
      >
        <Routes>
          <Route
            path="account"
            element={<AccountSettings email="" setEmail={() => {}} />}
          />
          <Route
            path="preferences"
            element={
              <Preferences darkModeEnabled={false} setDarkModeEnabled={() => {}} />
            }
          />
          <Route
            path="notifications"
            element={
              <Notifications
                notificationsEnabled={true}
                setNotificationsEnabled={() => {}}
              />
            }
          />
        </Routes>

        {/* Save Changes Button */}
        <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 4 }}>
          <Button variant="contained" color="primary">
            Save Changes
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default Settings;
