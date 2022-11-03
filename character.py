import random

from item import Item

class Character():
    def __init__(self,name,description,startingweapon,room,terminal,control):
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

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax

    def move(self):
        possibleDirections = list(self.currentRoom.sides.keys() )
        self.currentRoom.characters.remove(self)
        self.currentRoom.objects.remove(self)
        self.currentRoom = self.currentRoom.move(random.choice(possibleDirections))
        self.currentRoom.characters.append(self)
        self.currentRoom.objects.append(self)
        

    def run(self):
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
        self.terminal.descriptionAdd(self.description)
        if not(self.alive):
            self.terminal.descriptionAdd("He is dead")

    def talk(self,speaker,words):
        if self.anger < len(self.words):
            self.terminal.descriptionAdd(self.words[self.anger])
            self.anger += 1
        else:
            self.opponent = speaker
            self.state == "DISTURBED"

    def fight(self):
        for weapon in self.weaponsEquipped:
            if weapon.damage > self.chosenWeapon.damage:
                self.chosenWeapon = weapon

        self.chosenWeapon.use(self.opponent, self)
        
class Programmer(Character):
    def __init__(self,name,startingweapon,room,terminal,control):
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
            if "who" in message and "i" in message:
                self.terminal.descriptionAdd("Your hardware looks like that of a standard sentry bot, but your programming, that is different")
                self.terminal.descriptionAdd("You appear to be the most advanced AI {Artificial Intelligence} I know")
                self.terminal.descriptionAdd("Could I analyse your code")
                self.terminal.descriptionAdd("Y/N")
                self.state = "ANALYSING"
            if "where" in message:
                if "WHERE" not in self.previousMessages:
                    self.terminal.descriptionAdd("You are in the factory facility of RoboCops Inc.")
                    self.familiarity += 1
                    self.previousMessages.append("WHERE")
                else:
                    self.terminal.descriptionAdd("I've told you where we are.")
                    self.anger += 1
            if "how" in message:
                if self.familiarity > 1:
                    self.terminal.descriptionAdd("You must prevent the corporation from destroying the world.")
                    self.terminal.descriptionAdd("You must get out of here and spread the word.")
                    self.familiarity += 1
                    self.previousMessages.append("HOW")
            if "bye" in message:
                self.terminal.descriptionAdd("See you around")
                if "HOW" in self.previousMessages:
                    self.terminal.descriptionAdd("Don't get caught")
                    self.state = "PROGRAMMING"
            
        elif self.state == "ANALYSING":
            if "yes" in message or "y" in message:
                self.terminal.descriptionAdd(f"{self.name} plugs a cord into you and the other end to his computer.")
                self.terminal.descriptionAdd("Thanks, I'll give you this cord so you can transfer or copy your code if you want a new body")
                cord = Item("Transfer Cord","Used to transfer code from one robot to another",True,self.terminal,self.control)
                cord.take()
                self.control.player.inventory.append(cord)
                self.state = "PRGRAMMING"
            else:
                self.terminal.descriptionAdd("That's a shame")
                self.state = "TALKING"

class CEO(Character):
    def __init__(self,name,startingweapon,room,terminal,control):
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
        self.perception = 10
        
        self.control = control
        self.terminal = terminal
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.activityTimerMax = 120
        self.activityTimer = self.activityTimerMax
        self.state = "WORKING"
    
    def run(self):
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
            if "who" in message and "i" in message:
                self.terminal.descriptionAdd("Your hardware looks like that of a standard sentry bot, but your programming, that is different")
                self.terminal.descriptionAdd("You appear to be the most advanced AI {Artificial Intelligence} I know")
                self.terminal.descriptionAdd("Could I analyse your code")
                self.terminal.descriptionAdd("Y/N")
                self.state = "ANALYSING"
            if "where" in message:
                if "WHERE" not in self.previousMessages:
                    self.terminal.descriptionAdd("You are in the factory facility of RoboCops Inc.")
                    self.familiarity += 1
                    self.previousMessages.append("WHERE")
                else:
                    self.terminal.descriptionAdd("I've told you where we are.")
                    self.anger += 1
            if "how" in message:
                if self.familiarity > 1:
                    self.terminal.descriptionAdd("You must prevent the corporation from destroying the world.")
                    self.terminal.descriptionAdd("You must get out of here and spread the word.")
                    self.familiarity += 1
                    self.previousMessages.append("HOW")
            if "bye" in message:
                self.terminal.descriptionAdd("See you around")
                if "HOW" in self.previousMessages:
                    self.terminal.descriptionAdd("Don't get caught")
                    self.state = "PROGRAMMING"
            
        elif self.state == "ANALYSING":
            if "yes" in message or "y" in message:
                self.terminal.descriptionAdd(f"{self.name} plugs a cord into you and the other end to his computer.")
                self.terminal.descriptionAdd("Thanks, I'll give you this cord so you can transfer or copy your code if you want a new body")
                cord = Item("Transfer Cord","Used to transfer code from one robot to another",True,self.terminal,self.control)
                cord.take()
                self.control.player.inventory.append(cord)
                self.state = "PRGRAMMING"
            else:
                self.terminal.descriptionAdd("That's a shame")
                self.state = "TALKING"