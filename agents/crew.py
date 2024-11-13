from crewai import Crew
from .agents import Agente_Evaluacion_Calidad,Agente_Claridad,Agente_Originalidad
from .task import crear_tareas

def ejecutar_crew(texto_documento,contexto_usuario):
    tareas = crear_tareas(texto_documento,contexto_usuario)
    agentes = [Agente_Evaluacion_Calidad,Agente_Claridad,Agente_Originalidad]
    crew = Crew(agents = agentes, tasks=tareas, verbose=False)
    crew.kickoff()
    return crew 