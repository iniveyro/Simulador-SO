#!/bin/bash

# Configuración inicial
VENV_DIR=".venv"
REQ_FILE="requirements.txt"

echo "Iniciando configuración del entorno virtual..."

# Crear el entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual en $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: No se pudo crear el entorno virtual."
        exit 1
    fi
    echo "Entorno virtual creado."
else
    echo "El entorno virtual ya existe."
fi

# Crear el archivo requirements.txt si no existe
if [ ! -f "$REQ_FILE" ]; then
    echo "Creando archivo $REQ_FILE..."
    echo "# Lista de dependencias del proyecto" > "$REQ_FILE"
else
    echo "El archivo $REQ_FILE ya existe."
fi

# Instalar dependencias desde requirements.txt
if [ -s "$REQ_FILE" ]; then
    echo "Instalando dependencias desde $REQ_FILE..."
    "$VENV_DIR/bin/pip" install -r "$REQ_FILE"
else
    echo "El archivo $REQ_FILE está vacío. No hay dependencias para instalar."
fi

# Activar el entorno virtual en la sesión actual
echo "Activando el entorno virtual..."
source ".venv/bin/activate"

# Mantener el entorno activado para el usuario
echo "El entorno virtual está activo. ¡Listo para trabajar!"
#exec "$SHELL"

