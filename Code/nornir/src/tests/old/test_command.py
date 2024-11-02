from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_commands
from nornir_salt.plugins.tasks import netmiko_send_commands
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from utils.tools import updated_inventory_host


inventory, runner = updated_inventory_host("up202001001.yaml")
nr = InitNornir(
    inventory=inventory,
    runner=runner
    )

filtered_hosts = nr.filter(F(name__contains="pc1"))

def send_telnet_commands(task):
    #result = task.run(task=netmiko_send_command, command_string="\r\ntrace 10.0.0.28", delay_factor=5) 
    result = task.run(task=netmiko_send_commands, commands=["\r\n", "trace 10.0.0.28"], delay_factor=5)
    # config "show run" "Cisco IOS"
    return result
    

results = filtered_hosts.run(task=send_telnet_commands)
print_result(results)
