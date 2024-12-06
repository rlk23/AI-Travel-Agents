import React from "react";
import ChatWindow from "./components/Chat/ChatWindow";

const App = () => {
  return (
   
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* ChatWindow Section */}
      <ChatWindow />
    </div>
  );
};

export default App;
