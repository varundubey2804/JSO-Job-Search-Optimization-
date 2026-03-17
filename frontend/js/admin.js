document.addEventListener('DOMContentLoaded', async () => {
    const totalQueriesEl = document.getElementById('total-queries');
    const activeUsersEl = document.getElementById('active-users');
    const topRolesBody = document.getElementById('top-roles-body');
    const aiLogsBody = document.getElementById('ai-logs-body');

    try {
        // Fetch Analytics
        const analytics = await api.getAnalytics();
        
        // Sum total queries
        const totalQueries = Object.values(analytics.queries_per_day).reduce((a, b) => a + b, 0);
        totalQueriesEl.textContent = totalQueries;
        activeUsersEl.textContent = analytics.active_users;

        // Populate Top Roles Table
        topRolesBody.innerHTML = '';
        for (const [role, count] of Object.entries(analytics.top_roles)) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${role}</td><td>${count}</td>`;
            topRolesBody.appendChild(tr);
        }

        // Fetch Recent History logs
        const historyResponse = await api.getHistory();
        const logs = historyResponse.history;

        aiLogsBody.innerHTML = '';
        logs.slice(0, 10).forEach(log => {
            const tr = document.createElement('tr');
            const dateStr = new Date(log.created_at).toLocaleString();
            tr.innerHTML = `
                <td>${dateStr}</td>
                <td>${log.user_id.substring(0, 8)}...</td>
                <td>${log.role}</td>
                <td><span style="color: var(--primary-color); font-weight: 500;">${log.platform}</span></td>
            `;
            aiLogsBody.appendChild(tr);
        });

    } catch (error) {
        console.error('Failed to load admin dashboard data:', error);
    }
});
