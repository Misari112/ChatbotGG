from crewai import Agent
from langchain_groq import ChatGroq
import os

model_8b = 'groq/llama3-8b-8192'
model_70b = 'groq/llama3-70b-8192'

groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("La variable de entorno 'GROQ_API_KEY' no está definida.")

llm_8b = ChatGroq (
    temperature=0,
    groq_api_key=groq_api_key,
    model=model_8b
)

llm_70b = ChatGroq (
    temperature=0,
    groq_api_key=groq_api_key,
    model=model_70b
)

Agente_Evaluacion_Calidad = Agent(
    role='Agente_Evaluacion_Calidad',
    goal="""Evaluar la calidad general del trabajo de investigación, incluyendo la solidez metodológica y la relevancia del contenido.""",
    backstory="""Eres un experto en evaluación de trabajos de investigación, con amplio conocimiento en metodologías científicas y estándares académicos.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_70b,
)
Agente_Originalidad = Agent(
    role='Agente_Originalidad',
    goal="""Analizar la originalidad y contribución al campo del trabajo de investigación presentado.""",
    backstory="""Como especialista en revisión académica, te centras en identificar la innovación y el aporte que ofrece el trabajo al área de estudio.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_8b,
)

Agente_Claridad = Agent(
    role='Agente_Claridad',
    goal="""Evaluar la claridad y coherencia de la escritura, incluyendo la estructura, gramática y estilo del documento.""",
    backstory="""Eres un experto en redacción académica y te encargas de asegurar que el documento esté bien escrito y sea fácil de entender.""",
    verbose=True,
    allow_delegation=False,
    llm=llm_8b,
)