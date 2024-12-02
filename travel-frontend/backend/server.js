const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");


const app = express();

app.use(cors());
app.use(bodyParser.json());

app.post("/api/ai-agent",(req,res) => {
    const {prompt} = req.body;

    const result = {
        flights: [{ id: "1", price: "$300", duration: "3h 30m" }],
        hotels: [{ name: "Hotel Paradise", price: "$150/night" }],
        activities: [{ name: "Scuba Diving", price: "$100" }],
      };
    
      res.json(result);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));



    