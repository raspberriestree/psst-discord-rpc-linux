#!/usr/bin/env python3
import time
import subprocess
from pypresence import Presence
import sys

# --- CONFIGURACIÓN ---
CLIENT_ID = 'YOUR_CLIENT_ID'
# ---------------------

def get_psst_player():
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
        print(f"Error while connecting to Discord IPC: {e}")
        sys.exit(1)

    while True:
        try:
            player = get_psst_player()
            if player:
                status = subprocess.run(['playerctl', '-p', player, 'status'], capture_output=True, text=True).stdout.strip()
                
                if status == "Playing":
                    title = get_metadata(player, 'title')
                    artist = get_metadata(player, 'artist')
                    
                    
                    art_url = get_metadata(player, 'mpris:artUrl')
                    
                    if title:
                    
                        if art_url and art_url.startswith("http"):
                            imagen = art_url
                        else:
                            imagen = "logo" 
                            
                        RPC.update(
                            details=title[:128],
                            state=f"- {artist}"[:128] if artist else "Unknown",
                            large_image=imagen
                        )
                else:
                    RPC.clear()
            else:
                RPC.clear()
        except Exception:
            pass 
            
        time.sleep(3)

if __name__ == '__main__':
    main()
