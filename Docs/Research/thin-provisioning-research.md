Setup currently is using thin provisioning from a pool named "data"

at the present there is a template vm with ID 10000, all gns3-server instances are created by cloning this VM and making the necessary changes

by using lvs command on pve host, more detailed information can be obtained

in particular some usefull flags that may appear in its output are:
- r - read-only, typically indicates that specified disk is a template
- i - inherited, often indicates a snapshot or a linked clone
- t - thin pool usage, indicates the disk is part of a thin pool