

import pytesseract
import spacy
import fitz  # PyMuPDF para PDFs
from PIL import Image
import os
from django.core.files.storage import default_storage
from .models import Estudio, Resultado

# Cargar modelo de spaCy (usaremos "es_core_news_sm" para español)
nlp = spacy.load("es_core_news_sm")

def extraer_texto(archivo_path):
    """Extrae texto de imágenes o PDFs."""
    texto_extraido = ""

    if archivo_path.lower().endswith('.pdf'):
        doc = fitz.open(archivo_path)
        for page in doc:
            texto_extraido += page.get_text("text")
    else:
        imagen = Image.open(archivo_path)
        texto_extraido = pytesseract.image_to_string(imagen, lang="spa")  # OCR en español
    
    return texto_extraido

def analizar_texto_con_spacy(texto):
    """Usa spaCy para encontrar estudios y valores en el texto extraído."""
    doc = nlp(texto)
    resultados = {}

    for token in doc:
        if token.like_num:  # Si es un número, asumimos que es un valor de estudio
            palabra_anterior = token.nbor(-1).text if token.i > 0 else None
            if palabra_anterior:
                resultados[palabra_anterior] = token.text

    return resultados

def procesar_archivo(analitica):
    """Procesa una analítica, extrae los valores y los guarda en la base de datos."""
    archivo_path = analitica.archivo.path

    # 1️⃣ Extraer texto del archivo
    texto = extraer_texto(archivo_path)

    # 2️⃣ Usar spaCy para encontrar los estudios y valores
    resultados = analizar_texto_con_spacy(texto)

    # 3️⃣ Guardar los resultados en la base de datos
    for nombre_estudio, valor in resultados.items():
        estudio, _ = Estudio.objects.get_or_create(nombre=nombre_estudio)
        Resultado.objects.create(analitica=analitica, estudio=estudio, valor=valor)

    # 4️⃣ Eliminar el archivo después de procesarlo
    default_storage.delete(archivo_path)
