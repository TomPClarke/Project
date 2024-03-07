from queue import Queue
class End_Node:
    def __init__(self,name):
        self.name = name
        self.master = self
        self.data = Queue()
    def clear(self):
        while(self.data.empty() == False):
            self.data.get()
    def declare_master(self, master):
        self.master = master