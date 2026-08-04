#!/usr/bin/env python3
import time
import subprocess
from pypresence import Presence
import sys

# --- CONFIGURACIÓN ---
CLIENT_ID = 'YourID' #You can get it in Discord Developers Portals when creating a new app
# ---------------------

def get_psst_player():
    # Busca el nombre dinámico de psst en playerctl
    try:
        result = subprocess.run(['playerctl', '-l'], capture_output=True, text=True)
        for p in result.stdout.splitlines():
            if "psst" in p:
                return p
    except:
        pass
    return None

def get_metadata(player, field):
    try:
        res = subprocess.run(['playerctl', '-p', player, 'metadata', field], capture_output=True, text=True)
        return res.stdout.strip()
    except:
        return ""

def main():
    try:
        RPC = Presence(CLIENT_ID)
        RPC.connect()
    except Exception as e:
        print(f"Error conectando a Discord IPC: {e}")
        sys.exit(1)

    while True:
        try:
            player = get_psst_player()
            if player:
                status = subprocess.run(['playerctl', '-p', player, 'status'], capture_output=True, text=True).stdout.strip()
                
                if status == "Playing":
                    title = get_metadata(player, 'title')
                    artist = get_metadata(player, 'artist')
                    
                    if title:
                        # Formateamos para que se vea bien en Discord
                        RPC.update(
                            details=title[:128],
                            state=f"de {artist}"[:128] if artist else "Artista desconocido",
                            large_image="logo" # Cambia esto si no subiste ninguna imagen
                        )
                else:
                    RPC.clear()
            else:
                RPC.clear()
        except Exception:
            pass # Ignoramos errores temporales de lectura
            
        time.sleep(3) # Revisa qué canción suena cada 3 segundos

if __name__ == '__main__':
    main()
