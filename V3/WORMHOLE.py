## CLI SETTINGS

MAX_LINE_LENGTH = 128

first_time = True
clock_tick = 0
import globals
from Tools import FM
from NODES import Routers, Consumers, Producers
import keyboard, time, random, json


#How are you going to test this code?

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


##--------------------------------3x3 MESH------------------------------------------------
if(True):
    FM("Rout0").declare_table([FM("Rout1"),FM("Rout5"),FM("Rout7"),FM("Rout3")  ],FM("Con3"))
    FM("Rout1").declare_table([FM("Rout1"),FM("Rout0"),FM("Rout8"),FM("Rout2")  ],FM("Con2"))
    FM("Rout2").declare_table([FM("Rout2"),FM("Rout3"),FM("Rout1"),FM("Rout2")  ],FM("Prod0"))
    FM("Rout3").declare_table([FM("Rout2"),FM("Rout4"),FM("Rout0"),FM("Rout3")  ],FM("Prod4"))
    FM("Rout4").declare_table([FM("Rout3"),FM("Rout4"),FM("Rout5"),FM("Rout4")  ],FM("Con0"))
    FM("Rout5").declare_table([FM("Rout0"),FM("Rout5"),FM("Rout6"),FM("Rout4")  ],FM("Prod1"))
    FM("Rout6").declare_table([FM("Rout7"),FM("Rout6"),FM("Rout6"),FM("Rout5")  ],FM("Con1"))
    FM("Rout7").declare_table([FM("Rout8"),FM("Rout6"),FM("Rout7"),FM("Rout0")  ],FM("Prod3"))
    FM("Rout8").declare_table([FM("Rout8"),FM("Rout7"),FM("Rout8"),FM("Rout1")  ],FM("Prod2"))

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
##--------------------------END OF 3x3 MESH------------------------------------------------

##--------------------------------6x6 MESH------------------------------------------------
#                         UP           DOWN        LEFT        RIGHT         
else:
    FM("Rout0").declare_table([FM("Rout0"),FM("Rout6"), FM("Rout0"),FM("Rout1")  ],FM("Prod0"))
    FM("Rout1").declare_table([FM("Rout1"),FM("Rout7"), FM("Rout0"),FM("Rout2")  ],FM("Con0"))
    FM("Rout2").declare_table([FM("Rout2"),FM("Rout8"), FM("Rout1"),FM("Rout3")  ],FM("Prod1"))
    FM("Rout3").declare_table([FM("Rout3"),FM("Rout9"), FM("Rout2"),FM("Rout4")  ],FM("Prod2"))
    FM("Rout4").declare_table([FM("Rout4"),FM("Rout10"),FM("Rout3"),FM("Rout5")  ],FM("Con1"))
    FM("Rout5").declare_table([FM("Rout5"),FM("Rout11"),FM("Rout4"),FM("Rout5")  ],FM("Prod3"))

    FM("Rout6").declare_table([FM("Rout0"),FM("Rout12"), FM("Rout6"),FM("Rout7")  ],  FM("Prod4"))
    FM("Rout7").declare_table([FM("Rout1"),FM("Rout13"), FM("Rout6"),FM("Rout8")  ],  FM("Con2"))
    FM("Rout8").declare_table([FM("Rout2"),FM("Rout14"), FM("Rout7"),FM("Rout9")  ],  FM("Prod5"))
    FM("Rout9").declare_table([FM("Rout3"),FM("Rout15"), FM("Rout8"),FM("Rout10")  ], FM("Prod6"))
    FM("Rout10").declare_table([FM("Rout4"),FM("Rout16"),FM("Rout9"),FM("Rout11")  ], FM("Con3"))
    FM("Rout11").declare_table([FM("Rout5"),FM("Rout17"),FM("Rout10"),FM("Rout11")  ],FM("Prod7"))

    FM("Rout12").declare_table([FM("Rout6"),FM("Rout18"), FM("Rout12"),FM("Rout13")  ],FM("Con4"))
    FM("Rout13").declare_table([FM("Rout7"),FM("Rout19"), FM("Rout12"),FM("Rout14")  ],FM("Prod8"))
    FM("Rout14").declare_table([FM("Rout8"),FM("Rout20"), FM("Rout13"),FM("Rout15")  ],FM("Con5"))
    FM("Rout15").declare_table([FM("Rout9"),FM("Rout21"), FM("Rout14"),FM("Rout16")  ],FM("Con6"))
    FM("Rout16").declare_table([FM("Rout10"),FM("Rout22"),FM("Rout15"),FM("Rout17")  ],FM("Prod9"))
    FM("Rout17").declare_table([FM("Rout11"),FM("Rout23"),FM("Rout16"),FM("Rout17")  ],FM("Con7"))

    FM("Rout18").declare_table([FM("Rout12"),FM("Rout24"), FM("Rout18"),FM("Rout19")  ],FM("Prod10"))
    FM("Rout19").declare_table([FM("Rout13"),FM("Rout25"), FM("Rout18"),FM("Rout20")  ],FM("Con8"))
    FM("Rout20").declare_table([FM("Rout14"),FM("Rout26"), FM("Rout19"),FM("Rout21")  ],FM("Prod11"))
    FM("Rout21").declare_table([FM("Rout15"),FM("Rout27"), FM("Rout20"),FM("Rout22")  ],FM("Prod12"))
    FM("Rout22").declare_table([FM("Rout16"),FM("Rout28"), FM("Rout21"),FM("Rout23")  ],FM("Con9"))
    FM("Rout23").declare_table([FM("Rout17"),FM("Rout29"), FM("Rout22"),FM("Rout23")  ],FM("Prod13"))

    FM("Rout24").declare_table([FM("Rout18"),FM("Rout30"), FM("Rout24"),FM("Rout25")  ],FM("Prod14"))
    FM("Rout25").declare_table([FM("Rout19"),FM("Rout31"), FM("Rout24"),FM("Rout26")  ],FM("Con10"))
    FM("Rout26").declare_table([FM("Rout20"),FM("Rout32"), FM("Rout25"),FM("Rout27")  ],FM("Prod15"))
    FM("Rout27").declare_table([FM("Rout21"),FM("Rout33"), FM("Rout26"),FM("Rout28")  ],FM("Prod16"))
    FM("Rout28").declare_table([FM("Rout22"),FM("Rout34"), FM("Rout27"),FM("Rout29")  ],FM("Con11"))
    FM("Rout29").declare_table([FM("Rout23"),FM("Rout35"), FM("Rout28"),FM("Rout30")  ],FM("Prod17"))

    FM("Rout30").declare_table([FM("Rout24"),FM("Rout30"), FM("Rout30"),FM("Rout31")  ],FM("Con12"))
    FM("Rout31").declare_table([FM("Rout25"),FM("Rout31"), FM("Rout30"),FM("Rout32")  ],FM("Prod18"))
    FM("Rout32").declare_table([FM("Rout26"),FM("Rout32"), FM("Rout31"),FM("Rout33")  ],FM("Con13"))
    FM("Rout33").declare_table([FM("Rout27"),FM("Rout33"), FM("Rout32"),FM("Rout34")  ],FM("Con14"))
    FM("Rout34").declare_table([FM("Rout28"),FM("Rout34"), FM("Rout33"),FM("Rout35")  ],FM("Prod19"))
    FM("Rout35").declare_table([FM("Rout29"),FM("Rout35"), FM("Rout34"),FM("Rout35")  ],FM("Con15"))



