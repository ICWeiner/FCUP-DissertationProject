# Celery version (Flask + Celery based) POST-IO FIX

-AFTER IO CLEANUP
(only 2 cores)
VM Cloning process time: 44.905797 seconds

(only 8 cores)
VM Cloning process time: 33.338705 seconds

VM Cloning process time: 30.461152 seconds

(cloning and deleting with celery)

for 1 VM:
Template VM creation time: 34.415269 seconds
VM Cloning process time: 0.383235 seconds
VM deleting process time: 2.156981 seconds
Final CPU usage: 16.7%

Template VM creation time: 34.181023 seconds
VM Cloning process time: 0.380662 seconds
VM deleting process time: 1.154254 seconds
Final CPU usage: 17.1%

Template VM creation time: 34.204050 seconds
VM Cloning process time: 0.369326 seconds
VM deleting process time: 3.156202 seconds
Final CPU usage: 17.5%

34.266781
0.377741
2.155812
17.1

for 10 VMs:
Template VM creation time: 34.469319 seconds
VM Cloning process time: 1.551154 seconds
VM deleting process time: 2.094884 seconds
Final CPU usage: 15.9%

Template VM creation time: 34.203889 seconds
VM Cloning process time: 1.630142 seconds
VM deleting process time: 0.080990 seconds
Final CPU usage: 15.7%

Template VM creation time: 34.207585 seconds
VM Cloning process time: 1.516021 seconds
VM deleting process time: 0.083569 seconds
Final CPU usage: 16.1%

34.293598
1.565772
0.753148
15.9


for 20 VMs:
Template VM creation time: 34.426887 seconds
VM Cloning process time: 3.116554 seconds
VM deleting process time: 0.150268 seconds
Final CPU usage: 16.1%

Template VM creation time: 34.223055 seconds
VM Cloning process time: 3.868297 seconds
VM deleting process time: 1.176935 seconds
Final CPU usage: 13.4%

Template VM creation time: 34.390095 seconds
VM Cloning process time: 2.876733 seconds
VM deleting process time: 0.173194 seconds
Final CPU usage: 17.9%

34.346679
3.287195
0.500132
15.8

(OUTLIER)
Template VM creation time: 34.221422 seconds
VM Cloning process time: 17.994122 seconds
VM deleting process time: 0.165361 seconds
Final CPU usage: 3.1%


for 100 VMs:
Template VM creation time: 34.433466 seconds
VM Cloning process time: 14.243919 seconds
VM deleting process time: 5.068589 seconds
Final CPU usage: 20.4%

Template VM creation time: 34.194064 seconds
VM Cloning process time: 14.298767 seconds
VM deleting process time: 3.088729 seconds
Final CPU usage: 20.5%

Template VM creation time: 34.224277 seconds
VM Cloning process time: 14.693533 seconds
VM deleting process time: 1.095004 seconds
Final CPU usage: 20.0%

34.283936
14.412073
3.084107
20.3


for 200 VMs:
Template VM creation time: 34.412016 seconds
VM Cloning process time: 31.206578 seconds
VM deleting process time: 6.058494 seconds
Final CPU usage: 21.6%

Template VM creation time: 38.699065 seconds
VM Cloning process time: 33.528651 seconds
VM deleting process time: 4.139870 seconds
Final CPU usage: 21.8%

Template VM creation time: 39.222109 seconds
VM Cloning process time: 34.550468 seconds
VM deleting process time: 3.342061 seconds
Final CPU usage: 23.3%

37.444397
33.095232
4.513475
22.2(3)

total template average
34.639572