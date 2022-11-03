from computer import Computer
from terminal import Terminal
import sys
import random
from room import Room, Area
from door import Door, LockedDoor
from control import Control
from item import Item, Key, Note
from character import Character, Programmer
from player import Player
from security import SecurityBot
from weapon import Weapon
from completitionCheck import CompletionCheck

control = Control()
terminal = Terminal(control)
control.terminal = terminal
control.commandsToActions["commands"] = terminal.toggleCommands
control.commandsToActions["quit"] = terminal.endGame

f = open("names.txt","r")
names = list(i[:-1] for i in f.readlines())
f.close

def name():
    return random.choice(names)

# Creating Storage Room
storageRoom = Room("Storage Room", "Piles high with random boxes and machinery parts", terminal)
storageRoomMessenger = Area("Messenger Storage", "The shelves here are filled with small bots designed to deliver messages",terminal,storageRoom)
storageRoomWeapons = Area("Weapons Storage", "The shelves here are filled with machinery designed to kill and destroy",terminal,storageRoom)
storageRoomSentries = Area("Sentries Storage", "There are rows of blank guard robots",terminal,storageRoom)
storageRoomProtocol = Area("Protocol Storage", "There are rows of robots in the appearance of humans, created to help and assist",terminal,storageRoom)
storageRoomCleaning = Area("Cleaning Storage","The robots here remove dirt, grime, and the stuff no one talks about", terminal,storageRoom)
storageRoomLaborer = Area("Laborer Storage", "There are rows of robots designed to do heavy lifting and moving",terminal,storageRoom)
storageRoomMessenger.sides = {"north":storageRoomProtocol, "west": storageRoomLaborer}
storageRoomWeapons.sides = {"west": storageRoomSentries, "south": storageRoomProtocol}
storageRoomSentries.sides = {"east": storageRoomWeapons,"south":storageRoomCleaning}
storageRoomProtocol.sides = {"north": storageRoomWeapons, "west":storageRoomCleaning, "south": storageRoomMessenger}
storageRoomCleaning.sides = {"east": storageRoomProtocol, "north": storageRoomSentries, "south": storageRoomLaborer}
storageRoomLaborer.sides = {"east":storageRoomMessenger,"north":storageRoomCleaning}

# Create outside room
outside = Room("Outside","Away from the confines of the building, the world looks massive",terminal)
control.completedCheck = CompletionCheck(control,terminal,outside)

# Create security office
securityOffice = Room("Security Office", "Everything looks clean and nicely tendered", terminal)
for i in range(5):
    SecurityBot(str(i+1),securityOffice,terminal,control)
    

# Creating Programming Room and various stations
programmingRoom = Room("Programmers Office", "Banks of computer span this room", terminal)
programmingDesks = []
for i in range(2):
    programmingDeskRow = []
    for j in range(5):
        row = "1st" if (i == 0) else "2nd"
        description = f"Computer terminal in {row} row with a number {j} on the banner"
        newStation = Area("Computer Terminal",description,terminal,programmingRoom)
        Programmer(name(),Weapon("Blaster","Not normally required in their line of work",2,terminal,control),newStation,terminal,control)
        programmingDeskRow.append(newStation)
        if i == 1:
            programmingDesks[0][j].sides["south"] = newStation
            newStation.sides["north"] = programmingDesks[0][j]

        if j > 0:
            programmingDeskRow[j-1].sides["east"] = newStation
            newStation.sides["west"] = programmingDeskRow[j-1]

        password = Computer(newStation,terminal,control).getPassword()
        Note("crisp white paper",password,newStation,terminal,control)
        
        
    programmingDesks.append(programmingDeskRow)
    

# Creating Engineering Room
engineeringRoom = Room("Engineering Office", "In the centre there is a large worktable. Surrounded by a series of computer stations and 3D printers", terminal)
password = Computer(engineeringRoom,terminal,control).getPassword()
Note("yellow sticky note covered in stains",password,newStation,terminal,control)

# Creating Marketting Room
markettingRoom = Room("Marketting Office", "Just a bunch of computers and a giant colour palette poster", terminal)
for i in range(4):
    Character(name(),"Works on creating a positive message for the company",None,markettingRoom,terminal,control)

