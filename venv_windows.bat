@echo off

set VENV_NAME=.venv

echo Iniciando Entorno Virtual...

if not exist "%VENV_NAME%" (
    echo * Creando entorno virtual (%VENV_NAME%)...
    python -m venv %VENV_NAME%
    echo Entorno virtual creado.
) else (
    echo El entorno virtual (%VENV_NAME%) ya existe.
)

echo * Activando el entorno virtual...
call %VENV_NAME%\Scripts\activate

set REQUIREMENTS_FILE=requirements.txt
if not exist "%REQUIREMENTS_FILE%" (
    echo * Creando archivo %REQUIREMENTS_FILE%...
    :: echo # Lista de librerias para el proyecto > %REQUIREMENTS_FILE%
) else (
    echo %REQUIREMENTS_FILE% ya existe.
)

for /f %%i in ('findstr /r /c:".*" %REQUIREMENTS_FILE%') do (
    echo * Instalando dependencias desde %REQUIREMENTS_FILE%...
    pip install -r %REQUIREMENTS_FILE%
    goto :end_install
)
echo %REQUIREMENTS_FILE% está vacío. No hay dependencias por instalar.
:end_install

echo Listo para usar :D
