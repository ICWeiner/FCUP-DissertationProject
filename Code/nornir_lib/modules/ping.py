from nornir_lib.modules.module import CommandModule
from nornir_lib.utils.constants import TOLERANCE
import re

class PingModule(CommandModule):
    def __init__(self,file):
        super().__init__(file)

    def _command_router(self, source, destination):
        command = f'ping {destination} '
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_cisco_response(results)
    
    def _command_switch(self, source, destination):
        command = f'ping {destination} '
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_cisco_response(results)
    
    def _command_vpcs(self, source, destination):
        command = f'ping {destination} '
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_vpcs_response(results)
    
    def _command_linux(self, source, destination):
        command = f'ping {destination} -c 4'
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_linux_response(results)
    
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
        if total_pings > 0:
            success_rate = (successful_pings / total_pings) * 100
            if success_rate >= 100 - TOLERANCE:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        elif "not reachable" in results:
            return False, "Ping failed: Network is unreachable."
        
        return False, "Unable to determine ping status from results"


