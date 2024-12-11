"As each snapshot needs to save the whole RAM to disk you need to make sure there is enough space on your storage. If you use a lot of RAM in the VM it takes some time to save it. "

Snapshots take longer when RAM is also collected, around 1sec per gigabyte on our machine.

As proxmox uses ZFS, this particular file system enables fast and cheap snapshots that dont include RAM