import random
from computer import Computer
from terminal import Terminal
from room import Room, Area
from door import Door, LockedDoor
from control import Control
from item import Item, Key, Note, DormantRobot, PlayerCharacterChanger
from character import Character, Programmer, CEO, Engineer
from player import Player
from security import SecurityBot
from weapon import Weapon
from completitionCheck import CompletionCheck

import robots

control = Control()
terminal = Terminal(control)
control.terminal = terminal
control.commandsToActions["commands"] = terminal.toggleCommands
control.commandsToActions["quit"] = terminal.endGame

f = open("names.txt","r")
names = list(i[:-1] for i in f.readlines())
f.close

def name():
    ''' Returns random name from preloaded list of names'''
    return random.choice(names)

# Creating rooms

# Creating Storage Room
storageRoom = Room("Storage Room", "There are piles high with boxes of different sizes and machinery parts",False, terminal)
storageRoomMessenger = Area("Messenger Storage", "The shelves here are filled with small bots designed to deliver messages",terminal,storageRoom)
#DormantRobot(storageRoomMessenger,terminal,control,robots.messenger)
storageRoomWeapons = Area("Weapons Storage", "The shelves here are filled with machinery designed to kill or destroy",terminal,storageRoom)
storageRoomSentries = Area("Sentries Storage", "There are rows of blank guard robots",terminal,storageRoom)
DormantRobot(storageRoomSentries,terminal,control,robots.sentry)
storageRoomProtocol = Area("Protocol Storage", "There are rows of robots in the appearance of humans, created to help and assist",terminal,storageRoom)
DormantRobot(storageRoomProtocol,terminal,control,robots.protocol)
storageRoomCleaning = Area("Cleaning Storage","The robots here remove dirt, grime, and dust", terminal,storageRoom)
DormantRobot(storageRoomCleaning,terminal,control,robots.cleaning)
storageRoomLaborer = Area("Laborer Storage", "There are rows of robots designed to do heavy lifting and moving",terminal,storageRoom)
DormantRobot(storageRoomLaborer,terminal,control,robots.laborer)
storageRoomMessenger.sides = {"north":storageRoomProtocol, "west": storageRoomLaborer}
storageRoomWeapons.sides = {"west": storageRoomSentries, "south": storageRoomProtocol}
storageRoomSentries.sides = {"east": storageRoomWeapons,"south":storageRoomCleaning}
storageRoomProtocol.sides = {"north": storageRoomWeapons, "west":storageRoomCleaning, "south": storageRoomMessenger}
storageRoomCleaning.sides = {"east": storageRoomProtocol, "north": storageRoomSentries, "south": storageRoomLaborer}
storageRoomLaborer.sides = {"east":storageRoomMessenger,"north":storageRoomCleaning}

# Create outside room
outside = Room("Outside","Away from the confines of the building, the world looks massive",True,terminal)
control.completedCheck = CompletionCheck(control,terminal,outside)

# Create security office
securityOffice = Room("Security Office", "Everything looks clean and nicely tendered",True, terminal)
for i in range(5):
    SecurityBot(str(i+1),securityOffice,terminal,control)
    

