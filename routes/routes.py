# routes/routes.py

from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crew import ejecutar_crew
from agents.tools import leer_pdf
from controllers.user_controller import get_user_information
from controllers.response_handler import login_flow

from config import ConversationState
from controllers.subjects_controller import AssignmentChatHandler

routes = Blueprint('routes', __name__)
chat_handler = AssignmentChatHandler()

def render_chat(template_name):
    if 'user' not in session:
        return render_template('login.html')
    else:
        user_info = get_user_information()
        return render_template(template_name, user=user_info)

@routes.route('/')
def index():
    return render_chat('index.html')

@routes.route('/ChatGina')
def chat_gina():
    return render_chat('ChatGina.html')

@routes.route('/ChatGladys')
def chat_gladys():
    session['conversation_state'] = ConversationState.INITIAL.value
    return render_chat('ChatGladys.html')

@routes.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@routes.route('/evaluate', methods=['POST'])
def evaluate():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No se encontró el archivo PDF.'}), 400

    file = request.files['pdfFile']
    context = request.form.get('context', '')

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo PDF.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploads_dir = 'uploads'
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        file_path = os.path.join(uploads_dir, filename)

        file.save(file_path)

        try:
            texto_documento = leer_pdf(file_path)

            crew = ejecutar_crew(texto_documento, context)

            combined_message = ''
            for task in crew.tasks:
                agent_name = task.agent.role

                task_output = getattr(task, 'output', None)
                if task_output is None:
                    print(f"No se encontró el resultado para la tarea con agente {agent_name}")
                    continue

                # Convertir todo el task_output a cadena de texto
                agent_output_text = str(task_output)
                if not agent_output_text:
                    print(f"No se encontró el texto de salida para la tarea con agente {agent_name}")
                    continue

                # Concatenar el nombre del agente y su contenido
                combined_message += f"<strong>{agent_name}:</strong><br>{agent_output_text.strip()}<br><br>"

            os.remove(file_path)

            return jsonify({'message': combined_message})

        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Ocurrió un error al procesar el archivo PDF.'}), 500
    else:
        return jsonify({'error': 'Archivo no permitido. Solo se aceptan PDFs.'}), 400

@routes.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    response = login_flow(email, password)
    return response

@routes.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    current_state = session.get('conversation_state', ConversationState.INITIAL.value)
    session_data = session.get('data', {})
    
    result = chat_handler.handle_chat(current_state, user_message, session_data)
    
    session['conversation_state'] = result['next_state']
    session['data'] = result['data']
    
    return jsonify({
        "response": result['response'],
        "state": result['next_state']
    })