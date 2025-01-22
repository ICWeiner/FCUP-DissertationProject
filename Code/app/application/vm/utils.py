from flask import current_app as app

def _get_proxmox_host():
    return app.config['PROXMOX_HOST']

def _get_proxmox_credentials():
    return app.config['PROXMOX_USER'], app.config['PROXMOX_PASSWORD']

def _get_proxmox_host_and_credentials():
    return _get_proxmox_host(), *_get_proxmox_credentials()