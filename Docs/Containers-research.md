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