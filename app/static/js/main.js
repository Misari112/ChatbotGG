// app/static/main.js

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const pdfFileInput = document.getElementById('pdfFile');
    const userContextInput = document.getElementById('userContext');
    const chatArea = document.getElementById('chatArea');

    // Función para agregar mensajes al área de chat
    function appendMessage(sender, message, isUser) {
        const alignment = isUser ? 'chat-end' : 'chat-start';
        const avatarUrl = isUser
            ? 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp' // Avatar del usuario
            : 'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp'; // Avatar del chatbot

        // Formatear el mensaje: reemplazar ** por etiquetas <strong> y agregar saltos de línea
        const formattedMessage = message
            .replace(/_/g, ' ')                             // Quitar guiones bajos en nombres de agentes
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Reemplazar **texto** por <strong>texto</strong>
            .replace(/\n/g, '<br>');                        // Reemplazar saltos de línea por <br>

        const messageHtml = `
            <div class="chat ${alignment}">
                <div class="chat-image avatar">
                    <div class="w-10 rounded-full">
                        <img src="${avatarUrl}" alt="${sender}" />
                    </div>
                </div>
                <div class="chat-header">
                    ${sender}
                    <time class="text-xs opacity-50">${new Date().toLocaleTimeString()}</time>
                </div>
                <div class="chat-bubble">${formattedMessage}</div>
            </div>
        `;

        chatArea.insertAdjacentHTML('beforeend', messageHtml);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = pdfFileInput.files[0];
        const context = userContextInput.value.trim();

        if (!file) {
            alert('Por favor, seleccione un archivo PDF.');
            return;
        }

        // Agregar el mensaje del usuario al chat con el nombre del archivo y el contexto
        const userMessage = `Archivo: ${file.name}<br>Contexto: ${context}`;
        appendMessage('Tú', userMessage, true);

        // Limpiar los campos de entrada después de enviar
        pdfFileInput.value = '';
        userContextInput.value = '';

        const formData = new FormData();
        formData.append('pdfFile', file);
        formData.append('context', context);

        // Mostrar mensaje de espera en el lado del chatbot
        const waitingMessage = document.createElement('div');
        waitingMessage.classList.add('chat', 'chat-start');
        waitingMessage.innerHTML = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" alt="Gina" />
                </div>
            </div>
            <div class="chat-header">
                Gina
                <time class="text-xs opacity-50">${new Date().toLocaleTimeString()}</time>
            </div>
            <div class="chat-bubble chat-bubble-accent">
                Procesando su solicitud, por favor espere...
            </div>
        `;
        chatArea.appendChild(waitingMessage);
        chatArea.scrollTop = chatArea.scrollHeight;

        try {
            const response = await fetch('/evaluate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor.');
            }

            const result = await response.json();

            // Eliminar mensaje de espera
            chatArea.removeChild(waitingMessage);

            if (result.error) {
                appendMessage('Gina', result.error, false);
            } else {
                const sender = 'Gina';
                let content = result.message;

                // Formatear el contenido: quitar guiones bajos, reemplazar ** y agregar saltos de línea
                content = content
                    .replace(/_/g, ' ')                             // Quitar guiones bajos en nombres de agentes
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Reemplazar **texto** por <strong>texto</strong>
                    .replace(/\n/g, '<br>');                        // Reemplazar saltos de línea por <br>

                appendMessage(sender, content, false);
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al procesar su solicitud.');
            if (chatArea.contains(waitingMessage)) {
                chatArea.removeChild(waitingMessage);
            }
        }
    });
});
