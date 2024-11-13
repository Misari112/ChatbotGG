from enum import Enum
from database.db_functions import get_subjects, add_subject, get_user_subjects, delete_subject
from typing import Dict, Any
from flask import session
from utils.utils import transform_structure
from nltk.tokenize import word_tokenize

class ConversationState(Enum):
    INITIAL = "initial"
    GREETING = "greeting"
    MENU = "menu"
    # Consult flow
    SHOW_ASSIGNMENTS = "show_assignments"
    # Add flow
    ADD_ASSIGNMENT = "add_assignment"
    CONFIRM_ADD = "confirm_add"
    # Delete flow
    DELETE_ASSIGNMENT = "delete_assignment"
    CONFIRM_DELETE = "confirm_delete"
    COMPLETED = "completed"
    
class AssignmentChatHandler:
    def __init__(self):
        self
    
    def get_subjects(self) -> list:
        """Obtener todas las materias de la base de datos en tiempo real"""
        subjects_ref = get_subjects()
        return subjects_ref
    
    def get_user_subjects(self) -> list:
        """Obtener las materias del usuario desde la base de datos en tiempo real"""
        # Validar sesión
        if 'user' not in session:
            raise KeyError("Sesión de usuario no encontrada")

        user = session['user']
        localId = user['localId']
        
        subjects_ref = get_user_subjects(localId)
        return subjects_ref
        
    def get_available_subjects(self) -> dict:
        """Obtener materias disponibles para el usuario"""
        # Obtener todas las materias y las materias del usuario
        all_subjects = self.get_subjects()
        user_subjects = self.get_user_subjects()
        
        # Obtener el conjunto de nombres de materias
        user_subject_names = set(user_subjects.keys()) - {'state'}
        all_subject_names = set(all_subjects.keys()) - {'state'}
        
        # Encontrar materias que el usuario no tiene
        available_subject_names = all_subject_names - user_subject_names
        
        # Construir y retornar el diccionario de materias disponibles
        available_subjects = {subject: all_subjects[subject] for subject in available_subject_names}
        
        return available_subjects
    
    def add_assignment(self, assignment_id) -> dict:
        # Obtener todas las materias y las materias del usuario
        all_subjects = self.get_subjects()
        user_subjects = self.get_user_subjects()
        
        # Obtener el conjunto de nombres de materias
        user_subject_names = set(user_subjects.keys()) - {'state'}
        all_subject_names = set(all_subjects.keys()) - {'state'}
        
        # Encontrar materias que el usuario no tiene
        available_subject_names = all_subject_names - user_subject_names
        
        # Construir el diccionario de materias disponibles
        available_subjects = {subject: all_subjects[subject] for subject in available_subject_names}
        
        # Verificar si el assignment_id está en available_subjects
        if assignment_id in available_subjects:
            subject_data = available_subjects[assignment_id]
            
            # Agregar la materia a la base de datos usando la función `add_subject`
            user = session['user']
            localId = user['localId']
            
            # Llamada a `add_subject` con los datos de la asignatura
            result = add_subject(localId, [assignment_id, subject_data['creditos'], subject_data['valor']])
            
            return result['state'] == "success"
    
        return False
    
    def delete_assignment(self, assignment_id: str) -> bool:
        try:
            # Obtener el ID del usuario desde la sesión
            user = session['user']
            localId = user['localId']
            
            # Llamada a `delete_subject` con el nombre de la asignatura
            result = delete_subject(localId, assignment_id)
            
            return result['state'] == "success"
            
        except Exception as e:
            print(f"Error eliminando la materia: {e}")
            return False
    
    def handle_chat(self, current_state: str, user_message: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Manejador principal del chat"""
        
        # Estado inicial - saludo
        if current_state == ConversationState.INITIAL.value:
            tokens = word_tokenize(user_message.lower())
            if any(word in tokens for word in ["hola", "hey", "buenas", "saludos", "buen día", "buenas tardes", "buenas noches", "qué tal", "hola qué tal"]):
                return {
                    'next_state': ConversationState.MENU.value,
                    'response': (
                        "¡Hola! ¿Qué te gustaría hacer?\n"
                        "1. Consultar mis materias\n"
                        "2. Agregar materia\n"
                        "3. Eliminar materia\n"
                        "4. Todas las materias\n"
                        "5. Salir\n"
                    ),
                    'data': {}
                }
            return {
                'next_state': ConversationState.INITIAL.value,
                'response': "Por favor, empieza con un saludo (escribe 'hola')",
                'data': {}
            }
        
        # Estado de menú - manejar opciones
        elif current_state == ConversationState.MENU.value:
            if user_message.strip() == '1':  # Consultar
                assignments = self.get_user_subjects()
                
                if not assignments or assignments['state'] == "failure":
                    return {
                        'next_state': ConversationState.MENU.value,
                        'response': "No tienes materias inscritas. ¿Qué te gustaría hacer?\n1. Consultar mis materias\n2. Agregar materia\n3. Eliminar materia\n4. Todas las materias\n5. Salir",
                        'data': {}
                    }
                    
                assignments_formateado = "\n".join([f"{materia}: Créditos {details['creditos']} Valor {details['valor']}" for materia, details in assignments.items() if materia != 'state'])
                return {
                    'next_state': ConversationState.SHOW_ASSIGNMENTS.value,
                    'response': (
                        "Estas son tus materias actuales:\n\n"
                        f"{assignments_formateado}\n\n"
                        "Escribe 'menu' para volver al menú principal o 'salir' para terminar la conversación"
                    ),
                    'data': {'assignments': assignments}
                }
                
            elif user_message.strip() == '2':  # Agregar
                available = self.get_available_subjects()
                if not available:
                    return {
                        'next_state': ConversationState.MENU.value,
                        'response': "No hay materias disponibles para agregar. ¿Qué te gustaría hacer?\n1. Consultar mis materias\n2. Agregar materia\n3. Eliminar materia\n4. Todas las materias\n5. Salir",
                        'data': {}
                    }
                    
                available_formateado = "\n".join([f"{materia}: Créditos {details['creditos']} Valor {details['valor']}" for materia, details in available.items()])
                return {
                    'next_state': ConversationState.ADD_ASSIGNMENT.value,
                    'response': (
                        "Materias disponibles:\n\n"
                        f"{available_formateado}\n\n"
                        "Escribe el nombre de la materia que deseas agregar:"
                    ),
                    'data': {'available_assignments': available}
                }
                
            elif user_message.strip() == '3':  # Eliminar
                delete_available = self.get_user_subjects()
                print(delete_available)
                if delete_available['state'] != "failure":
                    delete_available = transform_structure(delete_available)
                    delete_available['state'] = "success"
                if not delete_available or delete_available['state'] == 'failure':
                    return {
                        'next_state': ConversationState.MENU.value,
                        'response': "No tienes materias para eliminar. ¿Qué te gustaría hacer?\n1. Consultar mis materias\n2. Agregar materia\n3. Eliminar materia\n4. Todas las materias\n5. Salir",
                        'data': {}
                    }
                    
                delete_available_formateado = "\n".join([f"{materia}: Créditos {details['creditos']} Valor {details['valor']}" for materia, details in delete_available.items() if materia != 'state'])
                return {
                    'next_state': ConversationState.DELETE_ASSIGNMENT.value,
                    'response': (
                        "Tus materias actuales:\n\n"
                        f"{delete_available_formateado}\n\n"
                        "Escribe el ID de la materia que deseas eliminar:"
                    ),
                    'data': {'delete_assignments': delete_available}
                }
                
            elif user_message.strip() == '4':  # Consultar todas
                assignments = self.get_subjects()
                assignments_formateado = "\n".join([f"{materia}: Créditos {details['creditos']} Valor {details['valor']}" for materia, details in assignments.items() if materia != 'state'])
                return {
                    'next_state': ConversationState.SHOW_ASSIGNMENTS.value,
                    'response': (
                        "Estas son todas las materias:\n\n"
                        f"{assignments_formateado}\n\n"
                        "Escribe 'menu' para volver al menú principal o 'salir' para terminar la conversación"
                    ),
                    'data': {'assignments': assignments}
                }
                
            elif user_message.strip() == '5':  # Salir
                return {
                    'next_state': ConversationState.COMPLETED.value,
                    'response': "¡Adiós!",
                    'data': {}
                }
                
            return {
                'next_state': ConversationState.MENU.value,
                'response': "Por favor, selecciona una opción válida (1-5)",
                'data': {}
            }
        
        # Estado de mostrar materias
        elif current_state == ConversationState.SHOW_ASSIGNMENTS.value:
            if user_message.lower().strip() == 'menu':
                return {
                    'next_state': ConversationState.MENU.value,
                    'response': "¿Qué te gustaría hacer?\n1. Consultar mis materias\n2. Agregar materia\n3. Eliminar materia\n4. Todas las materias\n5. Salir",
                    'data': {}
                }
            elif user_message.lower().strip() == 'salir':
                return {
                    'next_state': ConversationState.COMPLETED.value,
                    'response': "¡Adiós!",
                    'data': {}
                }
            return {
                'next_state': ConversationState.SHOW_ASSIGNMENTS.value,
                'response': "Escribe 'menu' para volver al menú principal o 'salir' para terminar la conversación",
                'data': session_data
            }
        
        # Estado de agregar materia
        elif current_state == ConversationState.ADD_ASSIGNMENT.value:
            available = session_data.get('available_assignments', [])
            print(available)
            assignment_name = user_message.strip()
            # Confirmar y agregar la materia
            if assignment_name not in available:
                return {
                    'next_state': ConversationState.ADD_ASSIGNMENT.value,
                    'response': "Por favor, selecciona una materia válida:",
                    'data': session_data
                }
            result = self.add_assignment(assignment_name)
            if result:
                return {
                    'next_state': ConversationState.MENU.value,
                    'response': (
                        "Materia agregada exitosamente.\n\n"
                        "¿Qué te gustaría hacer?\n"
                        "1. Consultar mis materias\n"
                        "2. Agregar materia\n"
                        "3. Eliminar materia\n"
                        "4. Todas las materias\n"
                        "5. Salir"
                    ),
                    'data': {}
                }
            return {
                'next_state': ConversationState.ADD_ASSIGNMENT.value,
                'response': "Hubo un error al agregar la materia. Inténtalo de nuevo o selecciona otra materia.",
                'data': session_data
            }
        
        # Estado de eliminar materia
        elif current_state == ConversationState.DELETE_ASSIGNMENT.value:
            delete_assignments = session_data.get('delete_assignments', [])
            print(delete_assignments)
            assignment_name = user_message.strip()
            
            # Confirmar y eliminar la materia
            if assignment_name not in delete_assignments:
                return {
                    'next_state': ConversationState.DELETE_ASSIGNMENT.value,
                    'response': "Por favor, selecciona una materia válida:",
                    'data': session_data
                }
            result = self.delete_assignment(assignment_name)
            if result:
                return {
                    'next_state': ConversationState.MENU.value,
                    'response': (
                        "Materia eliminada exitosamente.\n\n"
                        "¿Qué te gustaría hacer?\n"
                        "1. Consultar mis materias\n"
                        "2. Agregar materia\n"
                        "3. Eliminar materia\n"
                        "4. Todas las materias\n"
                        "5. Salir"
                    ),
                    'data': {}
                }
            return {
                'next_state': ConversationState.DELETE_ASSIGNMENT.value,
                'response': "Hubo un error al eliminar la materia. Inténtalo de nuevo o selecciona otra materia.",
                'data': session_data
            }
        
        return {
            'next_state': ConversationState.INITIAL.value,
            'response': "Lo siento, no entendí tu solicitud. Por favor, vuelve a intentarlo.",
            'data': {}
        }
