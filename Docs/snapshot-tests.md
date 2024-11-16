With RAM

Run 1
  Logical volume "vm-301-state-speedtest" created.
saving VM state and RAM using storage 'local-lvm'
1.00 MiB in 0s
1.02 GiB in 1s
1.90 GiB in 2s
2.42 GiB in 3s
2.93 GiB in 4s
completed saving the VM state in 5s, saved 3.20 GiB
snapshotting 'drive-scsi0' (local-lvm:vm-301-disk-0)
  Logical volume "snap_vm-301-disk-0_speedtest" created.
TASK OK

duration 18.8s

Run 2

  Logical volume "vm-300-state-speedtest" created.
saving VM state and RAM using storage 'local-lvm'
1.00 MiB in 0s
994.37 MiB in 1s
1.93 GiB in 2s
2.59 GiB in 3s
2.59 GiB in 4s
3.44 GiB in 5s
completed saving the VM state in 5s, saved 3.65 GiB
snapshotting 'drive-scsi0' (local-lvm:vm-300-disk-0)
  Logical volume "snap_vm-300-disk-0_speedtest" created.
TASK OK

25.9s

Run 3
  Logical volume "vm-800-state-speedtest" created.
saving VM state and RAM using storage 'local-lvm'
1.00 MiB in 0s
992.80 MiB in 1s
1.94 GiB in 2s
2.51 GiB in 3s
2.60 GiB in 4s
3.60 GiB in 5s
completed saving the VM state in 5s, saved 3.76 GiB
snapshotting 'drive-scsi0' (local-lvm:vm-800-disk-0)
  Logical volume "snap_vm-800-disk-0_speedtest" created.
TASK O

20.8s

Without RAM

Run 1
snapshotting 'drive-scsi0' (local-lvm:vm-300-disk-0)
  Logical volume "snap_vm-300-disk-0_speedtest_noram" created.
TASK OK
7.5s

Run 2
snapshotting 'drive-scsi0' (local-lvm:vm-301-disk-0)
  Logical volume "snap_vm-301-disk-0_speedtest_noram" created.
TASK OK
11.5s

Run 3
snapshotting 'drive-scsi0' (local-lvm:vm-800-disk-0)
  Logical volume "snap_vm-800-disk-0_speedtest_noram" created.
TASK OK
10.8s


