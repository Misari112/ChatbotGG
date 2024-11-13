# agents/tools.py

import PyPDF2

def leer_pdf(ruta_pdf):
    texto_completo = ''
    with open(ruta_pdf, 'rb') as archivo_pdf:
        lector_pdf = PyPDF2.PdfReader(archivo_pdf)
        for pagina in lector_pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina
    return texto_completo
