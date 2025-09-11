const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

// Set EJS as view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Serve static files (CSS, JS, images)
app.use(express.static(path.join(__dirname, "public")));

// Route for index
app.get("/", (req, res) => {
  res.render("index", { title: "Kochi Metro Decision System" });
});

// To handle form POST data
app.use(express.urlencoded({ extended: true }));

// Route for dashboard
app.get("/dashboard", (req, res) => {
  res.render("dashboard", { title: "Supervisor Dashboard" });
});

// Route to handle form submission
app.post("/process-input", (req, res) => {
  console.log(req.body); // See submitted form data in terminal
  // For now, just send a simple response
  res.send("Form submitted! Check your terminal for data.");
});

// Start server
app.listen(PORT, () => {
  console.log(`🚆 Server running at http://localhost:${PORT}`);
});
