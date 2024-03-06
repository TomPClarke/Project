## CLI SETTINGS

MAX_LINE_LENGTH = 128



from NODES import FM, Routers, Consumers, Producers
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
    #print(f"Port 1: {Routers[5].ports[0].data.queue}")
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
    #for x in Routers:
    #    for i in range(0,5):
    #        print(f"{x.name}'s Buffer on port {i + (clock_tick % 2)}: {list(x.ports[i+ (clock_tick % 2)].data.queue)}                  ")
    first_time = False
    time.sleep(0.1)

"""
We Have this:

        P2  C2  P0              
         |   |   |         
         8---1---2         
         |   |   |         
         7---O---3         
         |   |   |         
         6---5---4         
         |   |   |         
         C1  P1  C0     

But we want this:
      
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

FM("Rout0").declare_table(["Rout1","Rout5","Rout7","Rout3"],"Con3")
FM("Rout1").declare_table(["Rout1","Rout0","Rout8","Rout2"],"Con2")
FM("Rout2").declare_table(["Rout2","Rout3","Rout1","Rout2"],)
FM("Rout3").declare_table(["Rout2","Rout4","Rout0","Rout3"],)
FM("Rout4").declare_table(["Rout3","Rout4","Rout5","Rout4"],"Con0")
FM("Rout5").declare_table(["Rout0","Rout5","Rout6","Rout4"],)
FM("Rout6").declare_table(["Rout7","Rout6","Rout6","Rout5"],"Con1")
FM("Rout7").declare_table(["Rout8","Rout6","Rout7","Rout0"],)
FM("Rout8").declare_table(["Rout8","Rout7","Rout8","Rout1"])

#I think this is probably redudant, code above could handle masters and slaves
FM("Con0").declare_master("Rout4")
FM("Con1").declare_master("Rout6")
FM("Con2").declare_master("Rout1")
FM("Con3").declare_master("Rout0")

FM("Prod0").declare_master("Rout2")
FM("Prod1").declare_master("Rout5")
FM("Prod2").declare_master("Rout8")
FM("Prod3").declare_master("Rout7")
FM("Prod4").declare_master("Rout3")

update_UI()
###### Task Scheduler ######
def Run_task_scheduler():
    global clock_tick
    if(clock_tick % 5 == 2):
        FM("Prod4").produce_message(['H','I',],"Con3",1)
    if(clock_tick % 8 == 4):
        FM("Prod0").produce_message(['O','K'],"Con1",1)
    if(clock_tick % 15 == 0):
        random_tasks()
    if(clock_tick % 40 == 0):
        for x in Consumers:
            pass#x.Empty()

def random_tasks():
    string = "Con"
    string += str(random.randint(0,3))
    random.choice(Producers[1:3]).produce_message(['W','O','R','M'],string,random.randint(0,1))

#"""
################ THE CLOCK ################
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
