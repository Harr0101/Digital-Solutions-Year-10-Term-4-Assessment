class Door():
    """
    A class to represent a door.
    Links rooms together indirectly
    ...
    Attributes
    ----------
    name : str
        name of room
    description : str
        brief description of the room
    rooms : list
        list of rooms that the door connects to
    terminal : Terminal
        link to terminal
    locked : bool
        if door is currently able to be opened

    Methods
    -------
    describe():
        describes the appearence of the door

    run():
        legacy function needed for more efficient iteration

    """
    def __init__(self,name,description,terminal):
        '''
        Constructs necessary attributes for the door object

        Parameters:
            name(str) : name of door
            description (str) : brief description of the door
            terminal (Terminal) : link to terminal
        '''
        self.name = name
        self.descrition = description
        self.rooms = []
        self.terminal = terminal
        self.locked = False
    def describe(self):
        ''' Outputs description to terminal '''
        self.terminal.descriptionAdd(self.descrition)
    def run(self):
        ''' Runs every game loop, but does nothing, included for compatibility'''
        pass

    
class LockedDoor(Door):
    """
    A class to represent a door that can be locked.
    Links rooms together indirectly
    ...
    Attributes
    ----------
    name : str
        name of room
    description : str
        brief description of the room
    rooms : list
        list of rooms that the door connects to
    terminal : Terminal
        link to terminal
    key : Key
        key object that will unlock the door
    locked : bool
        if door is currently able to be opened

    Methods
    -------
    run():
        legacy function needed for more efficient iteration

    unlock(key):
        unlocks door if key is correct

    lock(key):
        locks door so that it can't be used

    describe():
        descripes the door's current state
    """
    def __init__(self,name,description,key,terminal):
        '''
        Constructs necessary attributes for the door object

        Parameters:
            name (str) : name of door
            description (str) : brief description of the door
            key (Key) : key that will unlock or lock the door
            terminal (Terminal) : link to terminal
        '''
        super().__init__(name,description,terminal)
        self.key = key
        self.locked = True

    def unlock(self,key):
        '''
        Unlocks the door if the correct key is used

        Parameters:
            key (Key) : object that is trying to be used to unlock the door

        Returns
            None
        '''
        if self.key == key:
            if self.locked:
                self.terminal.descriptionAdd("You unlock the door.")
                self.locked = False

    def lock(self,key):
        '''
        Locks the door 

        Parameters:
            key (Key) : object that is trying to be used to lock the door

        Returns
            None
        '''
        if not(self.locked):
            self.terminal.descriptionAdd("You lock the door.")
            self.locked = True

    def describe(self):
        ''' Outputs description to terminal '''
        if self.locked:
            self.terminal.descriptionAdd(self.descrition + ". It is locked.")
        else:
            self.terminal.descriptionAdd(self.descrition + "It is unlocked.")

