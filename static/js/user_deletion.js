document.addEventListener('DOMContentLoaded', function () {
    const startCaptureButton = document.getElementById('startDeletionButton');
    const nameInput = document.getElementById('nameInput');
    const statusDiv = document.getElementById('status');

    startCaptureButton.addEventListener('click', () => {
        const name = nameInput.value.trim();

        if (!name) {
            statusDiv.innerHTML = "<p style='color: red;'>Please enter a name.</p>";
            return;
        }

        statusDiv.innerHTML = "<p style='color: green;'>Starting Deleting for: " + name + "</p>";

        // Send POST request to start capturing
        fetch('/delete_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name })
        })
        .then(response => {
            if (response.ok) {
                statusDiv.innerHTML = "<p style='color: green;'>Deletion started successfully for " + name + "</p>";
            } else {
                statusDiv.innerHTML = "<p style='color: red;'>Failed to delete. Please try again.</p>";
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