from door import LockedDoor


class Item():
    def __init__(self,name,description,takeable,terminal, control):
        self.name = name
        self.description = description
        self.takeable = takeable
        self.terminal = terminal
        self.control = control
        self.keywords = []

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
    def __init__(self,name,description,terminal,control):
        super().__init__(name,description,True,terminal,control)
        self.keywords =  ["unlock","lock"]

    def do(self,keyword):
        if keyword == 'unlock':
            for door in self.control.currentRoom.doors.values():
                if isinstance(door,LockedDoor):
                    door.unlock(self)
        elif keyword == 'lock':
            for door in self.control.currentRoom.doors.values():
                if isinstance(door,LockedDoor):
                    door.lock(self)