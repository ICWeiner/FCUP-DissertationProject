from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from utils.file_transfer import transfer_file
from nornir.core.filter import F

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

source_file = "test/test.gns3"

up_linux = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))

print(f"Total: {len(up_linux.inventory.hosts.items())}")

if up_linux.inventory.hosts:
    result = up_linux.run(
        task=transfer_file,
        source_file=source_file,
    )

    print_result(result)
else:
    print("No hosts matched the filter criteria.")
