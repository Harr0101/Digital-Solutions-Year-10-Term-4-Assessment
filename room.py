#DOCSTRINGS DONE
class Room():
    """
    A class to represent a room.

    ...

    Attributes
    ----------
    name : str
        name of room
    description : str
        brief description of the room
    terminal : Terminal
        link to terminal
    sides : dict
        what is on each side of the room
    items : list
        items currently in the room
    objects : list
        list of objects that can be run, includes items, characters, and doors
    characters : list
        list of characters currently in room
    pathFindingCounter : int
        distance from target room to this room via the shortest root, only used for pathfinding
    pathFrom : Room
        previous room on the shortest route from target to this room, only used for pathfinding
    pathFindingDirection : str
        which direction a character needs to move in to get to the right location

    forHumans : bool
        if a room is designed for human use

    Methods
    -------
    run():
        runs all objects in current room 
    
    describe():
        adds to terminal the current room and what items and characters are in the room
    
    setDoor(door,direction):
        ammends sides to include new door
    
    move(direction):
        returns the room in that direction

    pathfind(target):
        returns directions required to be taken to get to the target
    
    """

    rooms = []

    def __init__(self,name,description,forHumans,terminal):
        '''
        Constructs necessary attributes for the room object

        Parameters:
            name(str) : name of room
            description (str) : brief description of the room
            forHumans (bool) : if the room is designed for human use
            terminal (Terminal) : link to terminal

        '''
        self.name = name
        self.description = description
        self.terminal = terminal
        self.sides = {}
        self.items = []
        self.objects = []
        self.characters = []
        self.forHumans = forHumans
        Room.rooms.append(self)

        self.pathFindingCounter = 9999
        self.pathFrom = None
        self.pathFindingDirection = None

    def run(self):
        """ Runs all objects in the room """
        for object in self.objects:
            object.run()

    def describe(self):
        """
        States the current room and room description
        States which items are in the room
        States what doors are in the room
        states what charcters are in the room if any
        """
        self.terminal.descriptionAdd(f"You are in the {self.name}","bold")
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
        '''
        Adds door to room and room to door

        Parameters:
            door (Door) : door object which is being assigned to the room
            direction (str) : which wall will the door be placed on

        Returns
            None
        '''
        self.sides[direction] = door
        door.rooms.append(self)
        self.objects.append(door)

    
    def move(self,direction):
        '''
        Determines what room a character will move to if they move in the direciont

        Parameters:
            direction (str) : which way the character wishes to move 

        Returns
            None
        '''
        
        if direction:
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
        else:
            self.terminal.descriptionAdd("Please specify a direction")
            return self

    def pathfind(self,target):
        """
        Finds the shortest route to the target area

        Resets pathfinding variable
        Moves through each door, going outwards from current room
        In each room record where you came from and what the room was

        Find shortest path by backtracking
        """
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
        else:
            path = ""
        return path

class Area(Room):
    """
    A class to represent an area of a room.

    ...

    Attributes
    ----------
    room : Room
        main room of which this object is a subroom
    objects : list
        objects list in current main room
    
    Methods
    -------
    run():
        runs all objects in current room 
    
    describe():
        adds to terminal the current room and what items and characters are in the room
    
    setDoor(door,direction):
        ammends sides to include new door
    
    move(direction):
        returns the room in that direction

    pathfind(target):
        returns directions required to be taken to get to the target
    
    """
    def __init__(self,name,description,terminal,room):
        '''
        Constructs necessary attributes for the area object

        Parameters:
            name(str) : name of room
            description (str) : brief description of the room
            forHumans (bool) : if the room was designed for human use
            terminal (Terminal) : link to terminal
            room (Room) : main room of which this object is a sub room

        '''
        super().__init__(name,description,room.forHumans,terminal)
        self.room = room
        self.objects = room.objects

    def describe(self):
        """
        States the current room and room description
        States which items are in the room
        States what doors are in the room
        states what charcters are in the room if any
        """
        self.terminal.descriptionAdd(f"You are in the {self.name} of {self.room.name}","bold")
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

   