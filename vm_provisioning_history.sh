# 1. Create the VM (ID 101) with 8 CPU Cores (Ryzen 5700G) and 16GB RAM
# This VM will use your NVMe (local-lvm) for its main system drive (128GB).
qm create 101 --name docker-host --ostype l26 --cpu host --cores 8 --memory 16384 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-single

# 2. Add the Ubuntu ISO as a virtual DVD drive
qm set 101 --cdrom local:iso/ubuntu-24.04.1-live-server-amd64.iso

# 3. Create the OS Disk (128GB) on your FAST local-lvm storage
# This is where Docker and your Minecraft server will live.
qm set 101 --scsi0 local-lvm:128,discard=on,ssd=1

# 4. Create a SECOND Disk (1TB) on your MASS-STORAGE (4TB Spinner)
# This is for large files, backups, and data that doesn't need NVMe speed.
qm set 101 --scsi1 mass-storage:1024

# 5. Set the Boot Order (CDROM first, then Disk)
qm set 101 --boot c --bootdisk scsi0
