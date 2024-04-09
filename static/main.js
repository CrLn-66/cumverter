const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const formatSelect = document.getElementById('format-select');
const progressBar = document.getElementById('progress');
const resultDiv = document.getElementById('result');
const socket = io(); // Connect to Socket.IO

uploadForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    const files = fileInput.files;
    const outputFormat = formatSelect.value;

    if (files.length === 0) {
        alert('Please select at least one file.');
        return;
    }

    // Show the progress bar
    progressBar.style.display = 'block';

    // Create FormData for sending files and form data
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]); 
    }
    formData.append('format', outputFormat);

    // Send files and form data using Fetch API (or XMLHttpRequest)
    fetch('/convert', { 
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Conversion failed');
        } 
        console.log('Conversion started!'); 
    })
    .catch(error => {
        console.error('Error:', error);
        // Update UI to show an error message 
    });
});

// Socket.IO progress listener
socket.on('progress', (data) => {
    const progressBar = document.getElementById('progress-bar');
    progressBar.value = (data.current / data.total_images) * 100; 

    // Display progress percentage: ...
    console.log(data.dlurl  );
    // If conversion is done, create the download link
    if (data.current === data.total_images) {
        const downloadLink = document.createElement('a');
        downloadLink.href = data.dlurl; 
        downloadLink.title = "my title text";
        // Add link to result section: ... 
        downloadLink.click();
    }
});
