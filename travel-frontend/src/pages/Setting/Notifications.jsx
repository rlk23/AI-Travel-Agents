import React from "react";
import { Card, CardContent, Typography, Grid, Switch, FormControlLabel } from "@mui/material";

const Notifications = ({ notificationsEnabled, setNotificationsEnabled }) => (
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
                onChange={(e) => setNotificationsEnabled(e.target.checked)}
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
                onChange={(e) => setNotificationsEnabled(e.target.checked)}
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
                onChange={(e) => setNotificationsEnabled(e.target.checked)}
              />
            }
            label="SMS Notifications"
          />
        </Grid>
      </Grid>
    </CardContent>
  </Card>
);

export default Notifications;
