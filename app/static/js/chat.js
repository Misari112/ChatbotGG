document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Evita que se añada una nueva línea
        sendMessage();  // Llama a la función para enviar el mensaje
    }
});

function sendMessage() {
    var userMessage = document.getElementById('userInput').value;

    // Mostrar el mensaje del usuario en el chat
    appendMessage('Yo', userMessage, false);

    // Limpiar el input después de enviar el mensaje
    document.getElementById('userInput').value = '';

    // Hacer la solicitud al servidor para obtener la respuesta del chatbot
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        // Mostrar la respuesta del chatbot en el chat
        appendMessage('Chatbot', data.response, true);
    });
}

// Función para agregar mensajes al área de chat
function appendMessage(sender, message, isUser) {
    var chatArea = document.getElementById('chatArea');
    
    // Reemplazar los saltos de línea con <br> para que se muestren correctamente
    message = message.replace(/\n/g, '<br>');

    // Si es el mensaje del usuario, alinearlo a la izquierda; si es del chatbot, alinearlo a la derecha
    var alignment = isUser ? 'chat-start' : 'chat-end';

    var messageHtml = `
        <div class="chat ${alignment}">
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                </div>
            </div>
            <div class="chat-header">
                ${sender}
                <time class="text-xs opacity-50">${new Date().toLocaleTimeString()}</time>
            </div>
            <div class="chat-bubble">${message}</div>
        </div>
    `;
    
    chatArea.insertAdjacentHTML('beforeend', messageHtml);
    
    // Hacer scroll hacia abajo automáticamente cuando se agrega un nuevo mensaje
    chatArea.scrollTop = chatArea.scrollHeight;
}

