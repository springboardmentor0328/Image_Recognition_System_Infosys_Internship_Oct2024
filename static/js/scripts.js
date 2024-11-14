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
document.getElementById('start_capture')?.addEventListener('click', function() {
    const personName = document.getElementById('person_name').value;
    if (!personName) {
        document.getElementById('status').innerText = 'Please enter a name before capturing.';
        return;
    }

    fetch('/start_capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: personName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('status').innerText = data.status;
    })
    .catch(error => {
        document.getElementById('status').innerText = 'Capture Error: ' + error;
        console.error("Capture error occurred:", error);
    });
});
