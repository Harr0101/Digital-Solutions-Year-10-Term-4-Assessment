
class CompletionCheck():
    def __init__(self,control,terminal, exit):
        self.control = control
        self.terminal = terminal
        self.exit = exit
        self.enemies = 0

    def run(self):
        # If player was exitted building
        if self.control.currentRoom == self.exit:
            return True
        
        # If player has killed all enemies
        if not(self.enemies):
            return True

        # The game is not completed
        return False