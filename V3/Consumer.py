from End_Node import End_Node
import globals
class Consumer(End_Node):
    def recieve(self, data, port):
        if(data.startswith("FREE")):
            print(f"{self.name} received packet. Latency = {int(globals.clock_tick) - int(data[4::])}")
        if(port == 1):
            #self.master.receive_credit(port)
            return
        self.data.put(data)
        #self.master.receive_credit(port)
    def Empty(self):
        while(not self.data.empty()):
            self.data.get()
        return