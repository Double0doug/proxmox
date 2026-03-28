# STEP 1: Create the directory on your 1TB disk
mkdir -p /mnt/data/minecraft
cd /mnt/data/minecraft

# STEP 2: Create the docker-compose.yml file
# Copy this entire block and paste it into your PowerShell
cat <<EOF > docker-compose.yml
services:
  mc:
    image: itzg/minecraft-server
    container_name: minecraft-server
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      MEMORY: "8G"
      VERSION: "LATEST"
    volumes:
      - /mnt/data/minecraft:/data
    restart: unless-stopped
EOF

# STEP 3: Start the server
docker compose up -d

# STEP 4: Watch the server logs (Press Ctrl+C to stop watching)
docker logs -f minecraft-server
