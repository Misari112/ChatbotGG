from typing import Dict, Tuple
from flask import session, jsonify
from database.dbcontext import firebase

def login_flow(email: str, password: str):
    """
    Handle user authentication with Firebase
    
    Args:
        email (str): User's email
        password (str): User's password
        
    Returns:
        flask.Response: JSON response with authentication result
    """
    try:
        # Input validation
        if not email or not password:
            return jsonify({
                "message": "Email y contraseña son requeridos.",
                "code": 400
            }), 400

        # Attempt authentication
        print(f"Attempting login for user: {email}")
        auth = firebase.authentication
        user_data = auth.sign_in_with_email_and_password(email, password)
        
        # Store user data in session
        session['user'] = {
            'localId': user_data.get('localId'),
            'email': user_data.get('email'),
            'idToken': user_data.get('idToken')
        }
        
        print(f"Login successful for user: {email}")
        return jsonify({
            "message": "Inicio de sesión correcto.",
            "code": 200
        }), 200

    except Exception as e:
        error_message = str(e)
        error_code = 400
        
        # Handle specific Firebase auth errors
        if "INVALID_PASSWORD" in error_message:
            message = "Contraseña incorrecta."
        elif "EMAIL_NOT_FOUND" in error_message:
            message = "Email no encontrado."
        elif "INVALID_EMAIL" in error_message:
            message = "Formato de email inválido."
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
            message = "Demasiados intentos. Intente más tarde."
            error_code = 429
        else:
            message = "Error en inicio de sesión."
            print(f"Login error: {error_message}")
        
        return jsonify({
            "message": message,
            "code": error_code
        }), error_code

# Example usage in a Flask route:
"""
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_flow(data.get('email'), data.get('password'))
"""