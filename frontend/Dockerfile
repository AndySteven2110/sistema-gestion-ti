# Frontend Dockerfile para Streamlit (producción / desarrollo)
# Ubicación esperada: ./frontend/Dockerfile

FROM python:3.11-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para compilar paquetes (pyarrow, pandas, cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python primero (cache layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copiar el resto de la aplicación
COPY . /app

# Crear un usuario no-root para ejecutar Streamlit (mejor práctica)
RUN useradd --create-home --shell /bin/bash appuser \
 && chown -R appuser:appuser /app

USER appuser

# Exponer el puerto de Streamlit
EXPOSE 8501

# Variables de entorno por defecto (puedes sobreescribir desde docker-compose/.env)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
# Usar watchdog como file watcher dentro del contenedor (recomendado si está en requirements)
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=watchdog

# Comando por defecto: ejecutar la app principal
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.fileWatcherType", "watchdog"]
