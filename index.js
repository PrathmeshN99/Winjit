const express = require("express");
const { exec } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.post("/query", (req, res) => {
  const userQuery = req.body.query;

  // Run the Python script in the background
  const pythonProcess = exec(
    "C:/Users/prath/AppData/Local/Programs/Python/Python310/python.exe hackathon.py",
    (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        res.status(500).json({ error: "Internal Server Error" });
        return;
      }

      // Parse the Python script output and send the response
      const relevantSection = stdout.trim();
      res.json({ mostRelevantSection: relevantSection });
    }
  );

  // Send the user query to the Python script
  pythonProcess.stdin.write(JSON.stringify({ query: userQuery }));
  pythonProcess.stdin.end();
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
