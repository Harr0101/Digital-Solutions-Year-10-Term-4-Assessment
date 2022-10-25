from character import Character


class Player(Character):
    def __init__(self,description,startingWeapon, terminal, control):
        super().__init__("you",description,startingWeapon, None,terminal,control)

        self.focus = None
        self.focusCountMax = 20
        self.focusCount = self.focusCountMax
        
        self.control = control

    def run(self):
        if self.focus is not None:
            self.focusCount -= 1
            if self.focusCount < 0:
                self.focus.describe()
                self.focusCount = self.focusCountMax
        return self.control.currentRoom

    def talk(self):
        self.terminal.descriptionAdd("Talking to yourself now, are you going mad")
        
    def fight(self, opponent):
        if opponent != self:
            self.chosenWeapon.use(opponent,self)
        else:
            self.terminal.descriptionAdd("You punch yourself in the head")
            self.hp -= 1

