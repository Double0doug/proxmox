# Homelab Backend Integration Plan: LLM + MCP

## 1. Objective
Transform the local **Gemma 2 (9B)** instance into a proactive homelab backend. Instead of a chatbot, the LLM will serve as an orchestration layer that identifies infrastructure issues on Proxmox and monitors Home Assistant states via the **Model Context Protocol (MCP)**.

## 2. Infrastructure Architecture & Methodology
Based on the **Big-Lab-01** standards:
- **Primary Orchestration:** Use **Portainer (Stacks)** on the Raspberry Pi 5 (managing `docker-host` via agent) for deploying MCP and LLM containers.
- **Sensitive Config:** Use **SSH** to VM 101 (`docker-host`) for initial directory creation and `.env` file management to keep secrets out of Git/UI.
- **Credential Source:** Use the **Proxmox Web UI** for API Token generation.

## 3. Implementation Phases

### Phase 1: Proxmox MCP Activation (Portainer + SSH)
- [ ] **API Token (Proxmox UI):** Create a token for `root@pam` with `PVEAuditor` permissions.
- [ ] **Directory & Env (SSH):** 
    - Ensure `~/git/proxmox/docker-mcp-setup/` exists.
    - Create `.env` with `PVE_TOKEN_SECRET`.
- [ ] **Deployment (Portainer):** Create a new Stack using the `docker-compose.yml` in `docker-mcp-setup/`.
- [ ] **Validation:** Verify the SSE endpoint at `http://192.168.1.40:8000/sse`.

### Phase 2: Home Assistant MCP Setup (Portainer + SSH)
- [ ] **Directory (SSH):** Create `~/git/proxmox/ha-mcp-setup/`.
- [ ] **Deployment (Portainer):** Create a new Stack for the HA MCP server.
    - **Image:** `modelcontextprotocol/server-homeassistant`
    - **Env Vars:** `HASS_URL` and `HASS_TOKEN`.
- [ ] **Validation:** Verify the SSE endpoint at `http://192.168.1.40:8001/sse`.

### Phase 3: Open WebUI Tool Integration (Web UI)
- [ ] **Connect MCPs:** Under Settings > External Connections > MCP, add:
    - `Proxmox MCP`: `http://192.168.1.40:8000/sse`
    - `Home Assistant MCP`: `http://192.168.1.40:8001/sse`
- [ ] **Tool Binding:** Confirm Gemma 2 recognizes tools like `list_vms`, `get_vm_status`, and `get_ha_states`.

### Phase 4: Backend Logic & Problem Identification (Gemma 2)
- [ ] **System Prompting:** Configure a "Homelab Manager" model profile with instructions to:
    - Periodically check Proxmox `get_recent_tasks` for failures.
    - Correlate high CPU usage in Proxmox with specific Home Assistant activity.
    - Alert on host-level stability issues (e.g., Ryzen governor shifts).

## 4. Testing Scenarios
1.  **Storage:** Gemma identifies that `mass-storage` is low on space.
2.  **Network:** Gemma detects `home-assistant-pi` is unresponsive.
3.  **Root Cause:** Gemma analyzes Proxmox logs to explain a VM failure.
