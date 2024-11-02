from modules.module import CommandLibrary
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir.core.task import AggregatedResult, MultiResult, Result
from utils.tools import updated_inventory_host
from utils.constants import TOLERANCE
#from utils.results_processing import get_result_strings
import re

class PingLibrary(CommandLibrary):
    def __init__(self,file):
        super().__init__(file)

    def _command_router(self, source, destination):
        results = self.get_result_strings(self._send_command(source, destination, ""))
        return self.interpret_cisco_response(results)
    
    def _command_switch(self, source, destination):
        results = self.get_result_strings(self._send_command(source, destination, ""))
        return self.interpret_cisco_response(results)
    
    def _command_vpcs(self, source, destination):
        results = self.get_result_strings(self._send_command(source, destination, "-c 4"))
        return self.interpret_vpcs_response(results)
    
    def _command_linux(self, source, destination):
        results = self.get_result_strings(self._send_command(source, destination, "-c 4"))
        return self.interpret_linux_response(results)
    
    def _send_command(self, source, destination, options):
        filter = self.nr.filter(F(name__contains=source))
        results = filter.run(
            task=netmiko_send_command,
            command_string=f"ping {destination} {options}"
        )
        print(self.get_result_strings(results))
        return results # returnar tuplo bool, msg
    
    def interpret_cisco_response(self, results):
        success_match = re.search(r'Success rate is (\d+) percent \((\d+)/(\d+)\)', results)
        if success_match:
            success_rate = int(success_match.group(1))
            if success_rate >= 100 - TOLERANCE:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        
        return False, "Unable to determine ping status from results"

    def interpret_linux_response(self, results):
        packet_info_match = re.search(r'(\d+) packets transmitted, (\d+) received', results)
        if packet_info_match:
            packets_sent = int(packet_info_match.group(1))
            packets_received = int(packet_info_match.group(2))
            success_rate = (packets_received / packets_sent) * 100
            if success_rate >= 100 - TOLERANCE:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        elif "Network is unreachable" in results:
            return False, "Ping failed: Network is unreachable"
        
        return False, "Unable to determine ping status from results"

    def interpret_vpcs_response(self, results):
        success_matches = re.findall(r'icmp_seq=\d+ ttl=\d+ time=.* ms', results)
        total_pings = results.count('icmp_seq=')
        successful_pings = len(success_matches)
        print(f'results is {results}')
        print(f'total pings is {total_pings} and successful ping is {successful_pings} and success matches is {success_matches}')
        if total_pings > 0:
            success_rate = (successful_pings / total_pings) * 100
            if success_rate >= 100 - TOLERANCE:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        elif "not reachable" in results:
            return False, "Ping failed: Network is unreachable."
        
        return False, "Unable to determine ping status from results"


