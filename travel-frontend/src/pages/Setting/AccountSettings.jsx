import React from "react";
import { Card, CardContent, Typography, Grid, TextField } from "@mui/material";

const AccountSettings = ({ email, setEmail }) => (
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
);

export default AccountSettings;
