document.addEventListener('DOMContentLoaded', () => {
    // Fetch list of files from the server
    fetch('/files')
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = ''; // Clear existing content

            data.files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.textContent = file;
                fileList.appendChild(fileDiv);
            });
        })
        .catch(err => console.error('Error fetching files:', err));
});
