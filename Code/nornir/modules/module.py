from nornir import InitNornir
from nornir.core.task import AggregatedResult, MultiResult, Result
from nornir_netmiko.tasks import netmiko_send_command
from utils.tools import updated_inventory_host
import re

class CommandLibrary:
    def __init__(self, file):
        inventory, runner = updated_inventory_host(file)
        self.nr = InitNornir(
            inventory=inventory,
            runner=runner
            )
    
    def command(self, source, destination):
        # Get the platform group of the source
        platform = self._get_platform(source)

        if platform == "cisco_router":
            return self._command_router(source, destination)
        elif platform == "cisco_switch":
            return self._command_switch(source, destination)
        elif platform == "vpcs":
            return self._command_vpcs(source, destination)
        elif platform == "linuxvm":
            return self._command_linux(source, destination)
        else:
            return f"Unsupported platform {platform} for source {source}"
    
    def _get_platform(self, source):
        # Get the platform group of the source
        host = self.nr.inventory.hosts.get(source)
        if host:
            return str(next(iter(host.groups), None))
        else:
            return None   
                                                                                   
    def _command_router(self, source, destination):
        raise NotImplementedError("Please Implement this method")
    
    def _command_switch(self, source, destination):
        raise NotImplementedError("Please Implement this method")
    
    def _command_vpcs(self, source, destination):
        raise NotImplementedError("Please Implement this method")
    
    def _command_linux(self, source, destination):
        raise NotImplementedError("Please Implement this method")
    
    def interpret_cisco_response(self, results):
        raise NotImplementedError("Please Implement this method")

    def interpret_linux_response(self, results):
        raise NotImplementedError("Please Implement this method")

    def interpret_vpcs_response(self, results):
        raise NotImplementedError("Please Implement this method")
    
    def _send_command(self, source, command):
        filter = self.nr.filter(F(name__contains=source))
        results = filter.run(
            task = netmiko_send_command,
            command_string = command
        )
        print(self.get_result_strings(results))
        return results # returnar tuplo bool, msg
        
    def get_result_strings(self, aggregated_result: AggregatedResult) -> list:

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


