from crewai import Task
from .agents import Agente_Evaluacion_Calidad,Agente_Originalidad,Agente_Claridad

def crear_tareas(texto_documento,contexto_usuario):
    tarea_evaluacion_calidad = Task(
        description=f"""Evaluar la calidad general del siguiente trabajo de investigación, teniendo en cuenta la metodología y la relevancia del contenido:
        Documento:
        {texto_documento}

        Contexto del usuario:
        {contexto_usuario}
        """,
        agent=Agente_Evaluacion_Calidad,
        expected_output="Un informe detallado en español sobre la calidad general del trabajo de investigación."
    )
    tarea_evaluacion_originalidad = Task(
        description=f"""Analizar la originalidad y contribución del trabajo de investigación al campo de estudio:
        Documento:
        {texto_documento}

        Contexto del usuario:
        {contexto_usuario}
        """,
        agent=Agente_Originalidad,
        expected_output="Un análisis en español sobre la originalidad y el aporte del trabajo al campo de estudio."
    )

    tarea_evaluacion_claridad = Task(
        description=f"""Evaluar la claridad y coherencia de la escritura, incluyendo estructura, gramática y estilo:

        Documento:
        {texto_documento}

        Contexto del usuario:
        {contexto_usuario}
        """,
        agent=Agente_Claridad,
        expected_output="Un informe en español sobre la claridad y coherencia de la escritura del documento."
    )

    return [tarea_evaluacion_calidad, tarea_evaluacion_originalidad, tarea_evaluacion_claridad]
