from nornir_lib.modules.ping import PingLibrary
from nornir_lib.modules.traceroute import TracerouteLibrary 
from nornir_lib.modules.generic import GenericLibrary

import logging


logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

def run_command(hostname: str,
                command: str,
                target: str,
                config_file_path: str
               ):
    logging.info(f"Running nornir commands")
    if command == "ping":
        logging.info(f"Running ping command on {hostname} to {target}")
        ping_lib = PingLibrary(config_file_path)
        results = ping_lib.command(hostname, target)

    elif command == "traceroute":
        logging.info(f"Running ping command on {hostname} to {target}")
        traceroute_lib = TracerouteLibrary(config_file_path)
        results = traceroute_lib.command(hostname, target)

    else:
        logging.info(f"Running {command} on {hostname} to {target}")
        generic_lib = GenericLibrary(config_file_path)
        generic_lib.set_command(command)
        results = generic_lib.command(hostname,target)#target isnt currently being used by generic_lib

    return {"test_results": results}