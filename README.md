# Psst Discord Rich Presence (Linux)

A lightweight Python and Bash bridge to connect the [Psst](https://github.com/jpochyla/psst) native Spotify client with Discord Rich Presence on Linux. 

This project specifically solves the Inter-Process Communication (IPC) routing issues that occur when Discord is installed via Flatpak (sandbox isolation) and standard tools fail to detect the dynamic MPRIS instances of Psst.

## Features
* **Zero Bloat:** Reads metadata directly from the system bus via `playerctl`.
* **Dynamic Album Art:** Fetches and displays public URLs for album covers dynamically.
* **Flatpak Native:** Automatically links the isolated Flatpak `discord-ipc-0` socket to the standard user runtime directory.
* **Smart Process Management:** Automatically starts with Psst and kills the background bridge when the music player is closed.

## Prerequisites
* **OS:** Linux (Debian/Ubuntu-based distributions recommended)
* **Discord:** Installed via Flatpak
* **Psst:** Native installation
* **Dependencies:** `playerctl`, `python3-venv`

## Installation

1. **Install system dependencies:**
   sudo apt install playerctl python3-venv

2. **Clone this Repository**
   git clone [https://github.com/raspberriestree/psst-discord-rpc-linux.git](https://github.com/raspberriestree/psst-discord-rpc-linux.git)
   cd psst-discord-rpc-linux

3. **Set up the Python Virtual Environment:**
  python3 -m venv venv
  source venv/bin/activate
  pip install pypresence

4. **Get your Discord Client ID:**
    -Go to the Discord Developer Portal.
    -Create a new application (e.g., "Psst" or "Spotify").
    -Copy the Application ID (Client ID).

5. **Configure the script:**
    Open discord-bridge.py and replace the placeholder with your Client ID:

## Usage
You can use the provided iniciar-psst.sh wrapper script to launch both the player and the RPC bridge simultaneously. Ensure the paths inside the script match your local setup.

Make the script executable:
  chmod +x iniciar-psst.sh

Run the launcher:
  ./iniciar-psst.sh

## How It Works (The Flatpak IPC Fix)
Flatpak sandboxes Discord, preventing standard MPRIS trackers from locating the IPC socket. This wrapper mitigates the issue by forcefully symlinking the Flatpak socket to the standard $XDG_RUNTIME_DIR:
ln -sf /run/user/1000/app/com.discordapp.Discord/discord-ipc-0 /run/user/1000/discord-ipc-0
