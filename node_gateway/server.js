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

// Catch all for frontend routing
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/dashboards/user.html'));
});

app.listen(PORT, () => {
    console.log(`Gateway Server running on port ${PORT}`);
    console.log(`Proxying requests to ${process.env.BACKEND_URL || 'http://localhost:8000'}`);
});
