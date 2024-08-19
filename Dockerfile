# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requisitos al contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación escuchará
EXPOSE 5000

# Define el comando para ejecutar la aplicación
CMD ["python", "pruebadeia.py"]
