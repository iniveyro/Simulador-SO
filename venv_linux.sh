#!/bin/bash

VENV_NAME=".venv"

echo "Iniciando Entorno Virtual..."

if [ ! -d "$VENV_NAME" ]; then
    echo " - Creando entorno virtual ($VENV_NAME)..."
    python3 -m venv $VENV_NAME
    echo "Entorno virtual creado."
else
    echo "El entorno virtual ($VENV_NAME) ya existe."
fi

echo " - Activando el entorno virtual..."
source $VENV_NAME/bin/activate

REQUIREMENTS_FILE="requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo " - Creando archivo $REQUIREMENTS_FILE..."
    touch $REQUIREMENTS_FILE
    #echo " - # Listado de librerías para el proyecto" > $REQUIREMENTS_FILE
else
    echo "$REQUIREMENTS_FILE ya existe."
fi

if [ -s "$REQUIREMENTS_FILE" ]; then
    echo " - Instalando dependencias desde $REQUIREMENTS_FILE..."
    pip install -r $REQUIREMENTS_FILE
else
    echo "$REQUIREMENTS_FILE está vacío. No hay dependencias por instalar."
fi

echo "Listo para usar :D"
