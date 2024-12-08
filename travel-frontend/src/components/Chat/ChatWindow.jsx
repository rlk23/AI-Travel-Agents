import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, Paper } from "@mui/material";
import { styled } from "@mui/system";
import axios from "axios";

const ChatInput = styled(TextField)(({ theme }) => ({
  "& .MuiOutlinedInput-root": {
    borderRadius: "20px",
    padding: "10px",
    "& fieldset": {
      borderColor: "#E0E3E7",
    },
    "&:hover fieldset": {
      borderColor: "#B2BAC2",
    },
    "&.Mui-focused fieldset": {
      borderColor: theme.palette.primary.main,
    },
  },
}));

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  // Scroll to the latest message
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { text: input.trim(), sender: "user" };
      setMessages((prev) => [...prev, userMessage]);
      setInput("");

      try {
        const API_BASE_URL = "http://localhost:5002";
        const response = await axios.post(`${API_BASE_URL}/api/ai-agent`, {
          prompt: input.trim(),
        });

        const botMessage = formatFlightResponse(response.data);
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = {
          text: "Something went wrong. Please try again.",
          sender: "bot",
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    }
  };

  const formatFlightResponse = (data) => {
    if (data.error) {
      return { text: data.error, sender: "bot" };
    }

    let text = "Here are the available flights:\n\n";
    if (data.departure_flights?.length > 0) {
      text += "Departure Flights:\n";
      data.departure_flights.forEach((flight, index) => {
        text += `  Flight ${index + 1}:\n`;
        text += `    Price: ${flight.price} ${flight.currency}\n`;
        text += `    Departure: ${flight.departure_code} at ${flight.departure_time}\n`;
        text += `    Arrival: ${flight.arrival_code} at ${flight.arrival_time}\n`;
        text += `    Duration: ${flight.duration}\n\n`;
      });
    } else {
      text += "No departure flights available.\n";
    }

    if (data.return_flights?.length > 0) {
      text += "Return Flights:\n";
      data.return_flights.forEach((flight, index) => {
        text += `  Flight ${index + 1}:\n`;
        text += `    Price: ${flight.price} ${flight.currency}\n`;
        text += `    Departure: ${flight.departure_code} at ${flight.departure_time}\n`;
        text += `    Arrival: ${flight.arrival_code} at ${flight.arrival_time}\n`;
        text += `    Duration: ${flight.duration}\n\n`;
      });
    } else {
      text += "No return flights available.\n";
    }

    return { text, sender: "bot" };
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ display: "flex", height: "100vh", overflow: "hidden", flexDirection: "column" }}>
      {/* Chat History */}
      <Paper
        ref={chatRef}
        elevation={3}
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          padding: "10px",
          backgroundColor: "#f4f4f4",
        }}
      >
        {messages.map((msg, index) => (
          <Box
            key={index}
            sx={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              marginBottom: "10px",
            }}
          >
            <Typography
              sx={{
                display: "inline-block",
                padding: "10px",
                borderRadius: "10px",
                backgroundColor: msg.sender === "user" ? "#1976d2" : "#ffffff",
                color: msg.sender === "user" ? "#ffffff" : "#000000",
                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.2)",
                maxWidth: "80%",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.text}
            </Typography>
          </Box>
        ))}
      </Paper>

      {/* Input Section */}
      <Box
        sx={{
          display: "flex",
          padding: "10px",
          backgroundColor: "#ffffff",
          boxShadow: "0 -2px 5px rgba(0, 0, 0, 0.2)",
        }}
      >
        <ChatInput
          fullWidth
          placeholder="Type your message..."
          multiline
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSend}
          sx={{ marginLeft: "10px" }}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatWindow;
