# Usa una imagen base de Python
FROM python:3.10-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev

# Configura la zona horaria
ENV TZ=America/Santo_Domingo

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Instala las dependencias globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script de arranque
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expone el puerto 8000
EXPOSE 8000

# Configura el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

