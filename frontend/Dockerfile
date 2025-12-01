# Frontend Dockerfile para Streamlit (producción / desarrollo)
# Ubicación esperada: ./frontend/Dockerfile

FROM python:3.11-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Establecer variables de entorno de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Crear usuario no-root
RUN useradd -m -d /home/appuser -s /bin/bash appuser && \
    chown -R appuser:appuser /app

# Copiar el resto de la aplicación (con los permisos correctos)
COPY --chown=appuser:appuser . .

# Cambiar al usuario no-root
USER appuser

# Variables de entorno de Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=watchdog

# Exponer el puerto
EXPOSE 8501

# Hacer ejecutable el script de inicio
RUN chmod +x /app/run.sh

# Comando de inicio
CMD ["/app/run.sh"]
