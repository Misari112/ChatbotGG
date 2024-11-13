from enum import Enum

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