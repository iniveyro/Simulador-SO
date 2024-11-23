@echo off
setlocal

:: Configuración inicial
set "VENV_NAME=.venv"
set "REQUIREMENTS_FILE=requirements.txt"

echo Iniciando configuración del proyecto Python...

:: Crear el entorno virtual si no existe
if not exist "%VENV_NAME%" (
    echo Creando entorno virtual en "%VENV_NAME%"...
    python -m venv "%VENV_NAME%"
    if errorlevel 1 (
        echo Error al crear el entorno virtual. Verifica tu instalación de Python.
        pause
        exit /b 1
    )
    echo Entorno virtual creado.
) else (
    echo El entorno virtual ya existe en "%VENV_NAME%".
)

:: Verificar si el archivo requirements.txt existe
if not exist "%REQUIREMENTS_FILE%" (
    echo Creando archivo %REQUIREMENTS_FILE%...
    echo # Lista de librerías para el proyecto > "%REQUIREMENTS_FILE%"
) else (
    echo El archivo %REQUIREMENTS_FILE% ya existe.
)

:: Instalar dependencias si el archivo no está vacío
if exist "%REQUIREMENTS_FILE%" (
    for /f "tokens=*" %%a in ('type "%REQUIREMENTS_FILE%"') do (
        if not "%%a"=="" (
            echo Instalando dependencias desde %REQUIREMENTS_FILE%...
            pip install -r "%REQUIREMENTS_FILE%"
            goto :end
        )
    )
    echo El archivo %REQUIREMENTS_FILE% está vacío. No hay dependencias por instalar.
)

:end
:: Activar el entorno virtual
echo Activando el entorno virtual...
call "%VENV_NAME%\Scripts\activate.bat"

call cls
echo Ya estas dentro del entorno virtual con todas las dependencias necesarias
:: Mantener la ventana abierta
cmd /k