document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const studentId = document.getElementById('studentId').value;
    const assignmentType = document.getElementById('assignmentType').value;
    const fileInput = document.getElementById('file');

    const formData = new FormData();
    formData.append('student_id', studentId);
    formData.append('assignment_type', assignmentType);
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        document.getElementById('result').innerHTML = `
            <strong>Status:</strong> ${response.ok ? 'Success' : 'Error'}<br>
            <strong>Message:</strong> ${result.message || result.detail || 'No response'}<br>
            <strong>Similarity:</strong> ${result.similarity_score !== undefined ? (result.similarity_score * 100).toFixed(2) + '%' : 'N/A'}
        `;
    } catch (error) {
        document.getElementById('result').innerText = 'Error uploading file.';
        console.error(error);
    }
});
