# Imagen base
FROM python:3.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo pyproject.toml (y opcionalmente poetry.lock) para las dependencias
COPY pyproject.toml poetry.lock* /app/

# Instala Poetry
RUN pip install poetry

# Configura Poetry para no crear un entorno virtual y luego instala las dependencias
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copia el resto del código fuente de la aplicación al directorio de trabajo
COPY . /app

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8899"]
