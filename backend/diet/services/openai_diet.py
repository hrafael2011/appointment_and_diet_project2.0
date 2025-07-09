import json
import re
from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from django.conf import settings


def validar_datos_paciente(data_paciente):
    campos_requeridos = [
        'DOB', 'weight', 'height', 'objetive',
        'sex', 'country', 'city', 'food_allergies', 'diseases'
    ]
    for campo in campos_requeridos:
        if not data_paciente.get(campo):
            raise ValueError(f"Falta el campo obligatorio: {campo}")


def extraer_json_desde_respuesta(texto):
    """
    Extrae el primer bloque JSON válido desde un texto, usando regex.
    """
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise json.JSONDecodeError("No se pudo extraer un JSON válido desde la respuesta del modelo.", texto, 0)


def generar_dieta_con_openai(data_paciente, data_diet):
    try:
        validar_datos_paciente(data_paciente)
    except ValueError as ve:
        return {"error": str(ve)}

    if not hasattr(settings, 'API_KEY_OPENAI') or not settings.API_KEY_OPENAI:
        return {"error": "No se encontró la API Key de OpenAI en la configuración."}

    client = OpenAI(api_key=settings.API_KEY_OPENAI)

    json_structure = """
    {
    "informacion_nutricional": {
        "calorias_diarias": número,
        "distribucion_macros": {
        "proteinas_porcentaje": número,
        "carbohidratos_porcentaje": número,
        "grasas_porcentaje": número
        },
        "recomendaciones_generales": "texto con consejos específicos para este paciente"
    },
    "dias": [
        {
        "dia": 1,
        "calorias_totales": número,
        "desayuno": "Descripción completa con cantidades exactas",
        "almuerzo": "Descripción completa con cantidades exactas",
        "merienda": "Descripción completa con cantidades exactas",
        "cena": "Descripción completa con cantidades exactas"
        },
        ...continuación para los 7 días...
    ]
    }
    """

    prompt = f"""Eres un nutricionista profesional certificado con especialización en nutrición clínica y planificación de dietas personalizadas. Tu misión es crear una dieta semanal completamente personalizada en formato JSON válido basada en los datos específicos del paciente.

## INSTRUCCIONES DETALLADAS

1. ANALIZA CUIDADOSAMENTE los datos del paciente para calcular:
   - Edad exacta (a partir de la fecha de nacimiento)
   - IMC (Índice de Masa Corporal)
   - Metabolismo Basal (TMB) usando la fórmula apropiada según sexo
   - Requerimiento calórico diario ajustado al objetivo

2. CONSIDERA FACTORES CULTURALES Y REGIONALES:
   - Adapta la dieta a alimentos típicos y disponibles en {data_paciente['country']} y {data_paciente['city']}
   - Respeta horarios de comida culturalmente apropiados

3. PERSONALIZA SEGÚN CONDICIONES MÉDICAS:
   - Ajusta la dieta para manejar las siguientes condiciones: {data_paciente['diseases']}
   - Excluye completamente los alimentos listados en: {data_paciente['food_allergies']}

4. OPTIMIZA PARA EL OBJETIVO ESPECÍFICO: {data_paciente['objetive']}
   - Ajusta macronutrientes según el objetivo (pérdida de peso, ganancia muscular, etc.)
   - Varía las calorías diarias según corresponda (déficit/superávit)

5. AJUSTA POR COMPOSICIÓN CORPORAL usando las medidas proporcionadas:
   - Cuello: {data_paciente["neck_size"]}
   - Pecho: {data_paciente["chest_size"]}
   - Cintura: {data_paciente["waist_size"]}
   - Cadera: {data_paciente["hip_size"]}
   - Pierna: {data_paciente["leg_size"]}
   - Pantorrilla: {data_paciente["calf_size"]}

6. SIGUE INSTRUCCIONES ESPECÍFICAS DEL PACIENTE:
   - {data_diet["diet_note"]}

7. Trata de que las comidas sean variadas y no repetitivas, ofreciendo diferentes opciones cada día para asegurar una alimentación equilibrada y diversa.

## ESPECIFICACIONES TÉCNICAS DEL FORMATO JSON

- La respuesta DEBE ser un JSON válido compatible con JSONField de Django
- El JSON NO debe contener texto introductorio ni explicaciones adicionales
- Cada comida debe describirse en UNA SOLA CADENA DE TEXTO (no usar arrays ni objetos anidados)
- Incluye cantidades precisas en gramos o medidas caseras (tazas, cucharadas, etc.)
- Especifica métodos de cocción y preparación

## ESTRUCTURA DEL JSON:
{json_structure}

## DATOS DEL PACIENTE:

- Fecha de nacimiento: {data_paciente['DOB']}
- Peso: {data_paciente['weight']} kg
- Altura: {data_paciente['height']} cm
- Objetivo: {data_paciente['objetive']}
- Sexo: {data_paciente['sex']}
- País: {data_paciente['country']}
- Ciudad: {data_paciente['city']}
- Restricciones alimentarias: {data_paciente['food_allergies']}
- Condiciones médicas: {data_paciente['diseases']}
- Nota dietética adicional: {data_diet["diet_note"]}

IMPORTANTE:
1. NO INCLUYAS EXPLICACIONES fuera del JSON
2. INCLUYE CANTIDADES PRECISAS para cada alimento
3. ESPECIFICA MÉTODOS DE PREPARACIÓN
4. ASEGÚRATE de que cada comida tenga un valor nutritivo adecuado según el objetivo
5. PROPORCIONA OPCIONES VARIADAS para evitar monotonía dietética
6. RESPETA COMPLETAMENTE las restricciones alimentarias
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return extraer_json_desde_respuesta(content)

    except APIError as api_error:
        return {"error": f"Error de la API de OpenAI: {str(api_error)}"}
    except RateLimitError as rate_limit_error:
        return {"error": f"Se excedió el límite de solicitudes: {str(rate_limit_error)}"}
    except AuthenticationError as auth_error:
        return {"error": f"Error de autenticación con OpenAI: {str(auth_error)}"}
    except Exception as e:
        return {"error": f"Error general inesperado: {str(e)}"}
