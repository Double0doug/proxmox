import os
import logging
from mcp.server.fastmcp import FastMCP
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

# Load .env file for local testing (not needed in Docker Compose)
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("proxmox-mcp")

# Environment Variables
PVE_HOST = os.getenv("PVE_HOST", "192.168.1.50")
PVE_USER = os.getenv("PVE_USER", "root@pam")
PVE_TOKEN_ID = os.getenv("PVE_TOKEN_ID")
PVE_TOKEN_SECRET = os.getenv("PVE_TOKEN_SECRET")

# Initialize MCP Server
mcp = FastMCP("ProxmoxLab")

# Global PVE connection
pve = None

def get_pve_conn():
    global pve
    if pve is None:
        try:
            pve = ProxmoxAPI(
                PVE_HOST,
                user=PVE_USER,
                token_name=PVE_TOKEN_ID,
                token_value=PVE_TOKEN_SECRET,
                verify_ssl=False
            )
            logger.info(f"Connected to Proxmox at {PVE_HOST}")
        except Exception as e:
            logger.error(f"Failed to connect to Proxmox: {e}")
            raise e
    return pve

@mcp.tool()
async def list_vms() -> str:
    """Lists all VMs and Containers managed by the Proxmox host."""
    try:
        conn = get_pve_conn()
        resources = conn.nodes("pve").qemu.get()
        lines = [f"ID: {r['vmid']} | Name: {r['name']} | Status: {r['status']}" for r in resources]
        return "\n".join(lines) if lines else "No VMs found."
    except Exception as e:
        return f"Error listing VMs: {str(e)}"

@mcp.tool()
async def get_vm_status(vmid: int) -> str:
    """Returns real-time CPU and RAM usage for a specific VM ID."""
    try:
        conn = get_pve_conn()
        status = conn.nodes("pve").qemu(vmid).status.current.get()
        name = status.get('name', 'Unknown')
        state = status.get('status', 'unknown').upper()
        cpu = status.get('cpu', 0) * 100
        ram = status.get('mem', 0) / (1024**3)
        return (f"VM {vmid} ({name}): {state}\n"
                f"CPU: {cpu:.1f}% | RAM: {ram:.2f}GB")
    except Exception as e:
        return f"Error fetching status for VM {vmid}: {str(e)}"

@mcp.resource("pve://cluster/tasks")
async def get_recent_tasks() -> str:
    """Provides the 10 most recent logs from the Proxmox task history."""
    try:
        conn = get_pve_conn()
        tasks = conn.nodes("pve").tasks.get(limit=10)
        lines = [f"{t.get('starttime', 'N/A')}: {t.get('type', 'N/A')} ({t.get('status') or 'RUNNING'})" for t in tasks]
        return "\n".join(lines) if lines else "No recent tasks."
    except Exception as e:
        return f"Error fetching tasks: {str(e)}"

if __name__ == "__main__":
    # Check for SSE mode via environment or CLI
    # FastMCP uses standard transport selection
    mcp.run()
