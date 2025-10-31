#!/bin/bash

# Script de inicio para el Frontend API

echo "🚀 Iniciando Frontend API..."

# Activar entorno virtual
source venv/bin/activate

# Verificar que las dependencias estén instaladas
if ! pip freeze | grep -q Flask; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus configuraciones."
fi

# Crear directorio de logs si no existe
if [ ! -d logs ]; then
    mkdir logs
fi

# Iniciar aplicación
echo "✅ Iniciando aplicación en http://localhost:5000"
python app.py
