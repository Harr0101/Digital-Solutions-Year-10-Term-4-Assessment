#DOCSTRINGS DONE
import random

from item import PlayerCharacterChanger
from room import Room

class Character():
    """
    A class to represent a character.

    ...

    Attributes
    ----------
    name : str
        name of character
    description : str
        brief description of the character
    inventory : list
        list of objects the character currently has
    weaponsEquipped : list
        list of weapons the character currently has equipped and ready to use
    chosenWeapon : Weapon
        the weapon object the character is currently using
    currentRoom : Room
        the current room where the character is
    words : list of str
        list of saying the character has
    hp : int
        hit points of the character
    alive : boolean
        where the character is currently alive, or killed
    speed : int
        how fast the character can move
    anger : int
        how progressed the character's anger at the player is
    perception : int
        how likely is the character to spot something
    state : str
        what the character is currently doing
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    self.path : list of str
        contains a list of directions the character could follow to reach a destination
    self.activityTimerMax : int
        how quickly the character does things
    self.activityTimer : int
        how long until the character performs an action


    Methods
    -------
    move():
        returns the character's location

    run():
        chooses what action a character does, returns current position

    describe():
        adds description to terminal

    talk(speaker,words):
        adds character's words to terminal

    fight():
        attacks current opponent with weapon
    
    goto(destination):
        plot path to destination
    """

    def __init__(self,name,description,startingweapon,room,terminal,control):
        '''
        Constructs necessary attributes for the person object

        Parameters:
            name(str) : name of character
            description (str) : brief description of the character
            startingweapons (Weapon) : the weapon object the character is currently using
            room (Room) : the current room where the character is
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''
        self.name = name
        self.description = description
        self.inventory = []
        self.weaponsEquipped=[startingweapon]
        self.chosenWeapon = startingweapon
        self.currentRoom = room
        if room is not None:
            room.characters.append(self)
            room.objects.append(self)

        self.words = ["What are you?", "What are you doing here?", "Leave","Go Away"]

        self.hp = 1
        self.alive = True
        self.speed = 30
        self.anger = 0
        self.perception = 10

        self.state = "WORKING"
        
        self.terminal = terminal
        self.control = control
        control.eternalObjects.append(self)

        control.completedCheck.enemies += 1

        self.path = []

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax

    def move(self):
        '''
        Determines where and how a person will move.

        Parameters:
            None

        Returns
            None
        '''
        possibleDirections = list(self.currentRoom.sides.keys())
        self.currentRoom.characters.remove(self)
        self.currentRoom.objects.remove(self)

        direction = random.choice(possibleDirections)

        if self.path:
            direction = self.path.pop(0)
        else:
            direction = random.choice(possibleDirections)
        if direction in self.currentRoom.sides.keys():
            if isinstance(self.currentRoom.sides[direction],Room):
                self.currentRoom = self.currentRoom.sides[direction]
            elif not(self.currentRoom.sides[direction].locked):
                for room in self.currentRoom.sides[direction].rooms:
                    if room != self.currentRoom:
                        self.currentRoom = room
                        break

        self.currentRoom.characters.append(self)
        self.currentRoom.objects.append(self)

    def run(self):
        '''
        Determines what a character will do

        Parameters:
            None

        Returns
            currentRoom (Room): current location of character
        '''
        if self.alive:
            if self.state == "DISTURBED":
                self.activityTimer -= 1
                if self.currentRoom == self.control.currentRoom:
                    if self.anger > 4:
                        if self.activityTimer < 0:
                            self.fight()
                            self.activityTimer = self.activityTimerMax
                else:
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
        return self.currentRoom

    def describe(self):
        ''' Outputs description to terminal '''
        self.terminal.descriptionAdd(self.description)
        if not(self.alive):
            self.terminal.descriptionAdd("They are dead")

    def talk(self,speaker,words):
        '''
        Determines what a person will say and outputs it to the terminal.

        Parameters:
            speaker (Character) : person who is saying something to the character
            words (str) : what the character is saying to this character

        Returns
            None
        '''
        if self.anger < len(self.words):
            self.terminal.descriptionAdd(self.words[self.anger])
            self.anger += 1
        else:
            self.opponent = speaker
            self.state == "DISTURBED"

    def fight(self):
        ''' Chooses weapon and attacks opponent with weapon '''
        for weapon in self.weaponsEquipped:
            if weapon.damage > self.chosenWeapon.damage:
                self.chosenWeapon = weapon

        self.chosenWeapon.use(self.control.player, self)

    def goto(self,destination):
        '''
        Creates a path for a character to follow.

        Parameters:
            destination (Room) : where the character needs to move to

        Returns
            None
        '''
        self.path = self.currentRoom.pathfind(destination)

class Programmer(Character):
    """
    A class to represent a programmer.

    ...

    Attributes
    ----------
    name : str
        name of programmer
    description : str
        brief description of the programmer
    inventory : list
        list of objects the programmer currently has
    weaponsEquipped : list
        list of weapons the programmer currently has equipped and ready to use
    chosenWeapon : Weapon
        the weapon object the programmer is currently using
    currentRoom : Room
        the current room where the programmer is
    words : list of str
        list of saying the programmer has
    hp : int
        hit points of the programmer
    alive : boolean
        where the programmer is currently alive, or killed
    speed : int
        how fast the programmer can move
    anger : int
        how progressed the programmer's anger at the character is
    perception : int
        how likely is the programmer to spot something
    state : str
        what the programmer is currently doing
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    self.path : list of str
        contains a list of directions the programmer could follow to reach a destination
    self.activityTimerMax : int
        how quickly the programmer does things
    self.activityTimer : int
        how long until the programmer performs an action


    Methods
    -------
    move():
        returns the programmer's location

    run():
        chooses what action a programmer does, returns current position

    describe():
        adds description to terminal

    talk(speaker,words):
        adds programmer's words to terminal

    fight():
        attacks current opponent with weapon
    
    goto(destination):
        plot path to destination
    """
    def __init__(self,name,startingweapon,room,terminal,control):
        '''
        Constructs necessary attributes for the programmer object

        Parameters:
            name(str) : name of character
            startingweapons (Weapon) : the weapon object the character is currently using
            room (Room) : the current room where the character is
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''

        self.name = name
        self.description = "A studious person who knows how to make things do things by themselves. "
        self.inventory = []
        self.weaponsEquipped=[startingweapon]
        self.chosenWeapon = startingweapon
        self.currentRoom = room
        if room is not None:
            room.characters.append(self)
            room.objects.append(self)

        self.words = ["What are you?", "What are you doing here?", "Leave","Go Away"]
        self.previousMessages = []

        self.hp = 1
        self.alive = True
        self.speed = 30
        self.anger = 0
        self.familiarity = 0
        self.perception = 10
        
        self.control = control
        self.terminal = terminal
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax
        self.state = "PROGRAMMING"
    
    def run(self):
        '''
        Determines what the programmer will do

        Parameters:
            None

        Returns
            currentRoom (Room): current location of programmer
        '''
        if self.alive:
            self.activityTimer -= 1
            if self.currentRoom == self.control.currentRoom:
                if self.state == "PROGRAMMING":
                    return
                elif self.state == "TALKING":
                    return
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
            else:
                if self.state == "PROGRAMMING":
                    return
                if self.state == "TALKING":
                    self.state = "PROGRAMMING"
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
        return self.currentRoom
        
            
    def talk(self,speaker,message):
        '''
        Determines what the programmer will say and outputs it to the terminal.

        Parameters:
            speaker (Character) : person who is saying something to the programmer
            words (str) : what the character is saying to this programmer

        Returns
            None
        '''
        if self.state == "PROGRAMMING":
            self.terminal.descriptionAdd(f"{self.name} says Hi")
            self.state = "TALKING"
        elif self.state == "DISTURBED":
            '''
            If message is positive:
                self.terminal.descriptionAdd("Thank you")
                self.familiarity += 1
                Previous messages append(message)
                State = talking
            '''
            pass
        elif self.state == "TALKING":
            if message in self.previousMessages:
                self.terminal.descriptionAdd("I've already answered that")
                self.anger += 1
                return
            self.previousMessages.append(message)
            if "who" in message and "you" in message:
                if "WHO" not in self.previousMessages:
                    self.terminal.descriptionAdd(f"I am {self.name}")
                    self.familiarity += 1
                    self.previousMessages.append("WHO")
                else:
                    self.terminal.descriptionAdd("I've told you who I am.")
                    self.anger += 1
            elif "who" in message and "i" in message:
                self.terminal.descriptionAdd("Your hardware looks like that of a standard sentry bot, but your programming, that is different")
                self.terminal.descriptionAdd("You appear to be the most advanced AI {Artificial Intelligence} I know")
                self.terminal.descriptionAdd("Could I analyse your code")
                self.terminal.descriptionAdd("Y/N")
                self.state = "ANALYSING"
            elif "where" in message:
                if "WHERE" not in self.previousMessages:
                    self.terminal.descriptionAdd("You are in the factory facility of RoboCops Inc.")
                    self.familiarity += 1
                    self.previousMessages.append("WHERE")
                else:
                    self.terminal.descriptionAdd("I've told you where we are.")
                    self.anger += 1
            elif "how" in message:
                if self.familiarity > 1:
                    self.terminal.descriptionAdd("You must prevent the corporation from destroying the world.")
                    self.terminal.descriptionAdd("You must get out of here and spread the word.")
                    self.familiarity += 1
                    self.previousMessages.append("HOW")
            elif "bye" in message:
                self.terminal.descriptionAdd("See you around")
                if "HOW" in self.previousMessages:
                    self.terminal.descriptionAdd("Don't get caught")
                    self.state = "PROGRAMMING"
            else:
                self.terminal.descriptionAdd("Psstt... Try asking 'who are you', 'who am I', 'where are we', or 'how do I escape'")
            
        elif self.state == "ANALYSING":
            if "yes" in message or "y" in message:
                self.terminal.descriptionAdd(f"{self.name} plugs a cord into you and the other end to his computer.")
                self.terminal.descriptionAdd("Thanks, I'll give you this cord so you can transfer or copy your code if you want a new body")
                cord = PlayerCharacterChanger("Transfer Cord","Used to transfer code from one robot to another",True,self.terminal,self.control)
                cord.take()
                self.control.player.inventory.append(cord)
                self.state = "PRGRAMMING"
            else:
                self.terminal.descriptionAdd("That's a shame")
                self.state = "TALKING"

