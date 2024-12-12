import React from "react";
import { Card, CardContent, Typography, Grid, Switch, FormControlLabel } from "@mui/material";

const Preferences = ({ darkModeEnabled, setDarkModeEnabled }) => (
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
      </Grid>
    </CardContent>
  </Card>
);

export default Preferences;
