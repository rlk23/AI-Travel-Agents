import React from "react";
import { Box, Toolbar, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography } from "@mui/material";

import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";

const drawerWidth = 240;

const Sidebar = ({ toggle, handleDrawerToggle }) => {
  const menuItems = ["Chat","Booking","Itinerary","Calendar","Settings"];

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
      {/* Sidebar Header */}
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
          Sidebar
        </Typography>
      </Toolbar>
      <Divider />

      {/* Sidebar Menu */}
      <List>
        {menuItems.map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton onClick={handleDrawerToggle}>
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
