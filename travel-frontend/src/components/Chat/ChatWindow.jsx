import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, Paper } from "@mui/material";
import { styled } from "@mui/system";
import axios from "axios";

// Styled TextField for chat input
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

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  // Format flights for display
  const formatFlights = (flights, type) =>
    flights
      .map(
        (flight, index) =>
          `${type} Flight ${index + 1}:\n` +
          `  Price: ${flight.price.total} ${flight.price.currency}\n` +
          `  Departure: ${flight.departure}\n` +
          `  Arrival: ${flight.arrival}\n`
      )
      .join("\n");

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

        const { departure_flights, return_flights } = response.data;

        const formattedDepartureFlights = formatFlights(
          departure_flights,
          "Departure"
        );
        const formattedReturnFlights = formatFlights(
          return_flights,
          "Return"
        );

        const botMessage = {
          text: `Here are the results:\n\n${formattedDepartureFlights}\n${formattedReturnFlights}`,
          sender: "bot",
        };
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

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        padding: "10px",
        backgroundColor: "#FFFFFF",
      }}
    >
      {/* Chat Messages */}
      <Paper
        ref={chatRef}
        elevation={3}
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          padding: "10px",
          backgroundColor: "#f4f4f4",
          borderRadius: "10px",
          marginBottom: "10px",
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
          alignItems: "center",
          gap: "10px",
          padding: "10px",
          backgroundColor: "#ffffff",
          borderTop: "1px solid #E0E3E7",
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
