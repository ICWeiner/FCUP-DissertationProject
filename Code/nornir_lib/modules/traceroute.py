from nornir_lib.modules.module import CommandLibrary
import re

class TracerouteLibrary(CommandLibrary):
    def __init__(self,file):
        super().__init__(file)
    
    def _command_router(self, source, destination):
        command=f"traceroute {destination} "
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_cisco_traceroute_response(results)
    
    def _command_switch(self, source, destination):
        command=f"traceroute {destination} "
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_cisco_traceroute_response(results)
    
    def _command_vpcs(self, source, destination):
        command=f"trace {destination} "
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_vpcs_traceroute_response(results)
    
    def _command_linux(self, source, destination):
        command=f"traceroute {destination} "
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_linux_traceroute_response(results)
    
    '''
    tracing the route to 10.0.1.4

    1 10.0.1.4 64msec 60msec 60msec
    '''
    def interpret_cisco_traceroute_response(self, results):
        # Cisco traceroute response interpretation
        if "Tracing the route to" in results:
            if "!" in results or "*" not in results:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        
        return False, "Unable to determine traceroute status from results"


    """
    traceroute to 10.0.0.3 (10.0.0.3), 30 hops max, 60 byte packets
    1  10.0.0.3  0.042 ms  0.010 ms  0.008 ms
    [root@localhost /]# 


    traceroute to 10.0.0.44 (10.0.0.44), 30 hops max, 60 byte packets
    1  10.0.0.3  3070.490 ms !H  3069.804 ms !H  3070.425 ms !H
    """
    def interpret_linux_traceroute_response(self, results):
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
    def interpret_vpcs_traceroute_response(self, results):
        # VPCS traceroute response interpretation
        if "trace to" in results:
            if "ms" in results:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        elif "not reachable" in results:
            return False, "Traceroute failed: Network is unreachable."
        
        return False, "Unable to determine traceroute status from results"