#I think this is probably redudant, code above could handle masters and slaves
    FM("Con0").declare_master(FM("Rout1"))
    FM("Con1").declare_master(FM("Rout4"))

    FM("Con2").declare_master(FM("Rout7"))
    FM("Con3").declare_master(FM("Rout10"))

    FM("Con4").declare_master(FM("Rout12"))
    FM("Con5").declare_master(FM("Rout14"))
    FM("Con6").declare_master(FM("Rout15"))
    FM("Con7").declare_master(FM("Rout17"))

    FM("Con8").declare_master(FM("Rout19"))
    FM("Con9").declare_master(FM("Rout22"))

    FM("Con10").declare_master(FM("Rout25"))
    FM("Con11").declare_master(FM("Rout28"))

    FM("Con12").declare_master(FM("Rout30"))
    FM("Con13").declare_master(FM("Rout32"))
    FM("Con14").declare_master(FM("Rout33"))
    FM("Con15").declare_master(FM("Rout35"))

    FM("Prod0").declare_master(FM("Rout0"))
    FM("Prod1").declare_master(FM("Rout2"))
    FM("Prod2").declare_master(FM("Rout3"))
    FM("Prod3").declare_master(FM("Rout5"))

    FM("Prod4").declare_master(FM("Rout6"))
    FM("Prod5").declare_master(FM("Rout8"))
    FM("Prod6").declare_master(FM("Rout9"))
    FM("Prod7").declare_master(FM("Rout11"))

    FM("Prod8").declare_master(FM("Rout13"))
    FM("Prod9").declare_master(FM("Rout16"))

    FM("Prod10").declare_master(FM("Rout18"))
    FM("Prod11").declare_master(FM("Rout20"))
    FM("Prod12").declare_master(FM("Rout21"))
    FM("Prod13").declare_master(FM("Rout23"))

    FM("Prod14").declare_master(FM("Rout24"))
    FM("Prod15").declare_master(FM("Rout26"))
    FM("Prod16").declare_master(FM("Rout27"))
    FM("Prod17").declare_master(FM("Rout29"))

    FM("Prod18").declare_master(FM("Rout31"))
    FM("Prod19").declare_master(FM("Rout34"))
##--------------------------END OF 6x6 MESH------------------------------------------------

