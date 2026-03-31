# Local LLM: Ollama & Open WebUI

This setup provides a local, private interface for LLM inference (Llama 3, Mistral, etc.) with RAG (Retrieval Augmented Generation) capabilities.

## 1. Resource Prerequisites
Before deploying, it is recommended to increase the `docker-host` (VM 101) RAM to at least **32GB** to handle larger models and context.

```bash
# On the Proxmox Host:
qm set 101 --memory 32768
```

## 2. Deployment
1.  Ensure `/mnt/data/` is mounted on VM 101 (pointing to your 1TB mass-storage disk).
2.  Deploy the stack:
    ```bash
    docker compose up -d
    ```

## 3. Usage
- **Web UI:** `http://192.168.1.40:3000`
- **First Run:** Create an admin account (this is local to the container).
- **Download a Model:** In the UI settings, pull `llama3` or `mistral`.

## 4. Homelab Assistant (RAG)
You can upload `lab_inventory.json` and `PROXMOX_MASTER_PLAN.md` to Open WebUI to give the LLM direct knowledge of your environment for maintenance tasks.
