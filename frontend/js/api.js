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

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'API request failed');
    }

    return response.json();
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
            // Don't set Content-Type here, let fetch handle the multipart/form-data boundary
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
