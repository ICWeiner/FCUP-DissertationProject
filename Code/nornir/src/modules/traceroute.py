from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import AggregatedResult, MultiResult, Result
from utils.tools import updated_inventory_host
import re

class TracerouteLibrary:
    def __init__(self, file):
        inventory, runner = updated_inventory_host(file)
        self.nr = InitNornir(
            inventory=inventory,
            runner=runner
            )
    
    def traceroute(self, source, destination):
        # Get the platform group of the source
        platform = self._get_platform(source)

        if platform == "cisco_router":
            return self._traceroute_router(source, destination)
        elif platform == "cisco_switch":
            return self._traceroute_switch(source, destination)
        elif platform == "vpcs":
            return self._traceroute_vpc(source, destination)
        elif platform == "linuxvm":
            return self._traceroute_linux(source, destination)
        else:
            return f"Unsupported platform {platform} for source {source}"
    
    def _get_platform(self, source):
        # Get the platform group of the source
        host = self.nr.inventory.hosts.get(source)
        if host:
            return str(next(iter(host.groups), None))
        else:
            return None   
    
    def _traceroute_router(self, source, destination):
        results = get_result_strings(self._send_traceroute_command(source, destination, ""))
        return interpret_cisco_traceroute_response(results)
    
    def _traceroute_switch(self, source, destination):
        results = get_result_strings(self._send_traceroute_command(source, destination, ""))
        return interpret_cisco_traceroute_response(results)
    
    def _traceroute_vpc(self, source, destination):
        results = get_result_strings(self._send_traceroute_command(source, destination, ""))
        return interpret_vpcs_traceroute_response(results)
    
    def _traceroute_linux(self, source, destination):
        results = get_result_strings(self._send_traceroute_command(source, destination, ""))
        return interpret_linux_traceroute_response(results)
    
    def _send_traceroute_command(self, source, destination, options):
        filter = self.nr.filter(F(name__contains=source))
        results = filter.run(
            task=netmiko_send_command,
            command_string=f"traceroute {destination} {options}"
        )
        #print_result(results)
        print(get_result_strings(results))
        return results # return tuple (bool, msg)

def interpret_cisco_traceroute_response(results):
    # Cisco traceroute response interpretation
    if "Tracing the route to" in results:
        if "!" in results or "*" not in results:
            return True, get_result_strings(results)
        else:
            return False, get_result_strings(results)
    
    return False, "Unable to determine traceroute status from results"


"""
traceroute to 10.0.0.3 (10.0.0.3), 30 hops max, 60 byte packets
 1  10.0.0.3  0.042 ms  0.010 ms  0.008 ms
[root@localhost /]# 


traceroute to 10.0.0.44 (10.0.0.44), 30 hops max, 60 byte packets
 1  10.0.0.3  3070.490 ms !H  3069.804 ms !H  3070.425 ms !H
"""
def interpret_linux_traceroute_response(results):
    # Linux traceroute response interpretation
    if "traceroute to" in results:
        if "ms" in results:
            return True, results
        elif "Network is unreachable" in results:
            return False, "Traceroute failed: Network is unreachable"
        elif "No route to host" in results:
            return False, "Traceroute failed: No route to host"
        elif "*" in results:
            return False, "Traceroute failed: Request timed out"
        else:
            return False, "Traceroute failed: Unknown error"
    return False, "Unable to determine traceroute status from results"


"""
Fail message
trace to 10.0.0.6, 8 hops max, press Ctrl+C to stop
host (10.0.0.6) not reachable

Successful message
traceroute to 10.0.0.2, 8 hops max
 1 10.0.0.2     0.001 ms
"""
def interpret_vpcs_traceroute_response(results):
    # VPCS traceroute response interpretation
    if "trace to" in results:
        if "ms" in results:
            return True, get_result_strings(results)
        else:
            return False, get_result_strings(results)
    elif "not reachable" in results:
        return False, "Traceroute failed: Network is unreachable."
    
    return False, "Unable to determine traceroute status from results"

def get_result_strings(aggregated_result: AggregatedResult) -> str:
    result_strings = []

    def _extract(result):
        if isinstance(result, AggregatedResult):
            for host_result in result.values():
                _extract(host_result)
        elif isinstance(result, MultiResult):
            for sub_result in result:
                _extract(sub_result)
        elif isinstance(result, Result):
            if result.result:
                # remove \x1b[?2004l' hexadecimal values ANSI escape codes (often used for terminal control sequences)
                clean_result = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', result.result)
                result_strings.append(clean_result)

    _extract(aggregated_result)
    return ''.join(result_strings)

