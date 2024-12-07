import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Paper, Typography, IconButton } from "@mui/material";
import { styled } from "@mui/system";
import axios from "axios";
import MenuIcon from "@mui/icons-material/Menu";

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

        const botMessage = { text: response.data, sender: "bot" };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        setMessages((prev) => [
          ...prev,
          { text: "Something went wrong. Please try again.", sender: "bot" },
        ]);
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
    <Box sx={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      {/* Main Chat Area */}
      <Box
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          backgroundColor: "#FFFFFF",
          padding: "10px",
        }}
      >
        {/* Chat Header */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "10px",
            borderBottom: "1px solid #E0E3E7",
            backgroundColor: "#F3F6F9",
          }}
        >
          <Typography variant="h6">Chat Window</Typography>
        </Box>

        {/* Chat History */}
        <Paper
          ref={chatRef}
          elevation={3}
          sx={{
            flexGrow: 1,
            overflowY: "auto",
            padding: "10px",
            borderRadius: "10px",
            marginBottom: "10px",
          }}
        >
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <Box
                key={index}
                sx={{
                  marginBottom: "10px",
                  textAlign: msg.sender === "user" ? "right" : "left",
                }}
              >
                <Typography
                  sx={{
                    display: "inline-block",
                    padding: "10px",
                    borderRadius: "15px",
                    backgroundColor:
                      msg.sender === "user" ? "#1976d2" : "#F3F6F9",
                    color: msg.sender === "user" ? "#ffffff" : "#000000",
                    maxWidth: "80%",
                    wordBreak: "break-word",
                  }}
                >
                  {msg.text}
                </Typography>
              </Box>
            ))
          ) : (
            <Typography color="textSecondary" align="center">
              Start the conversation!
            </Typography>
          )}
        </Paper>

        {/* Chat Input */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            position: "sticky",
            bottom: "10px",
            backgroundColor: "#FFFFFF",
            padding: "10px",
            boxShadow: "0 -2px 5px rgba(0,0,0,0.1)",
          }}
        >
          <ChatInput
            fullWidth
            placeholder="Type your message..."
            multiline
            minRows={1}
            maxRows={5}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSend}
            sx={{ borderRadius: "50px" }}
          >
            Send
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatWindow;