# Creating Programming Room and various stations
programmingRoom = Room("Programmers Office", "Banks of computers span this room arranged in 2 rows of 5", True,terminal)
programmingDesks = []
for i in range(2):
    programmingDeskRow = []
    for j in range(5):
        row = "1st" if (i == 0) else "2nd"
        description = f"Computer terminal in {row} row with a number {j+1} on the banner"
        newStation = Area("Computer Terminal",description,terminal,programmingRoom)
        Programmer(name(),Weapon("Blaster","Not normally required in their line of work",2,terminal,control),newStation,terminal,control)
        programmingDeskRow.append(newStation)
        if i >0:
            programmingDesks[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = programmingDesks[i-1][j]

        if j > 0:
            programmingDeskRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = programmingDeskRow[j-1]

        password = Computer(newStation,terminal,control).getPassword()
        Note("crisp white paper",password,newStation,False,terminal,control)
        
        
    programmingDesks.append(programmingDeskRow)

Item("Bin","Filled with bits of paper",True,programmingDesks[1][0],terminal,control)

# Creating Engineering Room
engineeringRoom = Room("Engineering Office", "The walls are occupied by a series of computer stations and 3D printers, in the centre there is a large worktable", True,terminal)
for i in range(4):
    Engineer(name(),Weapon("Wrench","Normally used for undoing nuts",2,terminal,control),engineeringRoom,terminal,control)
password = Computer(engineeringRoom,terminal,control).getPassword()
Note("yellow sticky note covered in stains",password,engineeringRoom,False,terminal,control)
Item("Worktable","It is square with a side length of 3m",False,engineeringRoom,terminal,control)
Item("3D Printer","Uses additive manufacturing to create quick prototypes",False,engineeringRoom,terminal,control)

# Creating Marketting Room
markettingRoom = Room("Marketting Office", "Just a bunch of computers and a giant colour palette poster", True,terminal)
for i in range(4):
    Character(name(),"Works on creating a positive public image",None,markettingRoom,terminal,control)
Item("Desk","Cheaply bought from a flatpack furniture store",False,markettingRoom,terminal,control)

# Creating Lunch Room
lunchRoom = Room("Lunch Room", "There's a mini kitchenette to the east, and several tables fill the rest of the room", True,terminal)
Item("Cooker","Heats and hydrates food quickly from its dehydrated state",True,lunchRoom,terminal,control)
Item("Sink","A simple stainless steel sink",False,lunchRoom,terminal,control)
for i in range(3):
    Item("Table","Constructed from plastic, although fairly sturdy",False,lunchRoom,terminal,control)

# Create Waiting Room
waitingRoom = Room("Waiting Room", "Nothing to see here, just a threadbare couch", True,terminal)
clerk = Character(name(),"Serves people who wish to see the CEO",None,waitingRoom,terminal,control)
Item("Couch","This used to be blue, you think. It's covered in dust and dirt - visitors would rather stand",False,waitingRoom,terminal,control)
Item("Desk","Cheaply bought from a flatpack furniture store",False,waitingRoom,terminal,control)


# Creating CEO's Office
ceoOffice = Room("CEO's Office", "A luxurious room, fit for a king", True, terminal)
Item("Desk", "Dark mahogony with luxurious inlay",False,ceoOffice,terminal,control)
CEO(name(),Weapon("Small range EMP","Temporarily disables electronics within a 1 m radius",10,terminal,control),ceoOffice,terminal,control)

# Creating Data Store
dataStore = Room("Data store and super computer","A room filled with whiring hard drives to the north and a large quantum computer to the south", True,terminal)
Item("Hardrive","Holds valuable company information that would be difficult to replace", True,dataStore,terminal,control)
Item("Quantum Computer", "Processes complicated algorithms in seconds that would take conventional computers years",False,dataStore,terminal,control)

# Creating Main Corridor
mainCorridor = Room("Main Corridor", "There is nowhere to hide",True, terminal)

decorations = [lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Plant","Adds greenery to the corridors",True,room,terminal,control),
                lambda room: Item("Lockers","A row of lockers, positioned 1.2 m from the floor",False,room,terminal,control),
                lambda room: Item("Lockers","A row of lockers, positioned 1.2 m from the floor",False,room,terminal,control),
                lambda room: Item("Lockers","A row of lockers, positioned 1.2 m from the floor",False,room,terminal,control),
                lambda room: Item("Pidgeon Holes","A row of pidgeon holes, each is a 30 cm cube",False,room,terminal,control),
                lambda room: Item("Pidgeon Holes","A row of pidgeon holes, each is a 30 cm cube",False,room,terminal,control),
                lambda room: Item("Pidgeon Holes","A row of pidgeon holes, each is a 30 cm cube",False,room,terminal,control),
                lambda room: Item("Vest rack","Occupied by 25 high-vis vests",True,room,terminal,control),
                lambda room: Item("Notice board","A cork board that was last used in the 20th century, about 200 years ago",False,room,terminal,control),
                None,
                None,
                None]
        
random.shuffle(decorations)

mainCorridorRooms = []
for i in range(17):
    newArea = Area("Main Corridor","The floors are white, as are the walls",terminal,mainCorridor)
    mainCorridorRooms.append(newArea)
    if decorations[i] is not None:
        decorations[i](newArea)
    if i != 0:
        if i<12:
            newArea.sides["north"] = mainCorridorRooms[i-1]
            mainCorridorRooms[i-1].sides["south"] = newArea
        else:
            newArea.sides["west"] = mainCorridorRooms[i-1]
            mainCorridorRooms[i-1].sides["east"] = newArea


# Creating factory space
# creating Protocol Manufacturing
protocolManu = Room("Protocol Manufacturing", "A factory filled with a multitude of machines, all connected",False, terminal)
protocolMachines = []
for i in range(3):
    protocolMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,protocolManu)
        protocolMachinesRow.append(newStation)
        if i > 0:
            protocolMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = protocolMachines[i-1][j]

        if j > 0:
            protocolMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = protocolMachinesRow[j-1]
        
    protocolMachines.append(protocolMachinesRow)

