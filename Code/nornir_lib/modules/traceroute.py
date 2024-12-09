from nornir_lib.modules.module import CommandLibrary
import re

class TracerouteLibrary(CommandLibrary):
    def __init__(self,file):
        super().__init__(file)
    
    def _command_router(self, source, destination):
        command=f"traceroute {destination} ttl 1 4"#TODO: make ttl optional and not hardcoded
        results = self.get_result_strings(self._send_command(source, command))
        return self.interpret_cisco_traceroute_response(results)
    
    def _command_switch(self, source, destination):
        command=f"traceroute {destination} ttl 1 4"#TODO: make ttl optional and not hardcoded
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
    SUCCESS
    Type escape sequence to abort.
    Tracing the route to 10.0.1.3

    1  * 
        10.0.1.3 48 msec 64 msec

    FAILURE
    Type escape sequence to abort.
    Tracing the route to 10.0.1.4

    1  *  *  * 
    2  *  *  * 
    3  *  *  * 
    4  *  *  * 

    '''
    def interpret_cisco_traceroute_response(self, results):#TODO: Test this expression
        match = re.search(r"Tracing the route to ([\d.]+)", results)
        
        if match:
            target_ip = match.group(1)  # Extracted target IP
            
            # Check if the target IP appears in the traceroute responses
            if re.search(rf"\b{target_ip}\b.*\d+\s+msec", results):
                return True, f"Traceroute successfully reached the target IP: {target_ip}"
            else:
                return False, f"Traceroute failed to reach the target IP: {target_ip}"
        
        return False, "Unable to determine the target IP from the results."


    """
    SUCCESS
    traceroute to 10.0.0.3 (10.0.0.3), 30 hops max, 60 byte packets
    1  10.0.0.3  0.042 ms  0.010 ms  0.008 ms
    [root@localhost /]# 

    FAILURE
    traceroute to 10.0.0.44 (10.0.0.44), 30 hops max, 60 byte packets
    1  10.0.0.3  3070.490 ms !H  3069.804 ms !H  3070.425 ms !H
    """
    def interpret_linux_traceroute_response(self, results):#TODO: this doesnt seem correct...
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
    SUCCESS
    traceroute to 10.0.0.2, 8 hops max
    1 10.0.0.2     0.001 ms

    FAILURE
    trace to 10.0.0.6, 8 hops max, press Ctrl+C to stop
    host (10.0.0.6) not reachable
    """
    def interpret_vpcs_traceroute_response(self, results):#TODO: one says traceroute and the other says trace...
        # VPCS traceroute response interpretation
        if "trace to" in results:
            if "ms" in results:
                return True, self.get_result_strings(results)
            else:
                return False, self.get_result_strings(results)
        elif "not reachable" in results:
            return False, "Traceroute failed: Network is unreachable."
        
        return False, "Unable to determine traceroute status from results"
