import pdfkit
from flask import make_response
import os

# Ruta al ejecutable wkhtmltopdf en Windows
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def generar_pdf(html_content, filename="reporte.pdf"):
    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None  # necesario para imágenes locales
    }

    pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response
