const express = require('express');
const router = express.Router();
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const upload = multer({ storage: multer.memoryStorage() }); 

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
            // Improved logging to catch HTML error pages from FastAPI
            console.error(`[Gateway] Backend returned ${error.response.status} for ${urlPath}`);
            res.status(error.response.status).send(error.response.data);
        } else {
            console.error(`[Gateway] Connection Error to Backend:`, error.message);
            res.status(502).json({ detail: 'Bad Gateway: Could not connect to Python backend' });
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

        const form = new FormData();
        form.append('file', req.file.buffer, req.file.originalname);
        
        let headers = {
            ...form.getHeaders()
        };

        if (req.headers.authorization) {
            headers.Authorization = req.headers.authorization;
        }

        const response = await axios.post(`${BACKEND_URL}/api/extract-skills`, form, { headers: headers });
        
        res.status(response.status).json(response.data);
    } catch (error) {
        if (error.response) {
            console.error(`[Gateway] Backend returned ${error.response.status} for /api/extract-skills`);
            res.status(error.response.status).send(error.response.data);
        } else {
            console.error('[Gateway] Connection Error to Backend:', error.message);
            res.status(502).json({ detail: 'Bad Gateway: Could not connect to Python backend' });
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