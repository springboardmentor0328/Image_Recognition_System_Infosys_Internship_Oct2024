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
    })
    .catch(error => {
        document.getElementById('status').innerText = 'Recognition Error: ' + error;
        console.error("Recognition error occurred:", error);  // Debugging info
    });
});

