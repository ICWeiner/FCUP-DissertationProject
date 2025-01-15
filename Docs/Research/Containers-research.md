# Containers

Pros:

Containers allow host to directly access files.

Pass throught just works

Memory efficient


Cons:

Since containers run directly on the host, can lead to security concerns under exteme conditions

Low memory can lead to processes being killed in container or host

Live migrations not possible

Potential for kernel panic caused by container


Overall, seems like containers might not be the best choice for this problem
UPDATE: With GNS3-Web containers seem like a great alternative than using full VMs, just as long as users cant access them directly and only by the GNS3-Web interface
UPDATE UPDATE: The only way to run linux instances in containers is by passing through /dev/kvm which is suboptimal as it can
lead to big security vulnerabilities.
Due to this the ideia has been shelved for now atleast