const API_BASE_URL = window.location.origin + '/api';

// Simple mock for getting token based on current page
function getToken() {
    const path = window.location.pathname;
    if (path.includes('admin.html')) return 'Bearer mock-admin-token';
    if (path.includes('hr.html')) return 'Bearer mock-hr-token';
    if (path.includes('licensing.html')) return 'Bearer mock-licensing-token';
    return 'Bearer mock-user-token';
}

async function fetchAPI(endpoint, options = {}) {
    const headers = {
        'Authorization': getToken(),
        ...options.headers
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        // 1. Check if the response is OK (200-299)
        if (!response.ok) {
            // 2. Read the raw text first before trying to parse JSON
            const rawText = await response.text();
            
            console.error(`[API Error] HTTP ${response.status} on ${endpoint}`);
            console.error("[Raw Response Body]:", rawText);

            let errorMessage = `API Error ${response.status}`;
            
            // 3. Try to parse it as JSON to extract a specific detail message
            try {
                const errorData = JSON.parse(rawText);
                if (errorData.detail) errorMessage = errorData.detail;
                else if (errorData.error) errorMessage = errorData.error;
            } catch (e) {
                // If it's not JSON (like an HTML error page), show a snippet of the raw text
                errorMessage = `Server Error. Check console. Snippet: ${rawText.substring(0, 100)}...`;
            }

            throw new Error(errorMessage);
        }

        // 4. If OK, parse and return JSON
        return await response.json();

    } catch (error) {
        console.error("Fetch API caught an error:", error);
        throw error; // Re-throw so the UI can display it
    }
}

const api = {
    generateQuery: async (data) => {
        return fetchAPI('/generate-query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    },

    extractSkills: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return fetchAPI('/extract-skills', {
            method: 'POST',
            body: formData,
        });
    },

    getHistory: async () => {
        return fetchAPI('/query-history');
    },

    getAnalytics: async () => {
        return fetchAPI('/analytics');
    }
};

// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const body = document.body;
            if (body.getAttribute('data-theme') === 'dark') {
                body.setAttribute('data-theme', 'light');
                themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                body.setAttribute('data-theme', 'dark');
                themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
            }
        });
    }
});