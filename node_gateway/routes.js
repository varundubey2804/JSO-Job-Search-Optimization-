const express = require('express');
const router = express.Router();
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const upload = multer({ dest: 'uploads/' }); // Temp storage for proxying file uploads

// Common helper to proxy requests to FastAPI backend
async function proxyRequest(req, res, method, urlPath, data = null, headers = {}) {
    try {
        const config = {
            method: method,
            url: `${BACKEND_URL}${urlPath}`,
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };

        // Forward Authorization header if present
        if (req.headers.authorization) {
            config.headers.Authorization = req.headers.authorization;
        }

        if (data) {
            config.data = data;
        }

        const response = await axios(config);
        res.status(response.status).json(response.data);
    } catch (error) {
        if (error.response) {
            res.status(error.response.status).json(error.response.data || { detail: "Unknown error from backend" });
        } else {
            console.error('Error forwarding request:', error.message);
            res.status(500).json({ error: 'Internal Gateway Error' });
        }
    }
}

// Routes
router.post('/generate-query', async (req, res) => {
    await proxyRequest(req, res, 'POST', '/api/generate-query', req.body);
});

router.post('/extract-skills', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ detail: "No file uploaded" });
        }

        // We use fs and form-data to forward the file to the python backend
        const fs = require('fs');
        const form = new FormData();
        form.append('file', fs.createReadStream(req.file.path), req.file.originalname);
        
        let headers = {
            ...form.getHeaders()
        };

        // Forward Authorization header if present
        if (req.headers.authorization) {
            headers.Authorization = req.headers.authorization;
        }

        const response = await axios.post(`${BACKEND_URL}/api/extract-skills`, form, { headers: headers });
        
        // Clean up temp file
        fs.unlinkSync(req.file.path);

        res.status(response.status).json(response.data);
    } catch (error) {
        if (req.file) {
            const fs = require('fs');
            if(fs.existsSync(req.file.path)) fs.unlinkSync(req.file.path);
        }
        if (error.response) {
            res.status(error.response.status).json(error.response.data || { detail: "Unknown error from backend" });
        } else {
            console.error('Error forwarding file request:', error.message);
            res.status(500).json({ error: 'Internal Gateway Error' });
        }
    }
});

router.get('/query-history', async (req, res) => {
    await proxyRequest(req, res, 'GET', '/api/query-history');
});

router.get('/analytics', async (req, res) => {
    await proxyRequest(req, res, 'GET', '/api/analytics');
});

module.exports = router;
