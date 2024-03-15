from queue import Queue

class Port():
    def __init__(self):
        self.direction = "FREE"
        self.data = Queue()
        self.landing_port = -1
        self.holding = False


class Router():
    def __init__(self,name):
        self.data = Queue()
        self.name = name
        self.holding = False
        self.direction = "FREE"
        self.ports = [Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port()]
        self.routing = {'UP' : self,
                        'DOWN' : self,
                        'LEFT' : self,
                        'RIGHT' : self,
                        'SLAVE' : self}
    def declare_table(self,UDLR,SLAVE = 0):
        self.routing["UP"] = UDLR[0]
        self.routing["DOWN"] = UDLR[1]
        self.routing["LEFT"] = UDLR[2]
        self.routing["RIGHT"] = UDLR[3]
        if(SLAVE != 0):
            self.routing["SLAVE"] = SLAVE


    def recieve(self, flit, port = 0):
        if(self.ports[port].direction == "FREE"):
            if(flit in ["DOWN","LEFT","UP","RIGHT"]):
                self.ports[port].direction = flit
            else:
                self.ports[port].direction = "SLAVE"
        else:
            self.ports[port].data.put(flit)
    #Every router is told: 
    #If you haven't got anything at the beginning of the clock cycle,
    #Do not send anything this clock cycle, to keep the illusion of synchronisation
    def hold_on(self):
        for port in self.ports:
            if(port.data.empty()):
                port.holding = True
            else:
                port.holding = False

    def find_landing_port(self, direction,channel = 0):
        if(direction == "SLAVE"): return (0 + channel)
        if(direction == "UP"): return (2 + channel) # Bottoms ports are 2 & 3    
        elif(direction == "RIGHT"): return (4 + channel) # Left ports are 4 & 5       
        elif(direction == "DOWN"): return (6 + channel) # Up ports are 6 & 7
        elif(direction == "LEFT"): return (8 + channel) # Right ports are 8 & 9


    def send(self):
        port_num = -1
        for port in self.ports:
            port_num += 1
            if(port.direction == "FREE" or port.data.empty() or port.holding):
                continue
            if(port.landing_port == -1):
                if(port.direction == "SLAVE"): pass
                else : 
                    port.landing_port = self.find_landing_port(port.direction,(port_num % 2))
            flit = port.data.get()
            self.routing[port.direction].recieve(flit, port.landing_port)
            if(flit == "FREE"): 
                port.direction = "FREE"
                port.landing_port = -1        
