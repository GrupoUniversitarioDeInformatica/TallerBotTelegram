#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    read -p "Do you want to install Python 3? (y/n): " choice

    if [[ "$choice" == "y" ]]; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update && sudo apt install python3 -y
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install python3
        else
            echo "Please install Python 3 manually."
            exit 1
        fi
    else
        echo "Python 3 is not installed. Exiting..."
        exit 1
    fi
else
    echo "Python 3 is installed."
fi

mkdir -p src/json/ 

echo "Directories created successfully."

URL="https://pytba.readthedocs.io/en/latest/quick_start.html"
xdg-open $URL
exit 0

