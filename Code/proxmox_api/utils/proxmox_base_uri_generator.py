def proxmox_base_uri(host, port = "8006"):
    return f'https://{host}:{port}/api2/json'