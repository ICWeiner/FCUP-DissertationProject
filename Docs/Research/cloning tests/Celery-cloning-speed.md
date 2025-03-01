Async version (Celery based)

for 10 VMs:
Template VM creation time: 34.961728 seconds
VM Cloning process time: 5.105833 seconds
VM deleting process time: 0.175033 seconds
Final CPU usage: 25%


for 20 VMs:
Template VM creation time: 34.836823 seconds
VM Cloning process time: 9.593564 seconds
VM deleting process time: 0.453605 seconds
Final CPU usage: 15%


Template VM creation time: 34.819028 seconds
VM Cloning process time: 9.480179 seconds
VM deleting process time: 0.468029 seconds
Final CPU usage: 16.3%


Template VM creation time: 34.618800 seconds
VM Cloning process time: 9.453679 seconds
VM deleting process time: 0.470697 seconds
Final CPU usage: 16.6%


for 100 VMs:
Template VM creation time: 34.790453  seconds
VM Cloning process time: 46.666599 seconds
VM deleting process time: 3.256207 seconds
Final CPU usage: 18.2%


Template VM creation time: 34.669975 seconds
VM Cloning process time: 51.141232 seconds
VM deleting process time: 3.313939 seconds
Final CPU usage: 15.7%


Template VM creation time: 34.737968 seconds
VM Cloning process time: 53.167206 seconds
VM deleting process time: 3.470970 seconds
Final CPU usage: 15.6%


for 200 VMs:
Template VM creation time: 35.015873 seconds
VM Cloning process time: 110.325907 seconds
FAILED deleting
Final CPU usage: 17.5%


Template VM creation time: 35.045584 seconds
VM Cloning process time: 120.727073 seconds
VM deleting process time: 9.250465 seconds
Final CPU usage: 18.4%


Template VM creation time: 35.015873 seconds
VM Cloning process time: 121.619209 seconds
VM deleting process time: 9.523142 seconds
Final CPU usage: 18.3%


Error processing task result for <User user1>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user2>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user3>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user4>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user5>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user6>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user7>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user8>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user9>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user10>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user11>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user12>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user13>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user14>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user15>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user16>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user17>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user18>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone


for 200 VMs: (8 cores)
Template VM creation time: 35.253194 seconds
VM Cloning process time: 100.127948 seconds
VM deleting process time: 10.531893 seconds
Final CPU usage: 35.3%

create linked clone of drive scsi0 (local-lvm:base-102-disk-1)
trying to acquire lock...
 OK
  WARNING: You have not turned on protection against thin pools running out of space.
  WARNING: Set activation/thin_pool_autoextend_threshold below 100 to trigger automatic extension of thin pools before they get full.
  Consider pruning pve VG archive with more then 2441 MiB in 13022 files (check archiving is needed in lvm.conf).
  WARNING: Sum of all thin volume sizes (<51.46 TiB) exceeds the size of thin pool pve/data and the size of whole volume group (<930.51 GiB).
  VG pve 14339 metadata on /dev/nvme0n1p3 (521537 bytes) exceeds maximum metadata size (521472 bytes)
TASK ERROR: clone failed: clone image 'pve/base-102-disk-1' error:   Failed to write VG pve


Template VM creation time: 35.380550 seconds
VM Cloning process time: 96.812612 seconds
VM deleting process time: 1.546878 seconds (not a lot of VMs were actually created since retries are not yet implemented)
Final CPU usage: 32.2%

Error processing task result for <User user2>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user5>: 500 Server Error: Linked clone feature is not supported for 'local-lvm:vm-102-disk-1' (scsi0) for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/102/clone
Error processing task result for <User user46>: 500 Server Error: Configuration file 'nodes/pve1/qemu-server/499555190.conf' does not exist for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/499555190/config
Error processing task result for <User user47>: 500 Server Error: Configuration file 'nodes/pve1/qemu-server/214225228.conf' does not exist for url: https://192.168.57.22:8006/api2/json/nodes/pve1/qemu/214225228/config

for 200 VMs: (8 cores - 4 workers)
Template VM creation time: 35.237862 seconds
VM Cloning process time: 129.823284 seconds
VM deleting process time: 0.762131 seconds
Final CPU usage: 23.7%

-AFTER IO CLEANUP
(only 2 cores)
VM Cloning process time: 44.905797 seconds

(only 8 cores)
VM Cloning process time: 33.338705