# Creating Laborer Manufacturing
laborerManu = Room("Laborer Manufacturing", "A factory filled with a multitude of machines, all connected", False,terminal)
laborerMachines = []
for i in range(3):
    laborerMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,laborerManu)
        laborerMachinesRow.append(newStation)
        if i > 0:
            laborerMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = laborerMachines[i-1][j]

        if j > 0:
            laborerMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = laborerMachinesRow[j-1]
    laborerMachines.append(laborerMachinesRow)

# Creating Cleaner Manufacturing
cleanerManu = Room("Cleaner Manufacturing", "A factory filled with a multitude of machines, all connected", False,terminal)
cleanerMachines = []
for i in range(3):
    cleanerMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,cleanerManu)
        cleanerMachinesRow.append(newStation)
        if i > 0:
            cleanerMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = cleanerMachines[i-1][j]

        if j > 0:
            cleanerMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = cleanerMachinesRow[j-1]
    cleanerMachines.append(cleanerMachinesRow)

# Creating Messenger Manufacturing
messengerManu = Room("Messenger Manufacturing", "A factory filled with a multitude of machines, all connected", False,terminal)
messengerMachines = []
for i in range(3):
    messengerMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,messengerManu)
        messengerMachinesRow.append(newStation)
        if i > 0:
            messengerMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = messengerMachines[i-1][j]

        if j > 0:
            messengerMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = messengerMachinesRow[j-1]
    messengerMachines.append(messengerMachinesRow)

# Creating Sentry Manufacturing
sentryManu = Room("Sentry Manufacturing", "A factory filled with a multitude of machines, all connected", False, terminal)
sentryMachines = []
for i in range(3):
    sentryMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,sentryManu)
        sentryMachinesRow.append(newStation)
        if i > 0:
            sentryMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = sentryMachines[i-1][j]

        if j > 0:
            sentryMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = sentryMachinesRow[j-1]
    sentryMachines.append(sentryMachinesRow)

# Creating Weapons Manufacturing
weaponsManu = Room("Weapons Manufacturing", "A factory filled with a multitude of machines, all connected", False, terminal)
weaponsMachines = []
for i in range(3):
    weaponsMachinesRow = []
    for j in range(3):
        description = "A machine chugging away strongly and loudly."
        newStation = Area("Manufacturing Machine",description,terminal,weaponsManu)
        weaponsMachinesRow.append(newStation)
        if i > 0:
            weaponsMachines[i-1][j].sides["south"] = newStation
            newStation.sides["north"] = weaponsMachines[i-1][j]

        if j > 0:
            weaponsMachinesRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = weaponsMachinesRow[j-1]
    weaponsMachines.append(weaponsMachinesRow)

# Create manufacturing corridor 
manuCorridor = Room("Manufacturing Corridor", "There are no people here, only robots", False, terminal)

manuCorridorRooms = []
for i in range(9):
    newArea = Area("Manufacturing Corridor","There are grey floors and a slightly darker gery for the walls",terminal,manuCorridor)
    manuCorridorRooms.append(newArea)
    if i != 0:
        newArea.sides["north"] = manuCorridorRooms[i-1]
        manuCorridorRooms[i-1].sides["south"] = newArea

# Create door between storage room and corridor 
newDoor = Door("Door to Storage Room", "Old and musty, this door is rarely used", terminal)
mainCorridorRooms[0].setDoor(newDoor,"east")
storageRoomLaborer.setDoor(newDoor,"west")

mainCorridorRooms[0].setDoor(newDoor,"east")
storageRoomLaborer.setDoor(newDoor,"west")

exitKey = Key("Orange keycard","You immediately know what this for, the door to the outside",ceoOffice,terminal,control)

newDoor = LockedDoor("Door to the Outside", "A sleek silver door, it has an orange card reader",exitKey,terminal)
mainCorridorRooms[7].setDoor(newDoor,"east")
outside.setDoor(newDoor,"west")

# Create door between security office and corridor
newDoor = Door("Door to Security Room", "The door is constructed from metal, it would be impossible to enter when locked, even if you could fit a tank in the corridor", terminal)
mainCorridorRooms[11].setDoor(newDoor,"west")
securityOffice.setDoor(newDoor,"east")

