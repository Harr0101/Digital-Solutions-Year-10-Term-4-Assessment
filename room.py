class Room():
    rooms = []

    def __init__(self,name,description,terminal):
        self.name = name
        self.description = description
        self.terminal = terminal
        self.sides = {}
        self.items = []
        self.objects = []
        self.characters = []
        Room.rooms.append(self)

        self.pathFindingCounter = 9999
        self.pathFrom = None
        self.pathFindingDirection = None

    def run(self):
        for object in self.objects:
            object.run()

    def describe(self):
        self.terminal.descriptionAdd(f"You are in the {self.name}")
        self.terminal.descriptionAdd(self.description)
        if self.items:
            itemListString = ""
            for item in self.items:
                itemListString += item.name + " and "
            self.terminal.descriptionAdd(f"There is {itemListString[:-5]}.")

        if self.sides:
            doorListString = ""
            for door in self.sides.items():
                doorListString += door[1].name + " to the " + door[0] + " and "
            self.terminal.descriptionAdd(f"There is {doorListString[:-5]}.")

        if self.characters:
            characterListString = ""
            for character in self.characters:
                characterListString += character.name + " and "
            self.terminal.descriptionAdd(f"There is {characterListString[:-5]}.")

    def setDoor(self,door,direction):
        self.sides[direction] = door
        door.rooms.append(self)
        self.objects.append(door)

    
    def move(self,direction):
        direction = " ".join(direction)
        if direction in self.sides.keys():
            if isinstance(self.sides[direction],Room):
                return self.sides[direction]
            if not(self.sides[direction].locked):
                for room in self.sides[direction].rooms:
                    if room != self:
                        return room
            else:
                self.terminal.descriptionAdd("The door is locked.")
                return self
        else:
            if direction in ["north","south","east","west"]:
                self.terminal.descriptionAdd("You can't go that way")
            else:
                path = self.pathfind(direction)
                if path:
                    directions = "Go " + ", ".join(path)
                    self.terminal.descriptionAdd(directions)
                else:
                    self.terminal.descriptionAdd("You can't plot a course there")
            return self

    def pathfind(self,target):
        for room in Room.rooms:
            room.pathFindingCounter = 999
        self.pathFindingCounter = 0
        open_list = [self]
        cell = self


        while open_list:
            current = open_list.pop(0)
            for side in current.sides.items():
                dist = current.pathFindingCounter+1
                analysing = current.move([side[0]])
                if analysing.pathFindingCounter > dist:
                    analysing.pathFindingCounter = dist
                    analysing.pathFrom = current
                    analysing.pathFindingDirection = side[0]
                    open_list.append(analysing)
                    if analysing.name.lower() == target.lower():
                        cell = analysing
        path = None
        if cell:
            path = []
            while cell != None:
                path.append(cell.pathFindingDirection)
                cell = cell.pathFrom
                if cell == self:
                    break
            path.reverse()
        return path

class Area(Room):
    def __init__(self,name,description,terminal,room):
        super().__init__(name,description,terminal)
        self.room = room
        self.items = []
        self.objects = room.objects
        self.characters = room.characters

    def run(self):
        for thing in self.objects:
            thing.run()

    def describe(self):
        self.terminal.descriptionAdd(f"You are in the {self.name} of {self.room.name}")
        self.terminal.descriptionAdd(self.room.description)
        self.terminal.descriptionAdd(self.description)
        if self.items:
            itemListString = ""
            for item in self.items:
                itemListString += item.name + " and "
            self.terminal.descriptionAdd(f"There is {itemListString[:-5]}.")

        if self.sides:
            doorListString = ""
            for side in self.sides.items():
                doorListString += side[1].name + " to the " + side[0] + " and "
            self.terminal.descriptionAdd(f"There is {doorListString[:-5]}.")

        if self.characters:
            characterListString = ""
            for character in self.characters:
                if character.alive:
                    characterListString += character.name + " and "
                else:
                    characterListString += "a dead " + character.name + " and "
            self.terminal.descriptionAdd(f"There is {characterListString[:-5]}.")
    """
    def move(self, direction):
        direction = " ".join(direction)
        if direction in self.sides.keys():
            if isinstance(self.sides[direction],Room):
                return self.sides[direction]
            if not(self.sides[direction].locked):
                for room in self.sides[direction].rooms:
                    if room != self:
                        return room
            else:
                self.terminal.descriptionAdd("The door is locked.")
                return self
        else:
            path = self.pathfind(direction)
            if path:
                directions = "Go " + ", ".join(path)
                self.terminal.descriptionAdd(directions)
            else:
                self.terminal.descriptionAdd("You can't plot a course there")
                
            return self
    """

    def setDoor(self,door,direction):
        self.sides[direction] = door
        door.rooms.append(self)
        self.objects.append(door)
   