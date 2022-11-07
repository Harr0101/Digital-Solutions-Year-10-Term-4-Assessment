from door import LockedDoor


class Item():
    def __init__(self,name,description,takeable,room,terminal,control):
        self.name = name
        self.description = description
        self.takeable = takeable
        self.terminal = terminal
        self.control = control
        self.keywords = []

        if room is not None:
            room.items.append(self)
            room.objects.append(self)

    def take(self):
        if self.takeable:
            self.terminal.descriptionAdd(f"You put {self.name} in your inventory")
            return True
        else:
            self.terminal.descriptionAdd(f"You can't put put {self.name} in your inventory")
            return False

    def describe(self):
        self.terminal.descriptionAdd(self.description)

    def run(self):
        pass



class Key(Item):
    def __init__(self,name,description,room,terminal,control):
        super().__init__(name,description,True,room,terminal,control)
        self.keywords =  ["unlock","lock"]

    def do(self,keyword):
        if keyword == 'unlock':
            for door in self.control.currentRoom.sides.values():
                if isinstance(door,LockedDoor):
                    door.unlock(self)
        elif keyword == 'lock':
            for door in self.control.currentRoom.sides.values():
                if isinstance(door,LockedDoor):
                    door.lock(self)

class Healing(Item):
    def __init__(self,room,terminal, control):
        super().__init__("Nanobots","Mends your body",True,room,terminal, control)
        self.keywords =  ["use"]

    def do(self,keyword):
        if keyword == "use":
            healthIncrease = 4
            self.control.player.hp += healthIncrease
            self.terminal.descriptionAdd(f"You healed {healthIncrease} hitpoints.")

class Note(Item):
    def __init__(self,paperDescription,message,room,takeable,terminal, control):
        description = f"A piece of {paperDescription}. It has words on that could be read if you pick it up."
        super().__init__("Note",description,takeable,room,terminal, control)
        self.message = message
        self.keywords = ["read"]

    def do(self,keyword):
        if keyword == "read":
            self.terminal.descriptionAdd(f"The note reads {self.message}.")