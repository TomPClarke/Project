from queue import Queue
from Component import Component


class Port():
    def __init__(self):
        self.direction = "FREE"
        self.data = Queue()
        self.landing_port = -1
        self.holding = False


class Router(Component):
    def __init__(self,name):
        self.data = Queue()
        self.name = name
        self.holding = False
        self.direction = "FREE"
        self.ports = [Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port(),Port()]
        self.credits = [9999,9999,3,3,3,3,3,3,3,3]
        self.port_order = [1,3,5,7,9,2,4,6,8]
        self.routing = {'UP' : self, #rename to routing_table
                        'DOWN' : self,
                        'LEFT' : self,
                        'RIGHT' : self,
                        'SLAVE' : self}
    #rename to declare_routing_table
    def declare_table(self,UDLR,SLAVE = 0):
        self.routing["UP"] = UDLR[0]
        self.routing["DOWN"] = UDLR[1]
        self.routing["LEFT"] = UDLR[2]
        self.routing["RIGHT"] = UDLR[3]
        if(SLAVE != 0):
            self.routing["SLAVE"] = SLAVE


    def receive(self, flit, port = 0):
        if(self.ports[port].direction == "FREE"):
            if(flit in ["DOWN","LEFT","UP","RIGHT"]):
                self.ports[port].direction = flit
            else:
                self.ports[port].direction = "SLAVE"
            #Make this return an error if it doesnt get a header flit
            self.send_credit(port)
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

    def receive_credit(self, port_num = 0):
        self.credits[port_num]+= 1

    def send_credit(self, port_num):
        #Find out who's buffer we have freed
        if(port_num == 0 or port_num == 1):
            self.routing["SLAVE"].receive_credit((port_num))
        elif(port_num == 2 or port_num == 3):
            self.routing["DOWN"].receive_credit((port_num))
        elif(port_num == 4 or port_num == 5):
            self.routing["LEFT"].receive_credit((port_num))
        elif(port_num == 6 or port_num == 7):
            self.routing["UP"].receive_credit((port_num))
        elif(port_num == 8 or port_num == 9):
            self.routing["RIGHT"].receive_credit((port_num))

    def send(self):
        #if(self.name == "Rout0"):print(f"{self.name} :{self.credits} ")
        #if(self.name == "Rout1"):print(f"{self.name} :{self.credits} ")
        #if(self.name == "Rout3"):print(f"{self.name} :{self.credits} ")
        #if(self.name == "Rout5"):print(f"{self.name} :{self.credits} ")
        port_num = -1
        used_directions = []
        new_port_order_high = []
        new_port_order_low = []
        for port_num in self.port_order:
            port = self.ports[port_num]
            if(port.direction == "FREE" or port.data.empty() or port.holding):
                continue
            if(port.landing_port == -1):
                port.landing_port = self.find_landing_port(port.direction,(port_num % 2))
            if(port.direction in used_directions):
                continue
            if(port_num in [0,2,4,5,8]):
                new_port_order_low.append(port_num)
            elif(port_num in [1,3,5,7,9]):
                new_port_order_high.append(port_num)
            if(self.credits[port.landing_port] > 0):
                flit = port.data.get()
                self.credits[port.landing_port]-= 1
                used_directions.append(port.direction)
                self.routing[port.direction].receive(flit, port.landing_port)
                if(flit.startswith("FREE")):
                    if(port.data.empty()):
                        port.direction = "FREE"
                        port.landing_port = -1
                    else:
                        flit = port.data.get()
                        if(flit in ["DOWN","LEFT","UP","RIGHT"]):
                            port.direction = flit
                        else:
                            port.direction = "SLAVE"
                        port.landing_port = -1
                        self.send_credit(port_num)
                self.send_credit(port_num)
        for x in range(5):
            if((2 * x) not in new_port_order_low):
                new_port_order_low.append(2 *x)
            if(((2 * x) +  1) not in new_port_order_high):
                new_port_order_high.append(2 * x + 1)
        self.port_order = new_port_order_high + new_port_order_low 

