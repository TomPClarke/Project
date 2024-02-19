from queue import Queue
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



class End_Node:
    def __init__(self,name):
        self.name = name
        self.master = self
        self.data = Queue()
    def clear(self):
        while(self.data.empty() == False):
            self.data.get()
    def declare_master(self, master_name):
        self.master = FM(master_name)

class Consumer(End_Node):
    def recieve(self, data, port = 0):
        self.data.put(data)
    #This shouldn't be here
    def first_open_port(self):
        return 0

class Producer(End_Node):
    def __init__(self,name):
        super().__init__(name)
        self.holding = False
        self.current_port = -1
    #This gives the producer some data
    Consumer_Nearest_Router = {'Con0' : [2,0],
                               'Con1' : [0,0],
                               'Con2' : [1,2]}
    
    Producer_Nearest_Router = {'Prod0' : [2,2],
                               'Prod1' : [1,0],
                               'Prod2' : [0,2]}
    
    #I will keep this for now,
    #But why Would a producer need to hold data ever?
    def hold_on(self):
        if(self.data.empty()):
            self.holding = False
        else:
            self.holding = False

    def produce_message(self, data, target):
        #Include the header
        path = self.find_path(target)
        for x in path:
            self.data.put(x)
        #Include the data
        for x in data:
            self.data.put(x)
        #Include the tail
        self.data.put("FREE")
        
    
    def find_path(self,dest):
        path =[]
        current = self.Producer_Nearest_Router[self.name].copy()
        target = self.Consumer_Nearest_Router[dest].copy()
        #sort out X
        while(current[0] != target[0]):
            if(current[0] > target[0]):
                current[0] -= 1
                path.append("LEFT")
            elif(current[0] < target[0]):
                current[0] += 1
                path.append("RIGHT")
        #sort out Y
        while(current[1] != target[1]):
            if(current[1] > target[1]):
                current[1] -= 1
                path.append("DOWN")
            elif(current[1] < target[1]):
                current[1] += 1
                path.append("UP")
        path.append(dest)
        return path
    
    def send(self):
        if(self.data.empty()):
            return
        if(self.holding == False):
            if(self.current_port == -1):
                self.current_port = self.master.first_open_port()
            flit = self.data.get()
            self.master.recieve(flit)
            if(flit == "FREE"):
                self.current_port = -1

class Port():
    def __init__(self):
        self.direction = "FREE"
        self.data = Queue()
        self.outbound_port = -1
        self.holding = False


class Router():
    def __init__(self,name):
        self.data = Queue()
        self.name = name
        self.holding = False
        self.direction = "FREE"
        self.ports = [Port(),Port(),Port(),Port()]
        self.routing = {'UP' : self,
                        'DOWN' : self,
                        'LEFT' : self,
                        'RIGHT' : self,
                        'SLAVE' : self} #Might Rename this to Local
    def declare_table(self,UDLR,SLAVE = 0):
        self.routing["UP"] = FM(UDLR[0])
        self.routing["DOWN"] = FM(UDLR[1])
        self.routing["LEFT"] = FM(UDLR[2])
        self.routing["RIGHT"] = FM(UDLR[3])
        if(SLAVE != 0):
            self.routing["SLAVE"] = FM(SLAVE)

    def first_open_port(self):
        for x in range(0,4):
            if(self.ports[x].direction == "FREE"):
                #If two Routers ask me for my first port.
                #Will I give them a different port.
                return x


    def recieve(self, flit, port = 0):
        if(self.ports[port].direction == "FREE"):
            if(flit in ["DOWN","LEFT","UP","RIGHT"]):
                self.ports[port].direction = flit
            else:
                self.ports[port].direction = "SLAVE"
        else:
            self.ports[port].data.put(flit)
        """
        if(self.direction == "FREE"):
            if(flit in ["DOWN","LEFT","UP","RIGHT"]):
                self.direction = flit
            else:
                self.direction = "SLAVE"
                pass
        else:
            self.data.put(flit)
        """
    #Every router is told: 
    #If you haven't got anything at the beginning of the clock cycle,
    #Do not send anything this clock cycle, to keep the illusion of synchronisation
    def hold_on(self):
        for port in self.ports:
            if(port.data.empty()):
                port.holding = True
            else:
                port.holding = False

    def send(self):
        """
        if(self.direction == "FREE" or self.data.empty() or self.holding):
            #If we don't have no direction or no data
            #Don't do anything
            return
        #Otherwise
        flit = self.data.get()
        self.routing[self.direction].recieve(flit)
        if(flit == "FREE"): self.direction = "FREE"
        """
        #return
        for port in self.ports:
            if(port.direction == "FREE" or port.data.empty() or port.holding):
                continue
            if(port.outbound_port == -1):
                if(port.direction == "SLAVE"): pass
                else : port.outbound_port = self.routing[port.direction].first_open_port()
            flit = port.data.get()
            self.routing[port.direction].recieve(flit, port.outbound_port)
            if(flit == "FREE"): 
                port.direction = "FREE"
                port.outbound_port = -1        


Consumers = [Consumer("Con0"),Consumer("Con1"),Consumer("Con2")]
Producers = [Producer("Prod0"),Producer("Prod1"),Producer("Prod2")]
Routers = [Router("Rout0"),Router("Rout1"),Router("Rout2"),Router("Rout3"),
           Router("Rout4"),Router("Rout5"),Router("Rout6"),Router("Rout7"), Router("Rout8")]