
# Usa una imagen base de Python más completa
FROM python:3.10

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev


RUN pip install --no-cache-dir xhtml2pdf==0.2.8 reportlab==3.6.12

 

# Configura la zona horaria (si es necesario)
ENV TZ=America/Santo_Domingo

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Copia el script 'wait-for-it.sh' y da permisos de ejecución
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Actualiza pip y limpia el cache
RUN pip install --upgrade pip && pip cache purge

# Instala las dependencias de Python desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo 'entrypoint.sh' y le da permisos de ejecución
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expone el puerto 8000
EXPOSE 8000

# Establece el script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

