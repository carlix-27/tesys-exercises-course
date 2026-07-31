#!/usr/bin/env bash
# Runs Dungeon of Shadows, creating the virtual environment on first launch.
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual e instalando dependencias..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip -q
    ./venv/bin/pip install -r requirements.txt -q
fi

exec ./venv/bin/python main.py
