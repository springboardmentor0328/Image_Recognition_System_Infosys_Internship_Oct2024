// JavaScript for handling the Start Recognition button click
document.getElementById('start_recognition').addEventListener('click', function() {
    fetch('/start_recognition')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Show the initial message
        document.getElementById('status').innerText = data.status;

        // After 10 seconds, update the status to "Recognition Started"
        setTimeout(() => {
            document.getElementById('status').innerText = 'Recognition Started';
        }, 10000);  // Update after 10 seconds
    })
    .catch(error => {
        document.getElementById('status').innerText = 'Recognition Error: ' + error;
        console.error("Recognition error occurred:", error);  // Debugging info
    });
});


// Capture Button Functionality
document.addEventListener('DOMContentLoaded', function () {
    const startCaptureButton = document.getElementById('startCaptureButton');
    const nameInput = document.getElementById('nameInput');
    const statusDiv = document.getElementById('status');

    startCaptureButton.addEventListener('click', () => {
        const name = nameInput.value.trim();

        if (!name) {
            statusDiv.innerHTML = "<p style='color: red;'>Please enter a name.</p>";
            return;
        }

        statusDiv.innerHTML = "<p style='color: green;'>Starting capture for: " + name + "</p>";

        // Send POST request to start capturing
        fetch('/start_capture', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name })
        })
        .then(response => {
            if (response.ok) {
                statusDiv.innerHTML = "<p style='color: green;'>Capture started successfully for " + name + "</p>";
            } else {
                statusDiv.innerHTML = "<p style='color: red;'>Failed to start capture. Please try again.</p>";
            }
            return response.json();
        })
        .then(data => {
            console.log("Response from server:", data);
        })
        .catch(error => {
            console.error("Error:", error);
            statusDiv.innerHTML = "<p style='color: red;'>An error occurred. Please check the console for details.</p>";
        });
    });
});

