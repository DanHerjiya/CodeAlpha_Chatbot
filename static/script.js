
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");
const suggestionButtons = document.querySelectorAll(".suggestion");

function getTime() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}-message`;

    if (sender === "bot") {
        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.textContent = "C";
        message.appendChild(avatar);
    }

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    const time = document.createElement("span");
    time.className = "message-time";
    time.textContent = getTime();

    bubble.appendChild(time);
    message.appendChild(bubble);
    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(messageText) {
    const message = messageText.trim();

    if (!message) return;

    addMessage(message, "user");
    messageInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.reply || "Something went wrong.");
        }

        addMessage(data.reply, "bot");

    } catch (error) {
        addMessage(
            error.message || "Sorry, I could not connect to the chatbot. Please try again.",
            "bot"
        );
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
        messageInput.focus();
    }
}

chatForm.addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage(messageInput.value);
});

suggestionButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        sendMessage(button.textContent);
    });
});
