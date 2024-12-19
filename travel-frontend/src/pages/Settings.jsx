import React, { useState } from "react";
import {
  Box,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Toolbar,
  Divider,
  Button,
} from "@mui/material";
import { Routes, Route, Link } from "react-router-dom";
import AccountSettings from "./Setting/AccountSettings";
import Preferences from "./Setting/Preferences";
import Notifications from "./Setting/Notifications";

const Settings = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [darkModeEnabled, setDarkModeEnabled] = useState(false);
  const [email, setEmail] = useState("");

  const menuItems = [
    { label: "Account Settings", path: "account" },
    { label: "Preferences", path: "preferences" },
    { label: "Notifications", path: "notifications" },
  ];

  return (
    <Box sx={{ display: "flex" }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: 240,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <List>
          {menuItems.map((item, index) => (
            <ListItem button key={index} component={Link} to={item.path}>
              <ListItemText primary={item.label} />
            </ListItem>
          ))}
        </List>
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          backgroundColor: "#f9f9f9",
          minHeight: "100vh",
        }}
      >
        <Toolbar />
        <Typography variant="h4" sx={{ mb: 4 }}>
          Settings
        </Typography>

        {/* Routing for different settings sections */}
        <Routes>
          <Route
            path="account"
            element={<AccountSettings email={email} setEmail={setEmail} />}
          />
          <Route
            path="preferences"
            element={
              <Preferences
                darkModeEnabled={darkModeEnabled}
                setDarkModeEnabled={setDarkModeEnabled}
              />
            }
          />
          <Route
            path="notifications"
            element={
              <Notifications
                notificationsEnabled={notificationsEnabled}
                setNotificationsEnabled={setNotificationsEnabled}
              />
            }
          />
        </Routes>

        <Divider sx={{ my: 4 }} />

        <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Button variant="contained" color="primary">
            Save Changes
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default Settings;
