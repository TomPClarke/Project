from Consumer import Consumer
from Producer import Producer
from Router import Router
"""

######### Consumers, Producers & End Nodes #########
There are End_Nodes
Consumers and Producers are End_Nodes
An End_Node has a name, a master and a buffer.
Consumers can only recieve data.
Producers can send data, they can also path-find.

#### Routers ####
A router has a name, a routing table, a direction and a slave.
The direction is the entry in the routing to which the router will send all flits




"""
Consumers = [Consumer("Con0"),Consumer("Con1"),Consumer("Con2"),Consumer("Con3")]
Producers = [Producer("Prod0"),Producer("Prod1"),Producer("Prod2"),Producer("Prod3"),Producer("Prod4")]
Routers = [Router("Rout0"),Router("Rout1"),Router("Rout2"),Router("Rout3"),
           Router("Rout4"),Router("Rout5"),Router("Rout6"),Router("Rout7"), Router("Rout8")]