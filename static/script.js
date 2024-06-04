document.getElementById('fileInput').addEventListener('change', function() {
    const file = this.files[0];
    document.getElementById('fileName').textContent = file ? file.name : '';
});

document.getElementById('uploadBtn').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById('status').textContent = 'No file selected';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/.netlify/functions/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').textContent = data.message;
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Upload failed';
    });
});

document.getElementById('convertBtn').addEventListener('click', function() {
    fetch('/.netlify/functions/clean', {
        method: 'POST'
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'cleaned_file.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Conversion failed';
    });
});
