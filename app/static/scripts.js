document.addEventListener('DOMContentLoaded', function() {
    // Toggle input fields based on selected input type
    document.getElementById('input_type').addEventListener('change', function() {
        if (this.value === 'text') {
            document.getElementById('textInput').style.display = 'block';
            document.getElementById('audioInput').style.display = 'none';
        } else {
            document.getElementById('textInput').style.display = 'none';
            document.getElementById('audioInput').style.display = 'block';
        }
    });

    // Handle form submission
    document.getElementById('summarizeForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch('/summarize', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('summary').innerText = data.summary;
            document.getElementById('keywords').innerText = data.keywords.join(', ');
            document.getElementById('output').style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle download button click
    document.getElementById('download').addEventListener('click', function() {
        const summaryText = document.getElementById('summary').innerText;
        const blob = new Blob([summaryText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'summary.txt';
        a.click();
        URL.revokeObjectURL(url);
    });

    // Handle copy button click
    document.getElementById('copy').addEventListener('click', function() {
        const summaryText = document.getElementById('summary').innerText;
        navigator.clipboard.writeText(summaryText).then(() => {
            alert('Summary copied to clipboard!');
        });
    });
});