from random import choice

from character import Character
from weapon import Weapon

class Control():
    """
    A class that controls all actions and allows a link between objects

    ...
    Attributes
    ----------
    currentRoom : Room
        the current location of the player
    terminal : Terminal
        link to terminal
    eternalObjects : list
        list of objects that are running regardless of whether the player is currently in the same room
    commandsToActions : dict
        dictionary of commands with links to functions that process those commands
    player : Player
        the current player object

    Methods
    -------
    runAll():
        runs room and eternal objects

    command(command):
        converts a text based command into an action directed at the relevant object reference

    move(command):
        calls room to move player

    look(command):
        describes currentRoom

    examine(command):
        finds object and describes it

    take(command):
        finds object and adds it to the player's inventory or weapons

    fight(command):
        finds person and attacks it

    talk(command):
        finds character and prompts them to talk

    watch(command):
        finds object in room to watch, or stops watching

    inventory(command):
        outputs current inventory contents

    setWeapon(command):
        sets the weapon specified to the current one

    """
    def __init__(self):
        ''' Constructs necessary attributes for the control  '''
        self.currentRoom = None
        self.terminal = None
        self.eternalObjects = []
        self.commandsToActions = {"move":self.move,
                                "look": self.look,
                                "examine": self.examine,
                                "take": self.take,
                                "fight":self.fight,
                                "talk":self.talk,
                                "watch":self.watch,
                                "inventory":self.inventory,
                                "setweapon":self.setWeapon,}
        self.player = None
                                       

    def runAll(self):
        """ Runs eternal objects and the current room """
        self.terminal.run()
        activeRooms = [self.currentRoom]
        for object in self.eternalObjects:
            room = object.run()
            if room not in activeRooms and room is not None:
                activeRooms.append(room)
        for room in activeRooms:
            room.run()

    def command(self,command):
        """ Converts a text based command into an action directed at the relevant object reference """
        try:
            if command == "":
                return
            command = command.lstrip().split()
            if command[0] in self.commandsToActions.keys():
                self.commandsToActions[command[0]](command)
                return
            command = " ".join(command)
            for object in self.player.inventory:
                if command.startswith(object.name.lower()):
                    keyword = command[len(object.name.lower()):].lstrip()
                    if keyword in object.keywords:
                        object.do(keyword)
                        return
                    else:
                        self.terminal.descriptionAdd(f"The {object.name.lower()} can't do that.")
            for object in self.currentRoom.items:
                if command.startswith(object.name.lower()):
                    keyword = command[len(object.name.lower()):].lstrip()
                    found = False
                    for word in object.keywords:
                        if keyword.startswith(word):
                            found = True
                    if found:
                        object.do(keyword)
                        return
                    else:
                        self.terminal.descriptionAdd(f"The {object.name} can't do that.")
                        if object.keywords:
                            commands = "".join(i+", " for i in object.keywords)
                        else:
                            commands = "do nothing  "
                        
                        self.terminal.descriptionAdd(f"It can {commands[:-2]}")
                        return
            self.terminal.descriptionAdd("Not a valid command")
            self.terminal.descriptionAdd("")
        except:
            pass
    
    def move(self,command):
        """ Calls room to move player and adds new room description to terminal """
        self.currentRoom = self.currentRoom.move(command[1:])
        self.terminal.descriptionAdd("")
        self.currentRoom.describe()
        return

    def look(self,command):
        """ Descibes current room """
        self.currentRoom.describe()

    def examine(self,command):
        """ Finds object reference and outputs description to terminal """
        try:
            foundItem = False
            command.pop(0)
            command = " ".join(command)
            
            if command == "me":
                self.player.describe()
                return
            for thing in self.currentRoom.objects:
                if thing.name.lower() == command:
                    thing.describe()
                    foundItem = True
                    break
            if not(foundItem):
                self.terminal.descriptionAdd("There isn't such a thing.")
        except:
            self.terminal.descriptionAdd("You must say what you want to examine.")
            
    def take(self,command):
        """ Finds object reference from objects in room and adds object to player's inventory and weapons whilst removing it from the room"""
        command.pop(0)
        command = " ".join(command)
        foundItem = False
        for thing in self.currentRoom.objects:
            if thing.name.lower() == command:
                if thing.take():
                    if isinstance(thing,Weapon):
                        self.player.weaponsEquipped.append(thing)
                        self.currentRoom.objects.remove(thing)
                        self.currentRoom.items.remove(thing)
                    else:
                        self.player.inventory.append(thing)
                        self.currentRoom.objects.remove(thing)
                        self.currentRoom.items.remove(thing)
                foundItem = True
                break
        if not(foundItem):
            self.terminal.descriptionAdd("There isn't such a thing.")

    def fight(self,command):
        """ Finds character object reference and calls player object to fight it """
        foundPerson = False
        person = " ".join(command[1:])
        for thing in self.currentRoom.characters:
            if thing.name.lower() == person and isinstance(thing, Character):
                foundPerson = True
                self.player.fight(thing)
                break
        if not(foundPerson):
            if self.currentRoom.characters:
                self.player.fight(choice(self.currentRoom.characters))
            else:
                self.terminal.descriptionAdd("There isn't a person called that here.")
    
    def talk(self,command):
        """ Finds character object, formats command, and calls character to speak"""
        foundPerson = False
        person = command[1]
        command.pop(0)
        command.pop(0)
        command = " ".join(command)
        for thing in self.currentRoom.characters:
            if thing.name.lower() == person and isinstance(thing, Character):
                foundPerson = True
                thing.talk(self.player, command)
                break
        if not(foundPerson):
            self.terminal.descriptionAdd("There isn't a person called that here.")
            
    def watch(self,command):
        """ Finds object (Item, Character, Door) in the room to watch and assigns to player.focus"""
        if len(command) > 1:
            if command[1] == "stop":
                self.player.focus = None
                return
            foundItem = False

            command = " ".join(command)

            for thing in self.currentRoom.objects:
                if thing.name.lower() == command:
                    self.player.focus = thing
                    foundItem = True
                    break
            if not(foundItem):
                self.terminal.descriptionAdd("There isn't such a thing.")

        else:
            self.terminal.descriptionAdd("Specify what you want to watch")

    def inventory(self,command):
        """ Lists all items in player's inventory to the terminal """
        self.terminal.descriptionAdd("You have:")
        for i in self.player.inventory:
            self.terminal.descriptionAdd("\t"+i.name)

    def setWeapon(self,command):
        """ Finds weapon specified in command and assigns it to player.chosenWeapon """
        foundItem = False
        joinedName = " ".join(command[1:])
        
        for thing in self.player.weaponsEquipped:
            if thing.name.lower() == joinedName:
                self.player.chosenWeapon = thing
                self.terminal.descriptionAdd(f"You are using {thing.name}")
                foundItem = True
        if not(foundItem):
            self.terminal.descriptionAdd("You don't have that.")
