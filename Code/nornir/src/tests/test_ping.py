from modules.ping import PingLibrary
from nornir_utils.plugins.functions import print_result

# o up pode ser obter pelo ficheiro original dos alunos (hosts.yaml)


config = "up202001001.yaml"
ping_lib = PingLibrary(config)

# Perform ping for a hostname (the full destination ip must be provided)
ping_results = ping_lib.ping("pc1", "10.0.1.1")
print("Ping Results:", ping_results)
