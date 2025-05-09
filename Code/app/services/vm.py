import uuid
import asyncio

from app.models import WorkVm
from app.dependencies.repositories import ExerciseRepositoryDep
from app.services import proxmox as proxmox_services

async def create_users_work_vms(request_user, users, exercises):
    '''
    Creates work VMs for a list of users, assigning each user a cloned VM 
    from the template VM associated with each exercise.

    This function ensures that each user receives a separate WorkVM for each 
    exercise template while preserving execution order using asyncio.gather().

    Args:
        users (List[User]): A list of users who need work VMs.
        exercises (List[Exercise]): A list of exercises, each having an associated template VM.

    Returns:
        List[WorkVm]: A list of WorkVm objects, each representing a VM created 
                      for a user and linked to the appropriate template VM.
    '''

    if not isinstance(users, list) or not isinstance(exercises, list):
        return []

    tasks = []

    created_vms = []

    assignments = []  # To store (user, exercise) in order

    for exercise in exercises:
        for user in users:
            hostname = f'vm-{uuid.uuid4().hex[:12]}'  # Generate a random hostname
            tasks.append(proxmox_services.aclone_vm(request_user, exercise.templatevm.proxmox_id, hostname))
            assignments.append((user, exercise, hostname)) 

    vm_ids = await asyncio.gather(*tasks)

    for (user, exercise, hostname), vm_id in zip(assignments, vm_ids):
        workvm = WorkVm(
                proxmox_id=vm_id,
                user=user,
                templatevm=exercise.templatevm,
                hostname = hostname
            )
        created_vms.append(workvm)

    return created_vms