from nornir import InitNornir
from gns3_api.gns3_actions import get_project, gns3_to_yaml
from nornir.core.filter import F

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

source_file = "test/test.gns3"

up_linux = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))

for i in up_linux.inventory.hosts.items():
    # needed in the host file particular to the student
    student_ip = up_linux.inventory.hosts[i[0]].hostname 
    # used as filename related to student
    student_mec = i[0] 
    gns3_path = "gns3/" + student_mec
    inventory_path = "inventory/"

    nodes = get_project(gns3_path, student_ip)
    gns3_to_yaml(nodes, student_ip, student_mec)
    
