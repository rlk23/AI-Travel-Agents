import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { ModeToggle } from '@/components/mode-toggle';

export function SettingsView() {
  return (
    <div className="p-4 h-full">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Appearance</CardTitle>
            <CardDescription>
              Customize how the app looks
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="theme">Theme</Label>
              <ModeToggle />
            </div>
            
            <div className="space-y-2">
              <Label>Text Size</Label>
              <RadioGroup defaultValue="medium">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="small" id="small" />
                  <Label htmlFor="small">Small</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="medium" id="medium" />
                  <Label htmlFor="medium">Medium</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="large" id="large" />
                  <Label htmlFor="large">Large</Label>
                </div>
              </RadioGroup>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
            <CardDescription>
              Manage your travel preferences
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="preferred-airline">Preferred Airline</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select airline" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="american">American Airlines</SelectItem>
                  <SelectItem value="delta">Delta</SelectItem>
                  <SelectItem value="united">United</SelectItem>
                  <SelectItem value="southwest">Southwest</SelectItem>
                  <SelectItem value="jetblue">JetBlue</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="seat-preference">Seat Preference</Label>
              <RadioGroup defaultValue="window">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="window" id="window" />
                  <Label htmlFor="window">Window</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="aisle" id="aisle" />
                  <Label htmlFor="aisle">Aisle</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="no-preference" id="no-preference" />
                  <Label htmlFor="no-preference">No Preference</Label>
                </div>
              </RadioGroup>
            </div>
            
            <div className="flex items-center space-x-2">
              <Switch id="notify" />
              <Label htmlFor="notify">Receive booking notifications</Label>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Units & Currency</CardTitle>
            <CardDescription>
              Change display formats
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="currency">Currency</Label>
              <Select defaultValue="usd">
                <SelectTrigger>
                  <SelectValue placeholder="Select currency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="usd">USD ($)</SelectItem>
                  <SelectItem value="eur">EUR (€)</SelectItem>
                  <SelectItem value="gbp">GBP (£)</SelectItem>
                  <SelectItem value="jpy">JPY (¥)</SelectItem>
                  <SelectItem value="cad">CAD ($)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="temperature">Temperature</Label>
              <RadioGroup defaultValue="fahrenheit">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="celsius" id="celsius" />
                  <Label htmlFor="celsius">Celsius (°C)</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="fahrenheit" id="fahrenheit" />
                  <Label htmlFor="fahrenheit">Fahrenheit (°F)</Label>
                </div>
              </RadioGroup>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="distance">Distance</Label>
              <RadioGroup defaultValue="miles">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="kilometers" id="kilometers" />
                  <Label htmlFor="kilometers">Kilometers (km)</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="miles" id="miles" />
                  <Label htmlFor="miles">Miles (mi)</Label>
                </div>
              </RadioGroup>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Account Settings</CardTitle>
            <CardDescription>
              Manage your account
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-2">
              <Switch id="marketing" defaultChecked />
              <Label htmlFor="marketing">Receive marketing emails</Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Switch id="travel-deals" defaultChecked />
              <Label htmlFor="travel-deals">Travel deals notifications</Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Switch id="data-collection" defaultChecked />
              <Label htmlFor="data-collection">Allow anonymized data collection</Label>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline">Reset Preferences</Button>
            <Button>Save Changes</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
