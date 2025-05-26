# Celery version (Flask + Celery based) POST-IO FIX

-AFTER IO CLEANUP
(only 2 cores)
VM Cloning process time: 44.905797 seconds

(only 8 cores)
VM Cloning process time: 33.338705 seconds

VM Cloning process time: 30.461152 seconds

(Only cloning is done with celery)

for 1 VM:
Template VM creation time: 34.385668 seconds
VM Cloning process time: 0.383235 seconds
VM deleting process time: 0.026182 seconds
Final CPU usage: 7.9%

Template VM creation time: 34.233205 seconds
VM Cloning process time: 0.380662 seconds
VM deleting process time: 0.027572 seconds
Final CPU usage: 7.3%

Template VM creation time: 34.210480 seconds
VM Cloning process time: 0.369326 seconds
VM deleting process time: 0.026037 seconds
Final CPU usage: 7.8%


for 10 VMs:
Template VM creation time: 45.636559 seconds
VM Cloning process time: 1.738983 seconds
VM deleting process time: 0.156389 seconds
Final CPU usage: 14.7%

Template VM creation time: 45.391426 seconds
VM Cloning process time: 1.772058 seconds
VM deleting process time: 0.154500 seconds
Final CPU usage: 14.1%

Template VM creation time: 34.171716 seconds
VM Cloning process time: 1.684034 seconds
VM deleting process time: 0.161085 seconds
Final CPU usage: 15.0%


for 20 VMs:
Template VM creation time: 34.396233 seconds
VM Cloning process time: 3.078449 seconds
VM deleting process time: 0.306715 seconds
Final CPU usage: 16.9%

Template VM creation time: 34.209975 seconds
VM Cloning process time: 2.994721 seconds
VM deleting process time: 0.322884 seconds
Final CPU usage: 18.6%

Template VM creation time: 34.167834 seconds
VM Cloning process time: 2.808956 seconds
VM deleting process time: 0.316418 seconds
Final CPU usage: 18.1%


for 100 VMs:
Template VM creation time: 45.592831 seconds
VM Cloning process time: 14.891445 seconds
VM deleting process time: 1.837723 seconds
Final CPU usage: 20.2%

Template VM creation time: 45.406052 seconds
VM Cloning process time: 14.884476 seconds
VM deleting process time: 1.812042 seconds
Final CPU usage: 20.0%

Template VM creation time: 34.190182 seconds
VM Cloning process time: 15.088231 seconds
VM deleting process time: 1.788040 seconds
Final CPU usage: 20.0%


for 200 VMs:
Template VM creation time: 34.421460 seconds
VM Cloning process time: 31.571591 seconds
VM deleting process time: 4.390037 seconds
Final CPU usage: 21.6%

Template VM creation time: 34.176918 seconds
VM Cloning process time: 30.073782 seconds
VM deleting process time: 4.394367 seconds
Final CPU usage: 22.2%

Template VM creation time: 45.593894 seconds
VM Cloning process time: 30.354872 seconds
VM deleting process time: 4.442125 seconds
Final CPU usage: 22.1%


(cloning and deleting with celery)

for 1 VM:
Template VM creation time: 34.415269 seconds
VM Cloning process time: 3.037243 seconds
VM deleting process time: 2.156981 seconds
Final CPU usage: 16.7%

Template VM creation time: 34.181023 seconds
VM Cloning process time: 2.989891 seconds
VM deleting process time: 1.154254 seconds
Final CPU usage: 17.1%

Template VM creation time: 34.204050 seconds
VM Cloning process time: 3.007208 seconds
VM deleting process time: 3.156202 seconds
Final CPU usage: 17.5%

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

Refined code 

Template VM creation time: 29.330032 seconds
VM Cloning process time: 29.852100 seconds
VM deleting process time: 3.089752 seconds
Final CPU usage: 21.9%

Template VM creation time: 29.352438 seconds
VM Cloning process time: 29.641674 seconds
VM deleting process time: 3.084086 seconds
Final CPU usage: 22.2%

Template VM creation time: 29.342889 seconds
VM Cloning process time: 29.532992 seconds
VM deleting process time: 2.936237 seconds
Final CPU usage: 22.0%

