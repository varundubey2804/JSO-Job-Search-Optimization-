document.addEventListener('DOMContentLoaded', () => {
    const candidateForm = document.getElementById('candidate-form');
    const extractBtn = document.getElementById('extract-btn');
    const loading = document.getElementById('loading');
    const tbody = document.getElementById('candidates-table-body');

    candidateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const nameInput = document.getElementById('candidate-name');
        const fileInput = document.getElementById('resume-upload');
        
        const name = nameInput.value;
        const file = fileInput.files[0];

        if (!name || !file) {
            alert('Please provide a name and upload a resume.');
            return;
        }

        loading.classList.remove('hidden');
        extractBtn.disabled = true;

        try {
            const response = await api.extractSkills(file);
            
            // Add row to table
            const tr = document.createElement('tr');
            
            const tdName = document.createElement('td');
            tdName.textContent = name;
            
            const tdSkills = document.createElement('td');
            tdSkills.textContent = response.skills.join(', ');
            
            const tdAction = document.createElement('td');
            const matchBtn = document.createElement('button');
            matchBtn.style.padding = "5px 10px";
            matchBtn.style.fontSize = "0.8rem";
            matchBtn.textContent = 'Generate Query';
            matchBtn.onclick = () => {
                alert(`Redirecting to generator for ${name} with skills: ${response.skills.join(', ')}`);
            };
            tdAction.appendChild(matchBtn);
            
            tr.appendChild(tdName);
            tr.appendChild(tdSkills);
            tr.appendChild(tdAction);
            
            tbody.appendChild(tr);

            // Reset form
            candidateForm.reset();
        } catch (error) {
            alert(`Error extracting skills: ${error.message}`);
        } finally {
            loading.classList.add('hidden');
            extractBtn.disabled = false;
        }
    });
});
