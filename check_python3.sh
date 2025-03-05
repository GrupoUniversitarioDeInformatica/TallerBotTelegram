#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado."
    read -p "Quieres instalar Python 3? (y/n): " choice

    if [[ "$choice" == "y" ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update && sudo apt install python3 -y
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python3
        else
            echo "Instala python 3 manualmente."
            exit 1
        fi
    else
        echo "Python 3 no está instalado. Saliendo..."
        exit 1
    fi
else
    echo "Python 3 ya instalado."
fi

if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual"
    python3 -m venv .venv
    source ./.venv/bin/activate
    pip install -r requierements.txt
    echo "Entorno virtual creado y activado. Se puede desactivar en cualquier momento ejecutando 'deactivate'"
fi

mkdir -p src/json/ 
echo "" > src/json/events.json
echo "" > src/json/tasks.json
echo "TOKEN=" > .env

echo "Directorios y archivos creados."

URL="https://pytba.readthedocs.io/en/latest/index.html"
URL2="https://pytba.readthedocs.io/en/latest/quick_start.html"
xdg-open $URL && xdg-open $URL2
exit 0

