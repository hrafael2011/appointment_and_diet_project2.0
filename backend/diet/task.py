from celery import shared_task
from .models import Patient, Diet
from .services.openai_diet import generar_dieta_con_openai

@shared_task
def create_patient_diet(patient_id, diet_note=None):
    try:
        patient = Patient.objects.get(id=patient_id)

        data_paciente = {
            "DOB": patient.DOB,
            "weight": patient.weight,
            "height": patient.height,
            "objetive": patient.objetive,
            "sex": patient.sex,
            "country": patient.country,
            "city": patient.city,
            "food_allergies": patient.food_allergies,
            "diseases": patient.diseases,
            "neck_size": patient.neck_size,
            "chest_size": patient.chest_size,
            "waist_size": patient.waist_size,
            "hip_size": patient.hip_size,
            "leg_size": patient.leg_size,
            "calf_size": patient.calf_size,
        }

        data_diet = {
            "diet_note": diet_note
        }

        resultado = generar_dieta_con_openai(data_paciente, data_diet)

        print(f"Esta es la dieta generada: {resultado}")

        if "error" not in resultado:
            Diet.objects.create(
                patient=patient,
                diet=resultado,
                diet_note=diet_note
            )
            return resultado
        else:
            return resultado["error"]

    except Patient.DoesNotExist:
        return "El paciente no existe."
    except ValueError as ve:
        return f"Error de validación: {str(ve)}"
    except Exception as e:
        return f"Error en la tarea Celery: {str(e)}"