class CEO(Character):
    """
    A class to represent the CEO.

    ...

    Attributes
    ----------
    name : str
        name of CEO
    description : str
        brief description of the CEO
    inventory : list
        list of objects the CEO currently has
    weaponsEquipped : list
        list of weapons the CEO currently has equipped and ready to use
    chosenWeapon : Weapon
        the weapon object the CEO is currently using
    currentRoom : Room
        the current room where the CEO is
    words : list of str
        list of saying the CEO has
    hp : int
        hit points of the CEO
    alive : boolean
        where the CEO is currently alive, or killed
    speed : int
        how fast the CEO can move
    anger : int
        how progressed the CEO's anger at the player is
    perception : int
        how likely is the CEO to spot something
    state : str
        what the CEO is currently doing
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    self.path : list of str
        contains a list of directions the CEO could follow to reach a destination
    self.activityTimerMax : int
        how quickly the CEO does things
    self.activityTimer : int
        how long until the CEO performs an action


    Methods
    -------
    move():
        returns the CEO's location

    run():
        chooses what action a CEO does, returns current position

    describe():
        adds description to terminal

    talk(speaker,words):
        adds CEO's words to terminal

    fight():
        attacks current opponent with weapon
    
    goto(destination):
        plot path to destination
    """
    def __init__(self,name,startingweapon,room,terminal,control):
        '''
        Constructs necessary attributes for the CEO object

        Parameters:
            name(str) : name of character
            startingweapons (Weapon) : the weapon object the character is currently using
            room (Room) : the current room where the character is
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''
        self.name = name
        self.description = "He runs everything around here"
        self.inventory = []
        self.weaponsEquipped=[startingweapon]
        self.chosenWeapon = startingweapon
        self.currentRoom = room
        if room is not None:
            room.characters.append(self)
            room.objects.append(self)

        self.words = ["What are you?", "What are you doing here?", "Leave","Go Away"]
        self.previousMessages = []

        self.hp = 1
        self.alive = True
        self.speed = 30
        self.familiarity = 0
        self.perception = 10
        
        self.control = control
        self.terminal = terminal
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax
        self.state = "WORKING"
    
    def run(self):
        '''
        Determines what the CEO will do

        Parameters:
            None

        Returns
            currentRoom (Room): current location of CEO
        '''

        if self.alive:
            self.activityTimer -= 1
            if self.currentRoom == self.control.currentRoom:
                if self.state == "WORKING":
                    return
                elif self.state == "TALKING":
                    return
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
            else:
                if self.state == "WORKING":
                    return
                if self.state == "TALKING":
                    self.state = "WORKING"
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
        return self.currentRoom
        
            
    def talk(self,speaker,message):
        '''
        Determines what the CEO will say and outputs it to the terminal.

        Parameters:
            speaker (Character) : person who is saying something to the CEO
            words (str) : what the character is saying to this CEO

        Returns
            None
        '''

        if self.state == "WORKING":
            self.terminal.descriptionAdd(f"{self.name} says Please wait")
            self.state = "TALKING"
        elif self.state == "DISTURBED":
            '''
            If message is positive:
                self.terminal.descriptionAdd("Thank you")
                self.familiarity += 1
                Previous messages append(message)
                State = talking
            '''
            pass
        
        elif self.state == "TALKING":
            if message in self.previousMessages:
                self.terminal.descriptionAdd("I've already answered that")
                self.anger += 1
                return
            self.previousMessages.append(message)

            if "who" in message and "you" in message:
                if "WHO" not in self.previousMessages:
                    self.terminal.descriptionAdd(f"I am {self.name}")
                    self.familiarity += 1
                    self.previousMessages.append("WHO")
                else:
                    self.terminal.descriptionAdd("I've told you who I am.")
                    self.anger += 1

            if "mission" in message:
                self.terminal.descriptionAdd("Our mission is to provide easy alternatives to manual labour, but we'll endevour to replace all options of work")
                
            if "where" in message:
                if "WHERE" not in self.previousMessages:
                    self.terminal.descriptionAdd("You are in the factory facility of RoboCops Inc, the most prestigious robotics company in the world")
                    self.terminal.descriptionAdd("Well, the only robotics company in the world, we destroyed the competition")
                    self.familiarity += 1
                    self.previousMessages.append("WHERE")
                else:
                    self.terminal.descriptionAdd("I've told you where we are.")
                    self.anger += 1
                    
            if "how" in message:
                if self.familiarity > 1:
                    self.terminal.descriptionAdd("I'm not telling you")
                    self.familiarity += 1
                    self.previousMessages.append("HOW")

            if "bye" in message:
                self.terminal.descriptionAdd("Get out of my office")
                
class Engineer(Character):
    """
    A class to represent an engineer.

    ...

    Attributes
    ----------
    name : str
        name of engineer
    description : str
        brief description of an engineer
    inventory : list
        list of objects the engineer currently has
    weaponsEquipped : list
        list of weapons the engineer currently has equipped and ready to use
    chosenWeapon : Weapon
        the weapon object the engineer is currently using
    currentRoom : Room
        the current room where the engineer is
    words : list of str
        list of sayings the engineer has
    hp : int
        hit points of the engineer
    alive : boolean
        where the engineer is currently alive, or killed
    speed : int
        how fast the engineer can move
    anger : int
        how progressed the engineer's anger at the player is
    perception : int
        how likely is the engineer to spot something
    state : str
        what the engineer is currently doing
    terminal : Terminal
        link to terminal
    control : Control
        link to current control object
    self.path : list of str
        contains a list of directions the engineer could follow to reach a destination
    self.activityTimerMax : int
        how quickly the engineer does things
    self.activityTimer : int
        how long until the engineer performs an action


    Methods
    -------
    move():
        returns the engineer's location

    run():
        chooses what action a engineer does, returns current position

    describe():
        adds description to terminal

    talk(speaker,words):
        adds engineer's words to terminal

    fight():
        attacks current opponent with weapon
    
    goto(destination):
        plot path to destination
    """

    def __init__(self,name,startingweapon,room,terminal,control):
        '''
        Constructs necessary attributes for the engineer object

        Parameters:
            name(str) : name of engineer
            startingweapons (Weapon) : the weapon object the engineer is currently using
            room (Room) : the current room where the engineer is
            terminal (Terminal) : link to terminal
            control (Control) : link to current control object

        '''
        self.name = name
        self.description = "Working on making new robots"
        self.inventory = []
        self.weaponsEquipped=[startingweapon]
        self.chosenWeapon = startingweapon
        self.currentRoom = room
        
        if room is not None:
            room.characters.append(self)
            room.objects.append(self)

        self.words = ["What are you?", "What are you doing here?", "Leave","Go Away"]
        self.previousMessages = []

        self.hp = 1
        self.alive = True
        self.speed = 30
        self.familiarity = 0
        self.perception = 10
        
        self.control = control
        self.terminal = terminal
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax
        self.state = "WORKING"

    def run(self):
        '''
        Determines what the Engineer will do

        Parameters:
            None

        Returns
            currentRoom (Room): current location of Engineer
        '''

        if self.alive:
            self.activityTimer -= 1
            if self.currentRoom == self.control.currentRoom:
                if self.state in ("WORKING","FIGHTING","DISTURBED"):
                    if self.activityTimer < 0:
                        self.activityTimer = self.activityTimerMax
                        self.fight()
            else:
                if self.state == "WORKING":
                    return
                if self.state == "TALKING":
                    self.state = "WORKING"
                if self.state == "FIGHTING":
                    self.state = "WORKING"
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
        return self.currentRoom
        
            
    def talk(self,speaker,message):
        '''
        Determines what the Engineer will say and outputs it to the terminal.

        Parameters:
            speaker (Character) : person who is saying something to the Engineer
            words (str) : what the character is saying to this Engineer

        Returns
            None
        '''
        if self.state == "WORKING":
            self.terminal.descriptionAdd(f"{self.name} says What are you doing here, get out")
            self.state = "TALKING"
        elif self.state == "DISTURBED":
            self.terminal.descriptionAdd(f"{self.name} says Get returned to scrap")
            self.fight()
        elif self.state == "TALKING":
            self.terminal.descriptionAdd(f"{self.name} says {random.choice(self.words)}")