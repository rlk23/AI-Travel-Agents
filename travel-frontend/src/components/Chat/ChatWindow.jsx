import React, {useState} from 'react';
import {sendMessage} from "../services/chatServices";


const ChatWindow = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const handleSend = async () => {
        if (!input.trim()) return;


        const newMessage = {sender:"user", test: input};
        setMessages([...messages, newMessage]);

        try {
            const response = await sendMessage(input);
            setMessages([...messages, newMessage, { sender: "ai", text: response }]);
        } catch (error) {
          console.error("Error:", error);
        }
    
        setInput(""); // Clear input
      };

      rpythoneturn (
        <div className="chat-window">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    );

};

export default ChatWindow;