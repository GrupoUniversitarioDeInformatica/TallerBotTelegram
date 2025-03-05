@echo off

python --version 2>nul
if %errorlevel% neq 0 (
    echo Python 3 no está instalado.
    set /p choice="Quieres instalar Python 3? (y/n): "
    
    if /i "%choice%"=="y" (
        echo Porfavor, para la realización del taller instala Python 3 desde la web oficial: https://www.python.org/
        exit /b 1
    ) else (
        echo Python 3 no instalado. Saliendo...
        exit /b 1
    )
) else (
    echo Python 3 está instalado.
)


@echo off
if not exist ".venv" (
    echo Creando entorno virtual
    python -m venv .venv
    call .\.venv\Scripts\activate
    pip install -r requirements.txt
    echo Entorno virtual creado y activado. Se puede desactivar en cualquier momento ejecutando 'deactivate'
)

:: Create directories
mkdir src/json/
echo "" > src/json/events.json
echo "" > src/jsos/tasks.json
echo "TOKEN=""" > .env

echo Directorios y archivos creados.
set URL=https://pytba.readthedocs.io/en/latest/index.html
set URL2=https://pytba.readthedocs.io/en/latest/quick_start.html
start %URL%
start %URL2%
exit /b 0

