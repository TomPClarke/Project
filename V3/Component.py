from abc import ABC, abstractmethod

class Component(ABC):
    def send(self):
        print("I am meant to send")
    #def receive(self):
    #    print("I am meant to receive")
    def receive_credit(self,port):
        print("I am meant to receive credits")
    def send_credit(self,port):
        print("I am meant to send credits")