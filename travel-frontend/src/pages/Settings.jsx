import React, { useState } from "react";
import {
  Box,
  Typography,
  Grid,
  Switch,
  TextField,
  Button,
  FormControlLabel,
  Divider,
  Card,
  CardContent,
} from "@mui/material";

const Settings = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [darkModeEnabled, setDarkModeEnabled] = useState(false);
  const [email, setEmail] = useState("");

  const handleSave = () => {
    alert("Settings saved successfully!");
  };

  return (
    <Box
      sx={{
        padding: "20px",
        backgroundColor: "#f9f9f9",
        minHeight: "100vh",
      }}
    >
      <Typography variant="h4" sx={{ mb: 4 }}>
        Settings
      </Typography>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Account Settings
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Password"
                type="password"
                placeholder="Update your password"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Preferences
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={darkModeEnabled}
                    onChange={(e) => setDarkModeEnabled(e.target.checked)}
                  />
                }
                label="Enable Dark Mode"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={notificationsEnabled}
                    onChange={(e) =>
                      setNotificationsEnabled(e.target.checked)
                    }
                  />
                }
                label="Enable Notifications"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Notification Settings
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <FormControlLabel
                control={
                  <Switch
                    checked={notificationsEnabled}
                    onChange={(e) =>
                      setNotificationsEnabled(e.target.checked)
                    }
                  />
                }
                label="Email Notifications"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControlLabel
                control={
                  <Switch
                    checked={notificationsEnabled}
                    onChange={(e) =>
                      setNotificationsEnabled(e.target.checked)
                    }
                  />
                }
                label="Push Notifications"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControlLabel
                control={
                  <Switch
                    checked={notificationsEnabled}
                    onChange={(e) =>
                      setNotificationsEnabled(e.target.checked)
                    }
                  />
                }
                label="SMS Notifications"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Divider sx={{ my: 4 }} />

      <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
        <Button variant="contained" color="primary" onClick={handleSave}>
          Save Changes
        </Button>
      </Box>
    </Box>
  );
};

export default Settings;
