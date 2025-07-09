
# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Diet
import json

@ensure_csrf_cookie
def actualizar_dieta(request):
    if request.method == "POST":
        dieta_id = request.POST.get("dieta_id")
        dia_num = int(request.POST.get("dia"))
        desayuno = request.POST.get("desayuno")
        almuerzo = request.POST.get("almuerzo")
        merienda = request.POST.get("merienda")
        cena = request.POST.get("cena")

        try:
            dieta = Diet.objects.get(id=dieta_id)

            # Obtener el JSON actual de la dieta
            diet_data = dieta.diet if dieta.diet else {"dias": []}
            dias = diet_data.get("dias", [])

            # Ver si el día ya existe
            actualizado = False
            for day in dias:
                if day.get("dia") == dia_num:
                    day.update({
                        "desayuno": desayuno,
                        "almuerzo": almuerzo,
                        "merienda": merienda,
                        "cena": cena
                    })
                    actualizado = True
                    break

            # Si no existe ese día, lo agregamos
            if not actualizado:
                dias.append({
                    "dia": dia_num,
                    "desayuno": desayuno,
                    "almuerzo": almuerzo,
                    "merienda": merienda,
                    "cena": cena
                })

            # Actualizamos el JSON completo y el campo dayX
            diet_data["dias"] = dias
            setattr(dieta, "diet", diet_data)

            day_field = f"day{dia_num}"
            setattr(dieta, day_field, {
                "dia": dia_num,
                "desayuno": desayuno,
                "almuerzo": almuerzo,
                "merienda": merienda,
                "cena": cena
            })

            dieta.save()  # Esto automáticamente vuelve a calcular los dayX en el modelo
            return JsonResponse({"success": True})

        except Diet.DoesNotExist:
            return JsonResponse({"success": False, "error": "Dieta no encontrada"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método no permitido"})


"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Diet

@csrf_exempt  # Solo para pruebas, usa CSRF en producción
def actualizar_dieta(request):
    if request.method == "POST":
        dieta_id = request.POST.get("dieta_id")
        dia_num = int(request.POST.get("dia"))
        desayuno = request.POST.get("desayuno")
        almuerzo = request.POST.get("almuerzo")
        merienda = request.POST.get("merienda")
        cena = request.POST.get("cena")

        try:
            dieta = Diet.objects.get(id=dieta_id)

            # Modificar el día específico dentro del JSON
            if dieta.diet:
                diet_data = dieta.diet  # Obtener JSON actual
                if "dias" in diet_data:
                    for day in diet_data["dias"]:
                        if day["dia"] == dia_num:
                            day["desayuno"] = desayuno
                            day["almuerzo"] = almuerzo
                            day["merienda"] = merienda
                            day["cena"] = cena
                            break

                    dieta.diet = diet_data  # Guardar JSON actualizado
                    dieta.save()

                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({"success": False, "error": "Estructura incorrecta"})
            else:
                return JsonResponse({"success": False, "error": "No hay datos en la dieta"})

        except Diet.DoesNotExist:
            return JsonResponse({"success": False, "error": "Dieta no encontrada"})

    return JsonResponse({"success": False, "error": "Método no permitido"})


"""
