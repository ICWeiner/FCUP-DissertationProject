from nornir import InitNornir
from utils.get_gns3_api import get_project, gns3_to_yaml
from nornir.core.filter import F
from nornir.core.task import AggregatedResult, MultiResult, Result
from nornir_http.result import HTTPResult
from nornir_http.tasks import http_method
from nornir_utils.plugins.functions import print_result

def get_json_from_result(agg_result: AggregatedResult):
    
    def _extract(result):
        if isinstance(result, AggregatedResult):
            for host_result in result.values():
                _extract(host_result)
        elif isinstance(result, MultiResult):
            for sub_result in result:
                _extract(sub_result)
        elif isinstance(result, Result):
            if result.result:
                return result.response.json()

    return _extract(agg_result)

def get_project_list(node_ip):
    
    '''results = nr.run(
        task=http_method,
        method='get',
        url=f'http://{node_ip}:3080/v2/projects',
        raise_for_status=True,
        verify=False,
        name='Collect list of projects')'''
    
    results = http_method(
        method="get",
        url=f"http://{node_ip}:3080/v2/projects",
        raise_for_status=True,
        verify=False)
    return get_json_from_result(results)

# Initialize Nornir
try:
    nr = InitNornir(config_file="config.yaml")
except Exception as e:
    print(f"Failed to initialize Nornir: {str(e)}")
    exit(1)

source_file = "test/test.gns3" #insert path to source file starting from /home/{username}/GNS3/

up_linux = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))


print(up_linux.inventory.hosts)
for i in up_linux.inventory.hosts.items(): 
    
    # needed in the host file particular to the student
    node_ip = up_linux.inventory.hosts[i[0]].hostname 
    print(f'student ip is : {node_ip}')
    # used as filename related to student
    node_mec = i[0] 
    print(f'student mec number is : {node_mec}')
    print(get_project_list(node_ip)[0]['path'])
    #print(results['host1.cmh'][0].result=)
    #gns3_path = "gns3/" + student_mec
    #inventory_path = "inventory/"

    #nodes = get_project(gns3_path, student_ip)
    #gns3_to_yaml(nodes, student_ip, student_mec)
    