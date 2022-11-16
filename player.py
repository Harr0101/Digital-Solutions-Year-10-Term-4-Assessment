#DOCSTRINGS DONE
from character import Character
from robots import *


class Player(Character):
    """
    A class to represent the player.

    ...

    Attributes
    ----------
    hp : int 
        hit points that the player currently has
    focus : Object
        what the player is currently looking at that will be described repeatedly
    mechanics : dictionary
        what type of robot the player is currently inhabiting
    control : Control
        link to current control object

    Methods
    -------
    run():
        outputs description of focus to the terminal
    
    fight():
        attacks another person

    """
    def __init__(self,description,startingWeapon, terminal, control):
        '''
        Constructs necessary attributes for the person object

        Parameters:
            description (str) : brief description of the player
            startingweapons (Weapon) : the weapon object the player is currently using
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''
        super().__init__("you",description,startingWeapon, None,terminal,control)

        control.completedCheck.enemies -= 1
        self.hp = 1000000
        self.mechanics = sentry

        self.focus = None
        self.focusCountMax = 20
        self.focusCount = self.focusCountMax
        
        self.control = control

    def run(self):
        '''
        Describes what the player is focussing on

        Parameters:
            None

        Returns
            currentRoom (Room): current location of character
        '''

        if self.focus is not None:
            self.focusCount -= 1
            if self.focusCount < 0:
                self.focus.describe()
                self.focusCount = self.focusCountMax
        return self.control.currentRoom

    def describe(self):
        """ Adds description to terminal """
        type = self.mechanics["Name"]
        self.terminal.descriptionAdd(f"You are a {type}")

    def fight(self, opponent):
        ''' Attacks opponent with weapon '''
        if opponent != self:
            self.chosenWeapon.use(opponent,self)
        else:
            self.terminal.descriptionAdd("You punch yourself in the head")
            self.hp -= 1

