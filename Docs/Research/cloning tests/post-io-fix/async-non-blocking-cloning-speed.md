# Async version (FastAPI-asyncio based) POST-IO FIX
5 concurrent request maximum

for 1 VM:
Template VM creation time: 32.277591 seconds
VM Cloning process time: 0.332573 seconds
Final CPU usage: 7.2%
VM deletion process time: 0.023404 seconds

Template VM creation time: 32.137275 seconds
VM Cloning process time: 0.318698 seconds
Final CPU usage: 8.6%
VM deletion process time: 0.023158 seconds

Template VM creation time: 32.247606 seconds
VM Cloning process time: 0.341546 seconds
Final CPU usage: 7.7%
VM deletion process time: 0.024713 seconds

32.220824
0.330939
0.023758
7.8(3)


for 10 VMs:
Template VM creation time: 32.213745 seconds
VM Cloning process time: 1.452375 seconds
Final CPU usage: 14.7%
VM deletion process time: 0.062086 seconds

Template VM creation time: 32.216619 seconds
VM Cloning process time: 1.428091 seconds
Final CPU usage: 14.7%
VM deletion process time: 0.066792 seconds

Template VM creation time: 32.155424 seconds
VM Cloning process time: 1.424305 seconds
Final CPU usage: 15%
VM deletion process time: 0.058975 seconds

32.195263
1.434924
0.062618
14.8



for 20 VMs:
Template VM creation time: 32.249668 seconds
VM Cloning process time: 2.820377 seconds
Final CPU usage: 16.8%
VM deletion process time: 0.140582 seconds

Template VM creation time: 32.165283 seconds
VM Cloning process time: 2.799981 seconds
Final CPU usage: 16.8%
VM deletion process time: 0.133163 seconds

Template VM creation time: 32.138648 seconds
VM Cloning process time: 2.996165 seconds
Final CPU usage: 15.8%
VM deletion process time: 0.130607 seconds

32.184533
2.872174
0.134784
16.4(6)


for 100 VMs:
Template VM creation time: 32.169642 seconds
VM Cloning process time: 14.893198 seconds
Final CPU usage: 18.8% 
VM deletion process time: 1.021420 seconds

Template VM creation time: 32.208805 seconds
VM Cloning process time: 14.716172 seconds
Final CPU usage: 19.2% 
VM deletion process time: 1.013605 seconds

Template VM creation time: 32.235647 seconds
VM Cloning process time: 14.888447 seconds
Final CPU usage: 19.2%
VM deletion process time: 1.033826 seconds

32.204698
14.832606
1.022950
19.0(6)

for 200 VMs:
Template VM creation time: 32.203489 seconds
VM Cloning process time: 31.535956 seconds
Final CPU usage: 20.9%
VM deletion process time: 2.893278 seconds

Template VM creation time: 32.156690 seconds
VM Cloning process time: 30.489418 seconds
Final CPU usage: 21.5%
VM deletion process time: 2.850222 seconds

Template VM creation time: 32.183706 seconds
VM Cloning process time: 31.735772 seconds
Final CPU usage: 20.7%
VM deletion process time: 2.872980 seconds

32.181295
31.253715
2.872160
21.0(3)

total template average
32.202087