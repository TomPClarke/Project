from NODES import Routers, Consumers, Producers
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
