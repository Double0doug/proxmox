# Minecraft Server (Paper)

This directory contains the Docker Compose configuration for the `itzg/minecraft-server` workload on VM 101 (`docker-host`).

## Prerequisites
- VM 101 must have Docker installed.
- The 1TB bulk storage disk must be mounted at `/mnt/data`.

## Deployment
1. Copy this directory to VM 101:
   ```bash
   scp -r minecraft-server/ <user>@192.168.1.101:~/
   ```
2. Create the data directory:
   ```bash
   sudo mkdir -p /mnt/data/minecraft
   sudo chown -R $USER:$USER /mnt/data/minecraft
   ```
3. Start the server:
   ```bash
   cd ~/minecraft-server
   docker compose up -d
   ```

## Management
- **Logs:** `docker logs -f minecraft-server`
- **Stop:** `docker compose down`
