document.getElementById('sendLogin').addEventListener('click', sendLogin);
document.getElementById('password').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Evita que se añada una nueva línea
        sendLogin();  // Llama a la función para enviar el mensaje
    }
});

let errorShown = false;

function sendLogin() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Limpiar el input después de enviar el mensaje
    document.getElementById('password').value = '';

    // Hacer la solicitud al servidor para obtener la respuesta del login
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar la respuesta del chatbot en el chat
        if (data.code === 200){
            window.location.href = '/';
        } else {
            if (!errorShown) {
                appendError(data.message);
                errorShown = true;
            }
        }
        
    });
}

function appendError(message) {
    var errorArea = document.getElementById('errorArea');
    var messageHtml = `
        <p class="bg-red-100 text-red-800 p-4 rounded-lg shadow-md mb-4">${message}</p>
    `;
    errorArea.insertAdjacentHTML('beforeend', messageHtml);
}