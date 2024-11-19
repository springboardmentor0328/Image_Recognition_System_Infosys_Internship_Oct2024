

document.addEventListener("DOMContentLoaded", function () {
    // Recognition Button
    const recognitionButton = document.getElementById("recognitionButton");
    if (recognitionButton) {
        recognitionButton.onclick = function () {
            window.location.href = "/recognition";
        };
    } else {
        console.error("Recognition button not found in the DOM");
    }

    // Back to Home Button
    const backToHomeButton = document.getElementById("backToHomeButton");
    if (backToHomeButton) {
        backToHomeButton.onclick = function () {
            window.location.href = "/";
        };
    } else {
        console.error("Back to Home button not found in the DOM");
    }

    // Register Button
    const registerButton = document.getElementById("registerButton");
    if (registerButton) {
        registerButton.onclick = function () {
            const username = document.getElementById("username").value;
            if (!username) {
                alert("Please enter your name.");
                return;
            }

            fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: username })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        const eventSource = new EventSource(`/register_stream?username=${username}`);
                        eventSource.onmessage = (event) => {
                            document.getElementById("message").innerText = event.data;
                            if (event.data === "Registration complete") {
                                eventSource.close();
                                alert("Registration completed!");
                                location.reload();
                                window.location.href = "/";
                            }
                        };

                        eventSource.onerror = () => {
                            eventSource.close();
                            alert("An error occurred during registration.");
                        };
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error occurred during registration.");
                });
        };
    } else {
        console.error("Register button not found in the DOM");
    }
});
