# Pulse Monitoring (External Monitor)

This directory contains the deployment instructions for **Pulse**, a simple external status monitor.

## Deployment (Raspberry Pi 5)
1.  **Portainer:** Access your Pi's Portainer instance.
2.  **Stack:** Create a new Stack named `pulse`.
3.  **Config:** Paste the `docker-compose.yml` from this directory.
4.  **Targets:** Add the following targets to your Pulse configuration:
    -   **Proxmox Host:** `192.168.1.50`
    -   **Docker Host VM:** `192.168.1.40`
    -   **Minecraft:** `192.168.1.40:25565` (via TCP check)
    -   **Portainer Agent:** `192.168.1.40:9001` (via TCP check)

## Benefit
Running Pulse on the Pi ensures that if Proxmox goes down, you still have a live monitor to tell you what happened.
