#DOCSTRINGS DONE
from door import LockedDoor


class Item():
    """
    A class to represent an item.

    ...

    Attributes
    ----------
    name : str
        name of item
    description : str
        brief description of the item
    takeable : bool
        item is able to be picked up by characters
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    keywords : list
        words that can be used to make the item do something


    Methods
    -------
    take():
        returns if item can be taken

    describe():
        adds description to terminal

    run():
        legacy function for compatibility

    """

    def __init__(self,name,description,takeable,room,terminal,control):
        '''
        Constructs necessary attributes for the item object

        Parameters:
            name(str) : name of item
            description (str) : brief description of the item
            takeable (bool) : if item can be picked up and moved between rooms
            room (Room) : current location of the item if any
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object
        '''
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
        '''
        Determines if the item can be picked up and outputs to terminal

        Parameters:
            None

        Returns
            takeable (bool) : item can be picked up
        '''
        if self.takeable:
            self.terminal.descriptionAdd(f"You put {self.name} in your inventory")
            return True
        else:
            self.terminal.descriptionAdd(f"You can't put put {self.name} in your inventory")
            return False

    def describe(self):
        ''' Outputs description to terminal '''
        self.terminal.descriptionAdd(self.description)

    def run(self):
        ''' Runs every game loop, but does nothing, included for compatibility'''
        pass



class Key(Item):
    """
    A class to represent a key used to unlock or lock a door or chest.

    ...

    Attributes
    ----------
    keywords : list
        words that can be used to make the item do something


    Methods
    -------
    do(keyword):
        attempts to use key to lock or unlock all locked items in the room


    """
    def __init__(self,name,description,room,terminal,control):
        '''
        Constructs necessary attributes for the key object

        Parameters:
            name(str) : name of key
            description (str) : brief description of the key
            takeable (bool) : if item can be picked up and moved between rooms
            room (Room) : current location of the item if any
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object
        '''
        super().__init__(name,description,True,room,terminal,control)
        self.keywords =  ["unlock","lock"]

    def do(self,keyword):
        '''
        Attempts to lock and unlock all locked items in currentRoom

        Parameters:
            keyword (str) : what was typed in the terminal to activate the item

        Returns
            None
        '''
        if keyword == 'unlock':
            for door in self.control.currentRoom.sides.values():
                if isinstance(door,LockedDoor):
                    door.unlock(self)
        elif keyword == 'lock':
            for door in self.control.currentRoom.sides.values():
                if isinstance(door,LockedDoor):
                    door.lock(self)

class Healing(Item):
    """
    A class to represent a healing item

    ...

    Attributes
    ----------
    keywords : list
        words that can be used to make the healing item do something


    Methods
    -------
    do(keyword):
        increases the player's hitpoints

    """
    def __init__(self,room,terminal, control):
        '''
        Constructs necessary attributes for the key object

        Parameters:
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object
        '''
        super().__init__("Nanobots","Mends your body",True,room,terminal, control)
        self.keywords =  ["use"]

    def do(self,keyword):
        '''
        Increases health of player by specified amount

        Parameters:
            keyword (str) : what was typed in the terminal to activate the item

        Returns
            None
        '''
        if keyword == "use":
            healthIncrease = 4
            self.control.player.hp += healthIncrease
            self.terminal.descriptionAdd(f"You healed {healthIncrease} hitpoints.")

class Note(Item):
    """
    A class to represent a piece of paper that something is written on

    ...

    Attributes
    ----------
    message : str
        what is currently written on the note

    keywords : list
        words that can be used to make the item do something


    Methods
    -------
    do(keyword):
        outputs message to terminal


    """
    def __init__(self,paperDescription,message,room,takeable,terminal, control):
        '''
        Constructs necessary attributes for the note object

        Parameters:
            paperDescrition(str) : a description of the type of paper the message is written on
            message (str) : what is written on the paper
            room (Room) : current location of the item if any
            takeable (bool) : if the note can be removed from current room
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object
        '''
        description = f"A piece of {paperDescription}. It has words on that could be read if you pick it up."
        super().__init__("Note",description,takeable,room,terminal, control)
        self.message = message
        self.keywords = ["read"]

    def do(self,keyword):
        '''
        Outputs the message to terminal

        Parameters:
            keyword (str) : what was typed in the terminal to activate the item

        Returns
            None
        '''
        if keyword == "read":
            self.terminal.descriptionAdd(f"The note reads {self.message}.")