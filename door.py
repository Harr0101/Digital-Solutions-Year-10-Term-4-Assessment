
class Door():
    def __init__(self,name,description,terminal):
        self.name = name
        self.descrition = description
        self.rooms = []
        self.terminal = terminal
        self.locked = False
    def describe(self):
        self.terminal.descriptionAdd(self.descrition)
    def run(self):
        pass

class LockedDoor(Door):
    def __init__(self,name,description,key,terminal):
        super().__init__(name,description,terminal)
        self.key = key
        self.locked = True

    def unlock(self,key):
        if self.key == key:
            if self.locked:
                self.terminal.descriptionAdd("You unlock the door.")
                self.locked = False

    def lock(self,key):
        if not(self.locked):
            self.terminal.descriptionAdd("You lock the door.")
            self.locked = True

    def describe(self):
        if self.locked:
            self.terminal.descriptionAdd(self.descrition + ". It is locked.")
        else:
            self.terminal.descriptionAdd(self.descrition + "It is unlocked.")

