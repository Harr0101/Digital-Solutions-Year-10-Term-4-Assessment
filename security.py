from weapon import Weapon
from character import Character

class SecurityBot(Character):
    """
    A class to represent a security bot.

    ...

    Attributes
    ----------
    name : str
        name of bot
    description : str
        brief description of the bot
    chosenWeapon : Weapon
        the weapon object the bot is currently using
    currentRoom : Room
        the current room where the bot is
    hp : int
        hit points of the bot
    alive : boolean
        where the bot is currently alive, or killed
    speed : int
        how fast the bot can move
    perception : int
        how likely is the bot to spot something
    state : str
        what the bot is currently doing
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    path : list of str
        contains a list of directions the bot could follow to reach a destination
    moveTimer : int
        how quickly the bot moves
    attackTimer : int
        how many ticks between the bot's attacks
    activityTimer : int
        how long until the bot performs an action


    Methods
    -------
    run():
        chooses what action the bot does, returns current position

    describe():
        adds description to terminal

    talk(speaker,words):
        Ouput's bot's state to terminal

    fight():
        attacks player with weapon
    """
    def __init__(self,name,room,terminal,control):
        '''
        Constructs necessary attributes for the bot object

        Parameters:
            name(str) : name of bot
            room (Room) : the current room where the bot is
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''
        self.name = name
        self.description = "A secuirty bot programmed to eliminate all threats to the building."
        self.chosenWeapon = Weapon('Gun',"Sleek and black",3,terminal,control)
        self.currentRoom = room
        if room is not None:
            room.characters.append(self)
            room.objects.append(self)

        self.hp = 3
        self.alive = True
        self.speed = 30
        self.perception = 10
        self.state = "Searching for threat"

        self.path = []
        
        self.terminal = terminal
        self.control = control
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.moveTimer = self.terminal.loopsPerSecond * 12
        self.attackTimer = self.terminal.loopsPerSecond * 7
        self.activityTimer = self.moveTimer

    def run(self):
        '''
        Determines what the bot will do

        Parameters:
            None

        Returns
            currentRoom (Room): current location of bot
        '''
        if self.alive:
            self.activityTimer -= 1
            if (self.control.currentRoom == self.currentRoom):
                if self.control.currentRoom.forHumans:
                    if self.control.player.mechanics["Presence in Human Area"]:
                        action = "move"
                    else:
                        action = "fight"
                else:
                    if self.control.player.mechanics["Presence in Robot Area"]:
                        action = "move"
                    else:
                        action = "fight"
            else:
                action = "move"
            
            if action == "fight":
                if self.activityTimer < 0:
                    self.fight()
                    self.activityTimer = self.attackTimer
                    self.state = "Eliminating threat"
            
            if action == "move":
                if self.activityTimer < 0:
                    self.move()
                    self.activityTimer = self.moveTimer
                    self.state = "Searching for threat"
        return self.currentRoom

    def describe(self):
        ''' Outputs description of bot  to terminal '''
        self.terminal.descriptionAdd(self.description)
        if self.alive:
            self.terminal.descriptionAdd(f"{self.name.capitalize()} has a {self.chosenWeapon.name}")
        else:
            self.terminal.descriptionAdd("It is destroyed")

    def talk(self,speaker,words):
        '''
        Outputs bot's current state to the terminal

        Parameters:
            speaker (Character) : person who is saying something to the bot
            words (str) : what the character is saying to this bot

        Returns
            None
        '''
        self.terminal.descriptionAdd(f"{self} is {self.state}")
        
    def fight(self):
        ''' Attacks player with current weapon '''
        self.chosenWeapon.use(self.control.player, self)