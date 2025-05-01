from nornir_lib.modules.module import CommandModule
from nornir_lib.utils.constants import TOLERANCE
import re

class GenericModule(CommandModule):
    def __init__(self,file):
        self.input_command = None
        super().__init__(file)

    #To use this library, you need to set the command first e.g. set_command("show version")
    def set_command(self, command):
        self.input_command = command

    def _command_router(self, source, destination):
        results = self.get_result_strings(self._send_command(source, self.input_command))
        return self.interpret_cisco_response(results)
    
    def _command_switch(self, source, destination):
        results = self.get_result_strings(self._send_command(source, self.input_command))
        return self.interpret_cisco_response(results)
    
    def _command_vpcs(self, source, destination):
        results = self.get_result_strings(self._send_command(source, self.input_command))
        return self.interpret_vpcs_response(results)
    
    def _command_linux(self, source, destination):
        results = self.get_result_strings(self._send_command(source, self.input_command))
        return self.interpret_linux_response(results)
    
    def interpret_cisco_response(self, results):
        return True, results

    def interpret_linux_response(self, results):
        return True, results

    def interpret_vpcs_response(self, results):
        return True, results


