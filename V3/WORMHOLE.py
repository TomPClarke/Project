## CLI SETTINGS

MAX_LINE_LENGTH = 128


from Tools import FM
from NODES import Routers, Consumers, Producers
import keyboard, time, random


#How are you going to test this code?

first_time = True
clock_tick = 0
def update_UI():
    #When I make a GUI, this is just going to return a JSON of the status of the nodes.
    global first_time, clock_tick
    if not(first_time):
        print('\033[F' * (6 + 5))
    print(f"Clock Tick: {clock_tick}")
    for x in Consumers:
        Buffer_string = (f"{x.name}'s Buffer: {list(x.data.queue)}")
        if(len(Buffer_string) > MAX_LINE_LENGTH):
            Buffer_string = Buffer_string[0:MAX_LINE_LENGTH]
            Buffer_string= Buffer_string[:-3] + "..."
            x.data.get()
        elif(len(Buffer_string) < MAX_LINE_LENGTH):
            Buffer_string = Buffer_string + " " * (MAX_LINE_LENGTH - len(Buffer_string))
        print(Buffer_string)
    for x in Producers:
        Buffer_string = (f"{x.name}'s Buffer: {list(x.data.queue)}")
        if(len(Buffer_string) > MAX_LINE_LENGTH):
            Buffer_string = Buffer_string[0:MAX_LINE_LENGTH]
            Buffer_string= Buffer_string[:-3] + "..."
        elif(len(Buffer_string) < MAX_LINE_LENGTH):
            Buffer_string = Buffer_string + " " * (MAX_LINE_LENGTH - len(Buffer_string))
        print(Buffer_string)
    first_time = False
    time.sleep(0.1)


"""
Chip Layout:
         8---1---2         
         |   |   |         
         7---O---3         
         |   |   |           
         6---5---4

        P2--C2--P0         
         |   |   |         
        P3--C3--P4         
         |   |   |           
        C1--P1--C0                  
"""

FM("Rout0").declare_table([FM("Rout1"),FM("Rout5"),FM("Rout7"),FM("Rout3")  ],FM("Con3"))
FM("Rout1").declare_table([FM("Rout1"),FM("Rout0"),FM("Rout8"),FM("Rout2")  ],FM("Con2"))
FM("Rout2").declare_table([FM("Rout2"),FM("Rout3"),FM("Rout1"),FM("Rout2")  ],)
FM("Rout3").declare_table([FM("Rout2"),FM("Rout4"),FM("Rout0"),FM("Rout3")  ],)
FM("Rout4").declare_table([FM("Rout3"),FM("Rout4"),FM("Rout5"),FM("Rout4")  ],FM("Con0"))
FM("Rout5").declare_table([FM("Rout0"),FM("Rout5"),FM("Rout6"),FM("Rout4")  ],)
FM("Rout6").declare_table([FM("Rout7"),FM("Rout6"),FM("Rout6"),FM("Rout5")  ],FM("Con1"))
FM("Rout7").declare_table([FM("Rout8"),FM("Rout6"),FM("Rout7"),FM("Rout0")  ],)
FM("Rout8").declare_table([FM("Rout8"),FM("Rout7"),FM("Rout8"),FM("Rout1")  ])

#I think this is probably redudant, code above could handle masters and slaves
FM("Con0").declare_master(FM("Rout4"))
FM("Con1").declare_master(FM("Rout6"))
FM("Con2").declare_master(FM("Rout1"))
FM("Con3").declare_master(FM("Rout0"))

FM("Prod0").declare_master(FM("Rout2"))
FM("Prod1").declare_master(FM("Rout5"))
FM("Prod2").declare_master(FM("Rout8"))
FM("Prod3").declare_master(FM("Rout7"))
FM("Prod4").declare_master(FM("Rout3"))

update_UI()
###### Task Scheduler ######
def Run_task_scheduler():
    global clock_tick
    if(clock_tick % 5 == 2):
        FM("Prod0").produce_message(['red','red',],"Con1",1)
    if(clock_tick % 8 == 4):
        FM("Prod3").produce_message(['yellow','yellow'],"Con2",1)
    if(clock_tick % 15 == 0):
        random_tasks()
    if(clock_tick % 40 == 0):
        for x in Consumers:
            pass#x.Empty()



def random_tasks():
    string = "Con"
    string += str(random.randint(0,3))
    random.choice(Producers[1:3]).produce_message(['orange','orange','orange','orange'],string,1)

#"""
################ THE CLOCK ################

if __name__ == "__main__":    
    def on_spacebar(event):
        global clock_tick
        if event.name == 'space':
            Run_task_scheduler()
            clock_tick += 1
            for x in Routers:
                x.hold_on()
            for x in Producers:
                x.hold_on()
            for x in Routers:
                x.send()
            for x in Producers:
                x.send()
            update_UI()
    keyboard.on_press_key('space', on_spacebar)
    keyboard.wait('esc')

#I get called every time space is pressed
def getJSONGUI():
    global clock_tick
    Run_task_scheduler()
    clock_tick+= 1
    for x in Routers:
        x.hold_on()
    for x in Producers:
        x.hold_on()
    for x in Routers:
        x.send()
    for x in Producers:
        x.send()

    data = {}    
    routers = {}
    for router in Routers:
        routers[f"{router.name}"] = {}
        port_id = 0 
        for port in router.ports:
            routers[f"{router.name}"][f"port_{str(port_id)}"] = list(port.data.queue)
            port_id+= 1
    data['routers'] = routers
    return data


"""
while(True):
        time.sleep(0.2)
        Run_task_scheduler()
        clock_tick += 1
        for x in Routers:
            x.hold_on()
        for x in Producers:
            x.hold_on()
        for x in Routers:
            x.send()
        for x in Producers:
            x.send()
        update_UI()
#"""
