from database.dbcontext import db

def load_user_information(localId: str) -> dict:
    """
    Load user information from Firebase database
    
    Args:
        localId (str): User's unique identifier
        
    Returns:
        dict: User information with state indicator
    """
    try:
        # Get reference to user's information node
        ref = db.reference(f'usuarios/{localId}/informacion')
        
        # Get user information
        information = ref.get()
        
        # Check if information exists
        if information is None:
            return {
                "state": "failure",
                "error": "User information not found"
            }
        
        # Add success state
        information['state'] = "success"
        print(f"Retrieved information for user {localId}: {information}")
        
        return information
        
    except Exception as e:
        print(f"Error loading user information: {str(e)}")
        return {
            "state": "failure",
            "error": str(e)
        }
        
def get_subjects():
    try:
        # Get reference to subjects's information node
        ref = db.reference(f'materias')
        
        # Get user information
        subjects = ref.get()
        
        # Check if information exists
        if subjects is None:
            return {
                "state": "failure",
                "error": "Subjects information not found"
            }
        
        # Add success state
        subjects['state'] = "success"
        print(f"Retrieved information for subjects.")
        
        return subjects
        
    except Exception as e:
        print(f"Error loading subjects information: {str(e)}")
        return {
            "state": "failure",
            "error": str(e)
        }
        
def get_user_subjects(local_id):
    try:
        # Get reference to user subjects's information node
        ref = db.reference(f'usuarios/{local_id}/materiasInscritas')
        
        # Get user information
        subjects = ref.get()
        
        # Check if information exists
        if subjects is None:
            return {
                "state": "failure",
                "error": "User subjects information not found"
            }
        
        # Add success state
        subjects['state'] = "success"
        print(f"Retrieved information for user subjects.")
        print(subjects)
        
        return subjects
        
    except Exception as e:
        print(f"Error loading user subjects information: {str(e)}")
        return {
            "state": "failure",
            "error": str(e)
        }

def add_subject(localId, subject):
    try:
        data = {
            'materia': subject[0],
            'creditos': subject[1],
            'valor': subject[2]
        }
        
        # Get reference to subjects's information node
        ref = db.reference(f'usuarios/{localId}/materiasInscritas/{data["materia"]}')
        
        # Get user information
        ref.set(data)
        
        return {
            "state": "success"
        }
        
    except Exception as e:
        print(f"Error adding subject: {str(e)}")
        return {
            "state": "failure",
            "error": str(e)
        }
        
def delete_subject(localId, name_subject):
    try:
        
        # Get reference to subjects's information node
        ref = db.reference(f'usuarios/{localId}/materiasInscritas/{name_subject}')
        
        # Get user information
        ref.delete()
        
        return {
            "state": "success"
        }
        
    except Exception as e:
        print(f"Error deleting subject: {str(e)}")
        return {
            "state": "failure",
            "error": str(e)
        }