from End_Node import End_Node
from globals import clock_tick as clock_tick
class Producer(End_Node):
    def __init__(self,name):
        super().__init__(name)
        self.holding = False
        self.landing_port = -1
        self.credits = [3,3]
    #This gives the producer some data
    #Should rename these Consumer_Masters
    Consumer_Nearest_Router = {'Con0' : [2,0],
                               'Con1' : [0,0],
                               'Con2' : [1,2],
                               'Con3' : [1,1]}
    
    #Why is this an array, why not just store your own location?
    Producer_Nearest_Router = {'Prod0' : [2,2],
                               'Prod1' : [1,0],
                               'Prod2' : [0,2],
                               'Prod3' : [0,1],
                               'Prod4' : [2,1]}
    
    #I will keep this for now,
    #But why Would a producer need to hold data ever?
    def hold_on(self):
        if(self.data.empty()):
            self.holding = False
        else:
            self.holding = False

    def produce_message(self, data, target,clock_tick, channel = 0):
        #Include the header
        path = self.find_path(target)
        self.data.put(channel)
        for x in path:
            self.data.put(x)
        #Include the data
        for x in data:
            self.data.put(x)
        #Include the tail
        self.data.put(f"FREE{str(clock_tick)}")
    def recieve(self, data, landingport):
        print(f"{self.name}: I received something. This is an error")

    
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
    
    def receive_credit(self, channel):
        self.credits[channel]+= 1
    
    def send(self):
        if(self.data.empty()):
            return
        if(self.holding == False):
            if(self.landing_port == -1):
                self.landing_port = int(self.data.get())
            if(self.credits[self.landing_port] > 0):
                flit = self.data.get()
                self.credits[self.landing_port]-= 1
                self.master.recieve(flit,self.landing_port)
                if(flit.startswith("FREE")):
                    self.landing_port = -1

