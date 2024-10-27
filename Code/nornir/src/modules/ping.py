from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import AggregatedResult, MultiResult, Result
from utils.tools import updated_inventory_host
from utils.constants import TOLERANCE
import re

class PingLibrary:
    def __init__(self, file):
        inventory, runner = updated_inventory_host(file)
        self.nr = InitNornir(
            inventory=inventory,
            runner=runner
            )
    
    def ping(self, source, destination):
        # Get the platform group of the source
        platform = self._get_platform(source)

        if platform == "cisco_router":
            return self._ping_router(source, destination)
        elif platform == "cisco_switch":
            return self._ping_switch(source, destination)
        elif platform == "vpcs":
            return self._ping_vpc(source, destination)
        elif platform == "linuxvm":
            return self._ping_linux(source, destination)
        else:
            return f"Unsupported platform {platform} for source {source}"
    
    def _get_platform(self, source):
        # Get the platform group of the source
        host = self.nr.inventory.hosts.get(source)
        if host:
            return str(next(iter(host.groups), None))
        else:
            return None   
                                                                                   
    def _ping_router(self, source, destination):
        results = get_result_strings(self._send_ping_command(source, destination, ""))
        return interpret_cisco_response(results)
    
    def _ping_switch(self, source, destination):
        results = get_result_strings(self._send_ping_command(source, destination, ""))
        return interpret_cisco_response(results)
    
    def _ping_vpc(self, source, destination):
        results = get_result_strings(self._send_ping_command(source, destination, "-c 4"))
        return interpret_vpcs_response(results)
    
    def _ping_linux(self, source, destination):
        results = get_result_strings(self._send_ping_command(source, destination, "-c 4"))
        return interpret_linux_response(results)
    
    def _send_ping_command(self, source, destination, options):
        filter = self.nr.filter(F(name__contains=source))
        results = filter.run(
            task=netmiko_send_command,
            command_string=f"ping {destination} {options}"
        )
        #print_result(results)
        print(get_result_strings(results))
        return results # returnar tuplo bool, msg
    
def interpret_cisco_response(results):
    success_match = re.search(r'Success rate is (\d+) percent \((\d+)/(\d+)\)', results)
    if success_match:
        success_rate = int(success_match.group(1))
        if success_rate >= 100 - TOLERANCE:
            return True, get_result_strings(results)
        else:
            return False, get_result_strings(results)
    
    return False, "Unable to determine ping status from results"

def interpret_linux_response(results):
    packet_info_match = re.search(r'(\d+) packets transmitted, (\d+) received', results)
    if packet_info_match:
        packets_sent = int(packet_info_match.group(1))
        packets_received = int(packet_info_match.group(2))
        success_rate = (packets_received / packets_sent) * 100
        if success_rate >= 100 - TOLERANCE:
            return True, get_result_strings(results)
        else:
            return False, get_result_strings(results)
    elif "Network is unreachable" in results:
        return False, "Ping failed: Network is unreachable"
    
    return False, "Unable to determine ping status from results"

def interpret_vpcs_response(results):
    success_matches = re.findall(r'icmp_seq=\d+ ttl=\d+ time=.* ms', results)
    total_pings = results.count('icmp_seq=')
    successful_pings = len(success_matches)
    print(f'results is {results}')
    print(f'total pings is {total_pings} and successful ping is {successful_pings} and success matches is {success_matches}')
    if total_pings > 0:
        success_rate = (successful_pings / total_pings) * 100
        if success_rate >= 100 - TOLERANCE:
            return True, get_result_strings(results)
        else:
            return False, get_result_strings(results)
    elif "not reachable" in results:
        return False, "Ping failed: Network is unreachable."
    
    return False, "Unable to determine ping status from results"
    
def get_result_strings(aggregated_result: AggregatedResult) -> list:

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


