#!/bin/bash

# 1. Fuerza el puente IPC de Flatpak para Discord
ln -sf /run/user/1000/app/com.discordapp.Discord/discord-ipc-0 /run/user/1000/discord-ipc-0

# 2. Inicia nuestro puente Python usando el entorno virtual en segundo plano
~/.local/share/psst-env/bin/python ~/.local/bin/discord-bridge.py &
PID_PUENTE=$!

# 3. Inicia Psst y espera a que lo cierres
/usr/bin/psst -gui

# 4. Cuando cierras Psst, destruye el proceso del puente de Python
kill $PID_PUENTE
