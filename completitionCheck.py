#DOCSTRINGS DONE

class CompletionCheck():
    """
    A class to represent a character.

    ...

    Attributes
    ----------
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    exit : Room
        the room that will win the game when the character enters it
    enemies : int
        number of enemies currently in existence
    
    Methods
    -------
    run():
        returns if exit conditions are met
    """
    def __init__(self,control,terminal, exit):
        '''
        Constructs necessary attributes for the completion checker object

        Parameters:
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object
            exit (Room) : the room that will allow the player to exit the game

        '''
        self.control = control
        self.terminal = terminal
        self.exit = exit
        self.enemies = 0       

    def run(self):
        '''
        Determines if the player has completed the game.

        Parameters:
            None

        Returns
            finished (boolean) : If the player has completed any finishing conditions
        '''
        # If player was exitted building
        if self.control.currentRoom == self.exit:
            return True
        
        # If player has killed all enemies
        if not(self.enemies):
            return True

        # The game is not completed
        return False