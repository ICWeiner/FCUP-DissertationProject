import time
from threading import Lock
from flask import current_app as app
from proxmox_api.utils.connection import proxmox_connect

proxmox_session_cache = {
    "session": None,
    "expires_at": 0
}
session_lock = Lock()

def get_flask_proxmox_session(proxmox_host, username, password):
    with session_lock:#lock for thread safety
        if proxmox_session_cache["session"] and proxmox_session_cache["expires_at"] > time.time():
            return proxmox_session_cache["session"]

        # If expired or missing, use the provided session creation function
        session = proxmox_connect(proxmox_host, username, password)
        print("#######################")
        print("New session created")
        print("#######################")
        proxmox_session_cache.update({
            "session": session,
            "expires_at": time.time() + 2 * 3500  # 2 hours from now(a bit less for safety)
        })
        return session