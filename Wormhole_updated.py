class Node:
    def __init__(self,name,buffer_size = 5):
        self.name = name
        self.buffer = []
        self.neighbours = []
        self.max_buffer_size = buffer_size
    def give_neighbours(self, neighbours):
        toadd = []
        for x in neighbours:
            toadd.append(FM(x))
        self.neighbours = toadd
    def print_buffer(self):
        print(f"{self.name}: {self.buffer}")

class Consumer(Node):
    def recieve(self, packet):
        if(False):
            #Refuse the packet
            #Right now, this will never refuse a packet
            #But later on it should refuse packets
            #That aren't meant for it etc..
            print("I can't take that")
        else:
            self.buffer.append(packet)
        
class Producer(Node):
    def load_buffer(self,data):
        #data should be an array
        for x in data:
            if(len(self.buffer) < self.max_buffer_size):
                self.buffer.append(x)
            else:
                print(f"{self.name}: Buffer is full.")
                return
    def send(self,target):
        #Find the target
        for n in self.neighbours:
            if(n.name == target):
                if(not self.buffer):
                    print(f"{self.name} has empty buffer")
                    return
                print(self.name + " sending packet to: " + target)
                n.recieve(self.buffer.pop())
                return
        print(self.name + " has no neighbour: " + target)

class Router(Consumer, Producer):  
    pass

#Create Nodes

Consumers = [Consumer("Con0"),Consumer("Con1"),Consumer("Con2")]
Producers = [Producer("Prod0"),Producer("Prod1"),Producer("Prod2")]
Routers = [Router("Rout0"),Router("Rout1"),Router("Rout2"),Router("Rout3"),
           Router("Rout4"),Router("Rout5"),Router("Rout6"),Router("Rout7"), Router("Rout8")]
Modules = [Consumers,Producers,Routers]
#Used for resolving module names
def FM(name):
    global Consumers, Producers, Routers
    if(name[0].upper() == "R"):
        for x in Routers:
            if(x.name == name):
                return x
    elif(name[0].upper() == "P"):
        for x in Producers:
            if(x.name == name):
                return x
    elif(name[0].upper() == "C"):
        for x in Consumers:
            if(x.name == name):
                return x
    raise Exception(f"No module called {name}")



#           Allocate Neighbours / Create Structure

#Tell each router their neighbour
FM("Rout0").give_neighbours(["Rout1","Rout2","Rout3","Rout4","Rout5","Rout6","Rout7","Rout8"])
FM("Rout1").give_neighbours(["Con2","Rout2","Rout8","Rout0"])
FM("Rout2").give_neighbours(["Rout1","Rout3","Prod0","Rout0"])
FM("Rout3").give_neighbours(["Rout2","Rout4","Rout0"])
FM("Rout4").give_neighbours(["Rout3","Rout5","Con0","Rout0"])
FM("Rout5").give_neighbours(["Rout0","Prod1","Rout6","Rout4"])
FM("Rout6").give_neighbours(["Rout0","Rout7","Rout5","Con1"])
FM("Rout7").give_neighbours(["Rout0","Rout8","Rout6"])
FM("Rout8").give_neighbours(["Prod2","Rout1","Rout7","Rout0"])
FM("Con0").give_neighbours(["Rout4"])
FM("Con1").give_neighbours(["Rout6"])
FM("Con2").give_neighbours(["Rout1"])
FM("Prod0").give_neighbours(["Rout2"])
FM("Prod1").give_neighbours(["Rout5"])
FM("Prod2").give_neighbours(["Rout8"])

#For now each router is going the whole network

nodes = []





"""
FM("Con0").give_neighbours([Routers[2]])
Producers[0].give_neighbours([Routers[0]])
Routers[0].give_neighbours([Routers[1],Producers[0],Routers[3]])
Routers[1].give_neighbours([Routers[0],Routers[2]])
Routers[2].give_neighbours([Consumers[0],Routers[3],Routers[1]])
Routers[3].give_neighbours([Routers[2],Routers[0]])
"""
Producers[0].load_buffer([1,2,3])
Producers[0].send("Rout0")
Routers[0].send("Rout1")
Routers[1].send("Rout2")
Routers[2].send("Con0")