# Creating Lunch Room
lunchRoom = Room("Lunch Room", "There's a mini kitchenette to the west, and several tables fill the rest of the room", terminal)

# Create Waiting Room
waitingRoom = Room("Waiting Room", "Nothing to see here, just a threadbare couch", terminal)
Character(name(),"Serves people who wish to see the CEO",None,waitingRoom,terminal,control)


# Creating CEO's Office
ceoOffice = Room("CEO's Office", "A luxurious room, fit for any executive", terminal)
Item("Desk", "Dark mahogony with luxurious inlay",False,ceoOffice,terminal,control)

# Creating Data Store
dataStore = Room("Data store and super computer","A room filled with harddrives to the north and a large quantum computer to the south",terminal)
Item("Hardrive","Holds valuable company information that will be difficult to replace", True,dataStore,terminal,control)
Item("Quantum Computer", "Processes complicated algorithms in seconds that would take conventional computers years",False,dataStore,terminal,control)

# Creating Main Corridor
mainCorridor = Room("Main Corridor", "There is nowhere to hide", terminal)

mainCorridorRooms = []
for i in range(17):
    newArea = Area("Main Corridor","Blank",terminal,mainCorridor)
    mainCorridorRooms.append(newArea)
    if i != 0:
        if i<12:
            newArea.sides["north"] = mainCorridorRooms[i-1]
            mainCorridorRooms[i-1].sides["south"] = newArea
        else:
            newArea.sides["west"] = mainCorridorRooms[i-1]
            mainCorridorRooms[i-1].sides["east"] = newArea


# Creating factory space
# creating Protocol Manufacturing
protocolManu = Room("Protocol Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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
laborerManu = Room("Laborer Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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
cleanerManu = Room("Cleaner Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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
messengerManu = Room("Messenger Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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
sentryManu = Room("Sentry Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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
weaponsManu = Room("Weapons Manufacturing", "A factory filled with a multitude of machines, all connected", terminal)
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

# Create Weapons corridor 
manuCorridor = Room("Manufacturing Corridor", "There are no people here, only robots", terminal)

manuCorridorRooms = []
for i in range(9):
    newArea = Area("Manufacturing Corridor","Blank",terminal,manuCorridor)
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
newDoor = Door("Door to Security Room", "The door is constructed from metal, it would be impossible to enter when locked", terminal)
mainCorridorRooms[11].setDoor(newDoor,"west")
securityOffice.setDoor(newDoor,"east")

# Create doors between programming room and corridor
newDoor = Door("Clear Door", "The door is constructed from bullet proof glass", terminal)
mainCorridorRooms[12].setDoor(newDoor,"north")
programmingDesks[1][0].setDoor(newDoor,"south")

newDoor = Door("Clear Door", "The door is constructed from bullet proof glass", terminal)
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
newDoor = LockedDoor("Mahogony Door", "Beautifully crafted, this door looks out of place with the minimalist design of the rest of the building.",newKey,terminal)
waitingRoom.setDoor(newDoor,"south") 
ceoOffice.setDoor(newDoor,"north")

newDoor = LockedDoor("Sliding Panel", "This door is carefully concealed from human sight.",newKey,terminal)
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

newDoor = Door("Portal","You can't see anything through it.", terminal)
manuCorridorRooms[8].setDoor(newDoor,"south")
engineeringRoom.setDoor(newDoor,"south")

# CREATING CHARACTERS
player = Player("You are a robot",Weapon("fist","",1,terminal,control),terminal,control)

control.player = player

control.currentRoom = storageRoomSentries
Note("Data stick","This company is evil, get out and expose it",control.currentRoom,terminal,control)
control.currentRoom = programmingDesks[0][0]

terminal.descriptionAdd("WELCOME TO Game Name")
terminal.descriptionAdd("Type 'commands' for hints or type ? at any time")
terminal.descriptionAdd("")
terminal.descriptionAdd("")
control.currentRoom.describe()

while not(control.completedCheck.run()):
    control.runAll()