#update_UI()
###### Task Scheduler ######
def Run_task_scheduler():
    global clock_tick
    #for x in FM("Rout2").ports:
    #    print(x.direction)
    if(clock_tick % 10 == 1):
        random_target("Prod4","red") #Uniform Traffic
        #random_hotspot_target("Prod4","red") #Hotspot Traffic
        #random_traffic("red")
        FM("Prod4").produce_message(['red','red','red','red'],"Con2", 0)
        pass
        
        
    if(clock_tick % 10 == 7):
        random_target("Prod3","yellow")
        #random_hotspot_target("Prod3","yellow")
        #random_traffic("yellow")
        #FM("Prod3").produce_message(['yellow','yellow','yellow','yellow'],"Con2",1)
        pass

    if(clock_tick % 10 == 3):
        #random_target("Prod2","green")
        #random_hotspot_target("Prod2","green")
        #random_traffic("green")
        #FM("Prod2").produce_message(['green','green','green'],"Con3",0)
        pass

    if(clock_tick % 10 == 4):
        random_target("Prod1","blue")
        #random_hotspot_target("Prod1","blue")
        #random_traffic("blue")
        #FM("Prod1").produce_message(['blue','blue','blue'],"Con3",1)
        pass

    if(clock_tick % 10 == 5):
        random_target("Prod0","blue")
        #random_hotspot_target("Prod0","blue")
        #random_traffic("blue")
        #FM("Prod0").produce_message(['blue','blue','blue'],"Con0",1)
        pass
    if(clock_tick):
        #produce_load(clock_tick)
        pass        

def produce_load(clock_tick):
    if(clock_tick % 25 == 1): random_hotspot_target("Prod0","blue")
    #if(clock_tick % 25 == 2): random_hotspot_target("Prod1","blue")
    if(clock_tick % 25 == 3): random_hotspot_target("Prod2","blue")
    #if(clock_tick % 25 == 3): random_hotspot_target("Prod3","blue")
    if(clock_tick % 25 == 4): random_hotspot_target("Prod4","blue")
    if(clock_tick % 25 == 5): random_hotspot_target("Prod5","blue")
    #if(clock_tick % 25 == 6): random_hotspot_target("Prod6","blue")
    if(clock_tick % 25 == 8): random_hotspot_target("Prod7","blue")
    if(clock_tick % 25 == 9): random_hotspot_target("Prod8","blue")
    #if(clock_tick % 25 == 10):random_hotspot_target("Prod9","blue")
    if(clock_tick % 25 == 11):random_hotspot_target("Prod10","blue")
    if(clock_tick % 25 == 12):random_hotspot_target("Prod11","blue")
    if(clock_tick % 25 == 13):random_hotspot_target("Prod12","blue")
    if(clock_tick % 25 == 14):random_hotspot_target("Prod13","blue")
    #if(clock_tick % 25 == 15):random_hotspot_target("Prod14","blue")
    if(clock_tick % 25 == 16):random_hotspot_target("Prod15","blue")
    #if(clock_tick % 25 == 17):random_hotspot_target("Prod16","blue")
    if(clock_tick % 25 == 18):random_hotspot_target("Prod17","blue")
    if(clock_tick % 25 == 19):random_hotspot_target("Prod18","blue")
    if(clock_tick % 25 == 20):random_hotspot_target("Prod19","blue")


def random_traffic(producer, color):
    con = "Con" + str(random.randint(0,3))
    random.choice(Producers[0:4]).produce_message([color, color],con,0)

def random_hotspot_target(producer, color, pri = 0):
    #Con3 is hotspot
    num = random.randint(0,6)
    if(num > 3): num = 3
    con = "Con" + str(num)
    FM(producer).produce_message([color,color],con,pri)

#def random_target(producer, color):
#    con = "Con" + str(random.randint(0,3))
#    FM(producer).produce_message([color,color],con,0)

def random_target(producer, color):
    con = "Con" + str(random.randint(0,3))
    FM(producer).produce_message([color,color],con,0)

def random_tasks():
    string = "Con"
    string += str(random.randint(0,3))
    random.choice(Producers[0:3]).produce_message(['orange','orange','orange'],string,random.randint(0,1))

#"""
################ THE CLOCK ################

if __name__ == "__main__":
    with open('output.json', 'w') as json_file:
        pass    
    def on_spacebar(event):
        global clock_tick
        if event.name == 'space':
            Run_task_scheduler()
            clock_tick += 1
            globals.clock_tick+= 1
            for x in Routers:
                x.hold_on()
            for x in Producers:
                x.hold_on()
            for x in Routers:
                x.send()
            for x in Producers:
                x.send()
            #update_UI()

            data = {}    
            routers = {}
            for router in Routers:
                routers[f"{router.name}"] = {}
                port_id = 0 
                for port in router.ports:
                    routers[f"{router.name}"][f"port_{str(port_id)}"] = list(port.data.queue)
                    port_id+= 1
            data['routers'] = routers
            with open('output.json', 'a') as json_file:
                json.dump(data, json_file)


    
    keyboard.on_press_key('space', on_spacebar)
    keyboard.wait('esc')
    print(f"\n\n Clock cycle:{clock_tick}\n\n")

#I get called every time space is pressed
else:
    def getJSONGUI():
        global clock_tick
        Run_task_scheduler()
        clock_tick+= 1
        globals.clock_tick+= 1
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
