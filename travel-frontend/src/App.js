import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [prompt, setPrompt] = useState(""); // User input
  const [result, setResult] = useState(null); // Backend response
  const [loading, setLoading] = useState(false); // Loading state

  const handlePromptSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      // Replace with your API endpoint
      const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";
      const response = await axios.post(`${API_BASE_URL}/api/ai-agent`, { prompt });

      setResult(response.data); // Set result from backend
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "Something went wrong. Please try again." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Travel AI Agent</h1>
      <form onSubmit={handlePromptSubmit} style={{ marginBottom: "20px" }}>
        <textarea
          rows="5"
          cols="50"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your travel plans here..."
          style={{ padding: "10px", fontSize: "16px" }}
        />
        <br />
        <button type="submit" style={{ padding: "10px 20px", fontSize: "16px" }}>
          Generate Itinerary
        </button>
      </form>
      {loading && <p>Loading...</p>}
      {result && (
        <div>
          <h2>Generated Results:</h2>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", borderRadius: "5px" }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
