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

:: Create directories
mkdir src/json/
echo "" > src/json/events.json
echo "" > src/jsos/tasks.json
echo "TOKEN=""" > .env

echo Directorios y archivos creados.
SET URL=https://pytba.readthedocs.io/en/latest/quick_start.html
start %URL%
exit /b 0