# Create doors between programming room and corridor
newDoor = Door("Clear Door", "The door is constructed from glass", terminal)
mainCorridorRooms[12].setDoor(newDoor,"north")
programmingDesks[1][0].setDoor(newDoor,"south")

newDoor = Door("Clear Door", "The door is constructed from glass", terminal)
mainCorridorRooms[16].setDoor(newDoor,"north")
programmingDesks[1][4].setDoor(newDoor,"south")

# Link programming room and super computer
newDoor = Door("Archway", "Just an archway", terminal)
dataStore.setDoor(newDoor,"west")
programmingDesks[0][4].setDoor(newDoor,"east")

# Link engineering Room to corridor
newDoor = Door("Pine Door", "Constructed from pine, fairly ornate considering the setting", terminal)
engineeringRoom.setDoor(newDoor,"north")
mainCorridorRooms[11].setDoor(newDoor,"south")

# Link Marketting Room to corridor
newDoor = Door("Pine Door", "Constructed from pine, fairly ornate considering the setting", terminal)
markettingRoom.setDoor(newDoor,"north")
mainCorridorRooms[14].setDoor(newDoor,"south")

# Link Lunch Room and Corridor
newDoor = Door("Pine Door", "Constructed from pine, fairly ornate considering the setting", terminal)
lunchRoom.setDoor(newDoor,"north")
mainCorridorRooms[16].setDoor(newDoor,"south")

# Link Waiting Room and Corridor
newDoor = Door("Archway","It's just an archway", terminal)
waitingRoom.setDoor(newDoor,"west") 
mainCorridorRooms[16].setDoor(newDoor,"east")

# Link CEO's Office to other rooms
newKey = Key("Black Stone","A large black stone that emits a strange signal. It could unlock a door",waitingRoom,terminal,control)
newDoor = LockedDoor("Mahogony Door", "Beautifully crafted, this door looks out of place with the minimalist design of the rest of the building",newKey,terminal)
waitingRoom.setDoor(newDoor,"south") 
ceoOffice.setDoor(newDoor,"north")

newDoor = LockedDoor("Sliding Panel", "This door is carefully concealed from human sight",newKey,terminal)
lunchRoom.setDoor(newDoor,"west") 
ceoOffice.setDoor(newDoor,"east")

# Link Manufacturing Rooms to manufacturing corridor
protocolMachines[1][2].sides["east"] = manuCorridorRooms[1]
manuCorridorRooms[1].sides["west"] = protocolMachines[1][2]
laborerMachines[1][2].sides["east"] = manuCorridorRooms[4]
manuCorridorRooms[4].sides["west"] = laborerMachines[1][2]
cleanerMachines[1][2].sides["east"] = manuCorridorRooms[7]
manuCorridorRooms[7].sides["west"] = cleanerMachines[1][2]

messengerMachines[1][2].sides["west"] = manuCorridorRooms[1]
manuCorridorRooms[1].sides["east"] = messengerMachines[1][2]
sentryMachines[1][2].sides["west"] = manuCorridorRooms[4]
manuCorridorRooms[4].sides["east"] = sentryMachines[1][2]
weaponsMachines[1][2].sides["west"] = manuCorridorRooms[7]
manuCorridorRooms[7].sides["east"] = weaponsMachines[1][2]

newDoor = Door("Portal","You can't see anything through the black swirls", terminal)
manuCorridorRooms[8].setDoor(newDoor,"south")
engineeringRoom.setDoor(newDoor,"south")

# CREATING CHARACTERS
player = Player("You are a robot",Weapon("fist","",1,terminal,control),terminal,control)

control.player = player

control.currentRoom = storageRoomLaborer

Note("yellow post-it note","This company is evil, get out and expose it!",control.currentRoom,True,terminal,control)
starterWeapon = Weapon("Plasma blade","The handle is roughly 10cm long, but the blade is 40cm when activated",2,terminal,control)
control.currentRoom.items.append(starterWeapon)
control.currentRoom.objects.append(starterWeapon)

terminal.descriptionAdd("WELCOME TO EscapeTech","bold")
terminal.descriptionAdd("Type 'commands' for hints or type ? at any time")
terminal.descriptionAdd("")
terminal.descriptionAdd("")
control.currentRoom.describe()


while not(control.completedCheck.run()):
    control.runAll()
