import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Toolbar, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography } from "@mui/material";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";

const drawerWidth = 240;

const Sidebar = ({ toggle, handleDrawerToggle }) => {
  const menuItems = [
    { text: "Chat", path: "/" },
    { text: "Booking", path: "/booking" },
    { text: "Itinerary", path: "/itinerary" },
    { text: "Calendar", path: "/calendar" },
    { text: "Settings", path: "/settings" },
  ];

  const navigate = useNavigate();

  return (
    <Box
      component="nav"
      sx={{
        width: { sm: toggle ? drawerWidth : 0 },
        flexShrink: { sm: 0 },
        transition: "width 0.3s",
        overflowX: "hidden",
        backgroundColor: "#F3F6F9",
        boxShadow: "2px 0px 5px rgba(0,0,0,0.1)",
        height: "100vh",
      }}
    >
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
          Sidebar
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map(({ text, path }, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton
              onClick={() => {
                navigate(path); // Navigate to the correct route
                handleDrawerToggle();
              }}
            >
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;
