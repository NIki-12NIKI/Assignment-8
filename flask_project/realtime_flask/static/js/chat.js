document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const chatbox = document.getElementById('chatbox');
    const messageInput = document.getElementById('message');
    const sendButton = document.getElementById('send');

    // Send message to server
    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message) {
            socket.send(message);
            messageInput.value = '';  // Clear the input field
        }
    });

    // Display incoming messages
    socket.on('message', (msg) => {
        const newMessage = document.createElement('p');
        newMessage.innerText = msg;
        chatbox.appendChild(newMessage);
        chatbox.scrollTop = chatbox.scrollHeight;  // Auto scroll to the bottom
    });
});
