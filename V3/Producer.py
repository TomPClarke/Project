from End_Node import End_Node
import globals
class Producer(End_Node):
    def __init__(self,name):
        super().__init__(name)
        self.holding = False
        self.landing_port = -1
        self.credits = [3,3]
    #This gives the producer some data
    #Should rename these Consumer_Masters
    if(True):
        #------------------3x3 MESH----------------
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
        #------------------------------------------
        #------------------6x6 MESH----------------
    else:
        Consumer_Nearest_Router = {'Con0' : [1,5],
                                   'Con1' : [4,5],
                                   'Con2' : [1,4],
                                   'Con3' : [4,4],
                                   'Con4' : [0,3],
                                   'Con5' : [2,3],
                                   'Con6' : [3,3],
                                   'Con7' : [5,3],
                                   'Con8' : [1,2],
                                   'Con9' : [4,2],
                                   'Con10' : [1,1],
                                   'Con11' : [4,1],
                                   'Con12' : [0,0],
                                   'Con13' : [2,0],
                                   'Con14' : [3,0],
                                   'Con15' : [5,0],
        }
        #Why is this an array, why not just store your own location?
        Producer_Nearest_Router = {'Prod0' :  [0,5],
                                   'Prod1' :  [2,5],
                                   'Prod2' :  [3,5],
                                   'Prod3' :  [5,5],
                                   'Prod4' :  [0,4],
                                   'Prod5' :  [2,4],
                                   'Prod6' :  [3,4],
                                   'Prod7' :  [5,4],
                                   'Prod8' :  [1,3],
                                   'Prod9' :  [4,3],
                                   'Prod10' : [0,2],
                                   'Prod11' : [2,2],
                                   'Prod12' : [3,2],
                                   'Prod13' : [5,2],
                                   'Prod14' : [0,1],
                                   'Prod15' : [2,1],
                                   'Prod16' : [3,1],
                                   'Prod17' : [5,1],
                                   'Prod18' : [1,0],
                                   'Prod19' : [4,0],
    }
    
    #------------------------------------------
    
    
    #I will keep this for now,
    #But why Would a producer need to hold data ever?
    def hold_on(self):
        if(self.data.empty()):
            self.holding = False
        else:
            self.holding = False

    def produce_message(self, data, target, channel = 0):
        #Include the header
        path = self.find_path(target)
        self.data.put(channel)
        for x in path:
            self.data.put(x)
        #Include the data
        for x in data:
            self.data.put(x)
        #Include the tail
        self.data.put(f"FREE{str(globals.clock_tick)}")

    def receive(self, data, landingport):
        print(globals.packet_latencies)
        raise RuntimeError(f"{self.name} received {data} on port {str(landingport)}. (Clock Tick: {globals.clock_tick})")

    
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
                self.master.receive(flit,self.landing_port)
                if(flit.startswith("FREE")):
                    self.landing_port = -1

