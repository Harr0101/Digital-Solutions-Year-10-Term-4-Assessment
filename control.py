from character import Character
from weapon import Weapon

class Control():
    def __init__(self):
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
                                "setweapon":self.setWeapon}
        self.player = None
                                       

    def runAll(self):
        self.terminal.run()
        activeRooms = [self.currentRoom]
        for object in self.eternalObjects:
            room = object.run()
            if room not in activeRooms and room is not None:
                activeRooms.append(room)
        for room in activeRooms:
            room.run()

    def command(self,command):
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
                    self.terminal.descriptionAdd(f"The {keyword} can't do that.")
        for object in self.currentRoom.items:
            if command.startswith(object.name.lower()):
                keyword = command[len(object.name.lower()):].lstrip()
                found = False
                for word in object.keywords:
                    print(word)
                    if keyword.startswith(word):
                        found = True
                if found:
                    object.do(keyword)
                    return
                else:
                    self.terminal.descriptionAdd(f"The {object.name} can't do that.")
                    return
        self.terminal.descriptionAdd("Not a valid command")
        self.terminal.descriptionAdd("")
    
    def move(self,command):
        # Move
        self.currentRoom = self.currentRoom.move(command[1])
        self.terminal.descriptionAdd("")
        self.currentRoom.describe()
        return

    def look(self,command):
        self.currentRoom.describe()

    def examine(self,command):
        # Examine
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
        foundPerson = False
        for thing in self.currentRoom.objects:
            if thing.name.lower() == " ".join(command[1:]) and isinstance(thing, Character):
                foundPerson = True
                self.player.fight(thing)
                break
        if not(foundPerson):
            self.terminal.descriptionAdd("There isn't a person called that here.")
    
    def talk(self,command):
        foundPerson = False
        person = command[1]
        command.pop(0)
        command.pop(0)
        command = " ".join(command)
        for thing in self.currentRoom.objects:
            if thing.name.lower() == person and isinstance(thing, Character):
                foundPerson = True
                thing.talk(self.player, command)
                break
        if not(foundPerson):
            self.terminal.descriptionAdd("There isn't a person called that here.")
            
    def watch(self,command):
        if command[1] == "stop":
            self.player.focus = None
            return
        foundItem = False
        for thing in self.currentRoom.objects:
            if thing.name.lower() == command[1]:
                self.player.focus = thing
                foundItem = True
                break
        if not(foundItem):
            self.terminal.descriptionAdd("There isn't such a thing.")

    def inventory(self,command):
        self.terminal.descriptionAdd("You have:")
        for i in self.player.inventory:
            self.terminal.descriptionAdd("\t"+i.name)

    def setWeapon(self,command):
        # Examine
        foundItem = False
        for thing in self.player.weaponsEquipped:
            if thing.name.lower() == command[1]:
                self.player.chosenWeapon = thing
                self.terminal.descriptionAdd(f"You are using {thing.name}")
                foundItem = True
        if not(foundItem):
            self.terminal.descriptionAdd("You don't have that.")
