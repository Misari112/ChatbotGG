from typing import Dict
from flask import session
from database.db_functions import load_user_information

def get_user_information() -> Dict:
    """
    Get user information using session data and database lookup
    
    Returns:
        Dict: User information with state indicator
    """
    try:
        # Validate session
        if 'user' not in session:
            raise KeyError("User session not found")

        user = session['user']
        localId = user['localId']

        # Load user information from database
        print(f"Loading information for user ID: {localId}")
        information = load_user_information(localId)

        # Check if information was retrieved successfully
        if information.get('state') == "success":
            return information
        
        # Return basic info if database lookup failed
        return {
            'state': 'error',
            'nombre': user['email']
        }

    except Exception as e:
        print(f"Error in get_user_information: {str(e)}")
        return {
            'state': 'error',
            'nombre': session.get('user', {}).get('email', 'Unknown User')
        }