let socket = null;

async function logout() {
    try {
        const response = await fetch('/v1/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });

        if (response.ok) {
            window.location.href = '/v1/auth';
        } else {
            console.error('logout error');
        }
    } catch (error) {
        console.error('Request error:', error);
    }
}

async function connectChat() {
    document.getElementById('logoutButton').onclick = logout;

    await loadMessages();
    connectWebSocket();
}

async function loadMessages() {
    try {
        const response = await fetch(`/v1/chat/messages`);
        const messages = await response.json();

        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = messages.map(message =>
            createMessageElement(message.content)
        ).join('');
    } catch (error) {
        console.error('Messages loading error:', error);
    }
}

function connectWebSocket() {
    if (socket) socket.close();

    socket = new WebSocket(`ws://${window.location.host}/v1/chat/ws`);

    socket.onopen = () => console.log('WebSocket connected');

    socket.onmessage = (event) => {
        const incomingMessage = JSON.parse(event.data);
        addMessage(incomingMessage.content);
    };

    socket.onclose = () => console.log('WebSocket connection closed');
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (message) {
        const payload = {content: message};

        try {
            await fetch('/v1/chat/messages', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            socket.send(JSON.stringify(payload));
            messageInput.value = '';
        } catch (error) {
            console.error('Sending message error:', error);
        }
    }
}

function addMessage(text) {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.insertAdjacentHTML('beforeend', createMessageElement(text));
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function createMessageElement(text) {
    return `<div class="message">${text}</div>`;
}

document.getElementById('sendButton').onclick = sendMessage;

document.getElementById('messageInput').onkeypress = async (e) => {
    if (e.key === 'Enter') {
        await sendMessage();
    }
};
