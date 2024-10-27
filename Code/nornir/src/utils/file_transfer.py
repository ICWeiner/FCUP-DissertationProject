from nornir.core.task import Task, Result
from nornir_netmiko.tasks import netmiko_file_transfer

def transfer_file(task: Task, source_file: str):    
    try:
        # If the file exists, proceed with the transfer
        result = task.run(
            task=netmiko_file_transfer,
            source_file=source_file,
            dest_file="gns3/" + task.host.name,
            direction='get',  # Change direction to 'get' to transfer from remote to local
            file_system='/home/up/GNS3/projects',
            overwrite_file=True
        )

        return Result(
            host=task.host,
            result=f"File {source_file} transferred to {task.host.name}",
            changed=True
        )
    except Exception as e:
        return Result(
            host=task.host,
            result=f"Failed to transfer file {source_file} to {task.host.name}: {str(e)}",
            failed=True
        )