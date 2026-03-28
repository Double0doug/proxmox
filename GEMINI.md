# Gemini CLI Instructions: Big-Lab-01 Proxmox

This file contains foundational mandates for all Gemini CLI agents interacting with this repository. These instructions take precedence over general workflows.

## 1. Source of Truth
- **Inventory:** Use `lab_inventory.json` as the absolute source of truth for IP addresses, VM IDs, and hardware mapping.
- **Plan:** Update `PROXMOX_MASTER_PLAN.md` immediately after any significant architectural or state change (e.g., new VM deployment, disk expansion).

## 2. Infrastructure Standards
- **Storage Tiering:** 
  - **NVMe (`local-lvm`):** Reserved for OS boot disks and performance-critical databases.
  - **HDD (`mass-storage`):** Reserved for bulk data, Docker persistent volumes, and backups.
- **Management:** 
  - Manage Docker workloads via **Docker Compose** within dedicated sub-directories (e.g., `minecraft-server/`).
  - Assume VM 101 (`docker-host`) is managed via the **Portainer Agent** (Port 9001) connected to the Raspberry Pi 5 master node.

## 3. Operational Safety
- **Host Modifications:** Never modify Proxmox host-level network configurations (`/etc/network/interfaces`) or storage mounts (`/etc/fstab`) without explicit user confirmation.
- **Ryzen Stability:** Always respect the CPU governor (`performance`) and ZFS ARC limits established in `post_install.sh` and `PROXMOX_MASTER_PLAN.md`.

## 4. Development Workflow
- **New Services:** Every new service must include:
  1. A dedicated folder.
  2. A `docker-compose.yml`.
  3. A `README.md` with deployment and troubleshooting steps.
- **MCP Server:** Use the tools provided by the Proxmox MCP server (defined in `docker-mcp-setup/`) for real-time telemetry once deployed.

## 5. Git & Commit Policy
- **No Automatic Commits:** NEVER `git commit` or `git push` to ANY branch (including feature branches) without explicit, specific permission for that exact action.
- **Permission Protocol:** You may suggest or ask to commit ("Should I commit these changes to the feature branch?"), but you must wait for a clear "Yes" or directive before executing.
- **Branch Strategy:** 
  - Never commit directly to the `main` branch. 
  - All changes must be made on a feature or appropriately designated branch (e.g., `feature/`, `fix/`, `docs/`, `infra/`).
  - **Sync Protocol:** Always ensure the local `main` branch is up-to-date (`git pull origin main`) before branching for a new task.
  - **Remote Cleanup:** If a branch has been merged and deleted from the remote, create a new local branch for subsequent work rather than continuing on the stale local branch.
  - Merging into `main` should only occur after the task is fully validated and upon explicit user request.
