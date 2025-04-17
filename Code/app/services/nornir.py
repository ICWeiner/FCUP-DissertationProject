from nornir_lib.modules.ping import PingLibrary
from nornir_lib.modules.traceroute import TracerouteLibrary 
from nornir_lib.modules.generic import GenericLibrary

from logger.logger import get_logger

logger = get_logger(__name__)

def run_command(hostname: str,
                command: str,
                target: str,
                config_file_path: str
               ):
    logger.info(f"Running nornir commands")
    
    if command == "ping":
        logger.info(f"Running ping command on {hostname} to {target}")
        ping_lib = PingLibrary(config_file_path)
        results = ping_lib.command(hostname, target)

    elif command == "traceroute":
        logger.info(f"Running ping command on {hostname} to {target}")
        traceroute_lib = TracerouteLibrary(config_file_path)
        results = traceroute_lib.command(hostname, target)

    else:
        logger.info(f"Running {command} on {hostname} to {target}")
        generic_lib = GenericLibrary(config_file_path)
        generic_lib.set_command(command)
        results = generic_lib.command(hostname,target)#target isnt currently being used by generic_lib

    return {"test_results": results}