# Issues with disk removal when mass cloning and subsequent deleting 

clone 200 VMs using celery
Single PVE node
VMs are cloned in around 30 seconds using HTTP requests to create linked clones from a specific template, no issues occurr

afterwards HTTP requests are sent to delete every of the 200 VMs just cloned

# 1st Output
Of these, the first 90ish output this to the task history

```
trying to acquire lock...
 OK
  Logical volume "vm-348786940-disk-0" successfully removed.
TASK OK
```

These all delete their disk, as is expected.

# 2nd Output

Around the 100 mark, starts alternating between the 1st output and the 2nd

```
trying to acquire lock...
Could not remove disk 'local-lvm:vm-120993831-disk-0', check manually: can't lock file '/var/lock/pve-manager/pve-storage-local-lvm' - got timeout
trying to acquire lock...
 OK
  Logical volume "vm-120993831-disk-0" successfully removed.
TASK OK
```

around the 120 mark we only see the second output.

# 3rd Output

Around the 180 mark

```
trying to acquire lock...
Could not remove disk 'local-lvm:vm-363495383-disk-0', check manually: can't lock file '/var/lock/pve-manager/pve-storage-local-lvm' - got timeout
trying to acquire lock...
can't lock file '/var/lock/pve-manager/pve-storage-local-lvm' - got timeout
TASK OK
```

the last 3 return this

```
trying to acquire lock...
Could not remove disk 'local-lvm:vm-5469324-disk-0', check manually: can't lock file '/var/lock/pve-manager/pve-storage-local-lvm' - got timeout
trying to acquire lock...
can't lock file '/var/lock/pve-manager/pve-storage-local-lvm' - got timeout
trying to acquire cfs lock 'file-user_cfg' ...
TASK OK
```


# Conclusions? 

This suggests Proxmox's locking mechanism can't keep pace with the delete requests.  
The lock is used to ensure that two tasks dont modify the LVM's metadata simulatenously.  
Since there should be some background tasks that are piling up, the system cant keep pace and eventually starts using retries to keep up but even this is insuficient and starts failing more and more towards the end as it becomes fully congested.  
At the end the system starts becoming overwhelmed and also begins having trouble updating its internal storage config file.  

