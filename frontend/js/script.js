document.getElementById("summarizeButton").onclick = function() {
    const inputText = document.getElementById("inputText").value;
    const loadingIndicator = document.getElementById("loadingIndicator");
    loadingIndicator.style.display = 'block'; // Show the loading indicator

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("outputText").value = data.summary;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById("outputText").value = 'An error occurred. Please try again.';
    })
    .finally(() => {
        loadingIndicator.style.display = 'none'; // Hide the loading indicator
    });
};
