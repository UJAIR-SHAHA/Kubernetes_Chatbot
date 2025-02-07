document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        // Display user message
        displayMessage(userMessage, "user");
        userInput.value = ""; // Clear input field

        // Make API request to backend
        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: userMessage })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    displayMessage(data.error, "bot");
                } else {
                    displayMessage(data.response, "bot");
                }
            })
            .catch(error => {
                displayMessage("An error occurred. Please try again later.", "bot");
                console.error(error);
            });
    }

    function displayMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);

        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
