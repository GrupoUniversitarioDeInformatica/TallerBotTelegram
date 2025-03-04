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

mkdir -p src/json/ 
echo "" > src/json/events.json
echo "" > src/json/tasks.json
echo "TOKEN=" > .env

echo "Directorios y archivos creados."

URL="https://pytba.readthedocs.io/en/latest/quick_start.html"
xdg-open $URL
exit 0

