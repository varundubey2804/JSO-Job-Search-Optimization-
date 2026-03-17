document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('query-form');
    const resultsSection = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const btn = document.getElementById('generate-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const role = document.getElementById('role').value;
        const experience = document.getElementById('experience').value;
        const location = document.getElementById('location').value;
        const platform = document.getElementById('platform').value;
        const skillsStr = document.getElementById('skills').value;
        
        const skills = skillsStr.split(',').map(s => s.trim()).filter(s => s);

        const requestData = {
            role,
            skills,
            experience,
            location,
            platform
        };

        // UI Feedback
        loading.classList.remove('hidden');
        btn.disabled = true;
        resultsSection.classList.add('hidden');

        try {
            const response = await api.generateQuery(requestData);
            
            // Populate output
            document.getElementById('boolean-output').textContent = response.boolean_query;
            document.getElementById('xray-output').textContent = response.xray_query;
            
            const linksList = document.getElementById('links-output');
            linksList.innerHTML = '';
            response.search_links.forEach(link => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = link;
                a.target = '_blank';
                a.textContent = link.substring(0, 60) + '...';
                li.appendChild(a);
                linksList.appendChild(li);
            });

            resultsSection.classList.remove('hidden');
        } catch (error) {
            alert(`Error generating query: ${error.message}`);
        } finally {
            loading.classList.add('hidden');
            btn.disabled = false;
        }
    });
});
