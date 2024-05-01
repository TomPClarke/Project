from End_Node import End_Node
import globals
class Consumer(End_Node):
    def receive(self, data, port):
        if(data.startswith("FREE")):
            globals.packet_latencies += f"{int(globals.clock_tick) - int(data[4::])},"
            print(f"{int(globals.clock_tick) - int(data[4::])},",end= "")
        if(port == 1):
            #self.master.receive_credit(port)
            return
        self.data.put(data)
        #self.master.receive_credit(port)
    def Empty(self):
        while(not self.data.empty()):
            self.data.get()
        return