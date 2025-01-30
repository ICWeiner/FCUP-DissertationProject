import json
from nornir import InitNornir
from nornir.core.filter import F
from gns3_api.utils.gns3_parser import parse_gns3_to_yaml

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

up_linux = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))

for i in up_linux.inventory.hosts.items():
    print(i)

    # needed in the host file particular to the student
    student_ip = up_linux.inventory.hosts[i[0]].hostname 
    # used as filename related to student
    student_mec = i[0] 
    gns3_path = "gns3/" + student_mec

    parse_gns3_to_yaml(gns3_path, student_ip, student_mec, "inventory/")
