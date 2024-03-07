from End_Node import End_Node
class Consumer(End_Node):
    def recieve(self, data, port):
        if(port == 1):
            return
        self.data.put(data)
    def Empty(self):
        while(not self.data.empty()):
            self.data.get()
        return