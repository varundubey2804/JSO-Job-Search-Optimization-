require('dotenv').config({ path: '../.env.example' });
const express = require('express');
const cors = require('cors');
const path = require('path');
const apiRoutes = require('./routes');

const app = express();
const PORT = process.env.GATEWAY_PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve frontend static files
app.use(express.static(path.join(__dirname, '../frontend')));

// API Routes
app.use('/api', apiRoutes);

// Error handler for JSON parsing or other middleware errors
app.use((err, req, res, next) => {
    if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
        return res.status(400).json({ detail: "Invalid JSON payload" });
    }

    // Ensure all API errors return JSON instead of Express default HTML
    if (req.path.startsWith('/api/')) {
        console.error('API Error:', err.message);
        return res.status(err.status || 500).json({ detail: err.message || "Internal Server Error" });
    }

    next(err);
});

// Catch all for unknown API routes
app.all('/api/*', (req, res) => {
    res.status(404).json({ detail: "API endpoint not found" });
});

// Catch all for frontend routing
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dashboards/user.html'));
});

app.listen(PORT, () => {
    console.log(`Gateway Server running on port ${PORT}`);
    console.log(`Proxying requests to ${process.env.BACKEND_URL || 'http://localhost:8000'}`);
});
