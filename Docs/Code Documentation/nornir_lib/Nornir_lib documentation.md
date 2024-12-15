# Nornir_lib - System for pratical evaluation of network administration 

This library is responsible for connecting to the various GNS3 devices in a given topology, inputing commands, retrieving and analyzing output to evaluate success or failure.

It is comprised of 2 folders:

- ```modules```: Which is documented in [Modules.md](Modules.md)
- ```utils```: Contains several useful useful functions that interface with GNS3

It makes use of the following files found in the ```app``` folder:
- ```config.yaml```: Contains the location of ```host_file``` , ```group_file``` and ```defaults_file```. Also contains the configuration for the nornir ```runner```.
- ```host_file```: Contains info on the VMs/containers that host a GNS3 server. It is required to include atleast the IP address, the group they belong to ('linux' should be used in 99% of cases) and a valid username and password, in clear text.
- ```group_file```: Contains the default configuration of the various groups. Note :fast_cli must remain set to ```false``` or tests might not work properly
- ```defaults_file```: Currently unused
