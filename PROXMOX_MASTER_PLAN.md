# Proxmox Environment: Big-Lab-01 (System Specification & Context)

This document serves as the authoritative source of truth for the **Big-Lab-01** environment. It provides a snapshot of the current state, technical constraints, and strategic roadmap for future agents to research, plan, and implement improvements.

**Last Verified State:** March 28, 2026

---

## 1. Host Infrastructure (Physical)

### 1.1 Hardware Specifications
- **Hostname:** `pve` (IP: `192.168.1.50`)
- **CPU:** AMD Ryzen 7 5700G (8C/16T).
- **RAM:** 64GB DDR4.
- **Primary Storage (OS/Fast):** 1.8TB NVMe (`local-lvm`).
- **Secondary Storage (Bulk):** 4TB HDD (`mass-storage`, EXT4, mounted at `/mnt/pve/mass-storage`).

### 1.2 Host-Level Optimizations
- **Kernel Fixes:** `amd64-microcode` (0x0a500014) applied for Ryzen stability.
- **CPU Tuning:** Governor set to `performance` via `post_install.sh`.
- **ZFS Tuning:** ARC limited to 16GB (ref: `/etc/modprobe.d/zfs.conf`).
- **APT Repos:** `pve-no-subscription` active; enterprise repo disabled.
- **UI:** Subscription nag suppressed via `proxmoxlib.js` modification.

---

## 2. Virtualized Environment (L1)

### 2.1 VM 101: `docker-host`
- **Purpose:** Primary application and container orchestration node.
- **OS:** Ubuntu Server 24.04.1 LTS.
- **Resources:** 8 vCPUs (Host-type), 16GB RAM.
- **Storage Layout:**
  - `scsi0`: 128GB (NVMe-backed) - OS & Docker Engine.
  - `scsi1`: 1TB (HDD-backed) - Data & Persistent Volumes.
- **Current Status:** OS installed and SSH active. Docker installation and data disk mounting (`/dev/sdb` to `/mnt/data`) are the immediate pending tasks.

---

## 3. Strategic Roadmap & Desired State

Future agents should use the following goals to guide research and implementation:

### 3.1 Containerized Workloads
- **Minecraft Server:** Deploy `itzg/minecraft-server` via Docker Compose on VM 101.
  - *Context:* Configuration located in `minecraft-server/`. Data must persist on the 1TB HDD mount point (`/mnt/data/minecraft`).
- **IOT Build Server:** Deploy an ESP32/ESP-IDF build environment to support sensor node development.

### 3.2 Network Services & Storage Integration
- **NFS Server:** Configure the Proxmox host to export `/mnt/pve/mass-storage` via NFS.
- **Satellite Integration:** Integrate Raspberry Pi nodes (e.g., `home-assistant-pi`) by mounting the host's NFS shares.
- **Centralized Management:** Connect VM 101 to the Raspberry Pi 5 Portainer instance via the **Portainer Agent** (Port 9001).
- **Proxmox MCP Server (SSE):** Deploy a Dockerized Model Context Protocol server on VM 101 to expose real-time host/VM telemetry to future agents.
  - *Context:* Implementation files located in `docker-mcp-setup/`.

### 3.3 Infrastructure Maturity (Future Research)
- **Pulse Monitoring:** Deploy `rcourtman/pulse` on Raspberry Pi 5 to monitor Proxmox host and VM 101 from an external node.
  - *Context:* Configuration located in `pulse-monitoring/`.
- **Monitoring (Advanced):** Implement Prometheus/Grafana (LXC or Docker) for host and VM telemetry.
- **Automation:** Transition from manual `qm` commands to IaC (Terraform/OpenTofu and Ansible) for environment reproducibility.

---

## 4. Context for Future Agents

### Key Files & Locations
- `lab_inventory.json`: Machine-readable metadata for IPs and satellite nodes.
- `post_install.sh`: Historical record of host-level optimizations.
- `vm_provisioning_history.sh`: `qm` command history for VM creation.
- `minecraft-server/`: Docker Compose and deployment guide for the Minecraft workload.

### Operating Principles
1. **Stability First:** All host changes must respect the Ryzen 5700G's specific microcode and governor requirements.
2. **Storage Tiering:** Always distinguish between NVMe (performance/OS) and HDD (bulk/backup) when allocating resources.
3. **Documentation:** Update this document whenever the "Current Status" of a node changes.
