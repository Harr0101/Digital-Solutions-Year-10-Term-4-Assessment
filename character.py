import random

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
        
        self.terminal = terminal
        self.control = control
        control.eternalObjects.append(self)

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
        if self.alive:
            self.terminal.descriptionAdd(f"{self.name.capitalize()} has a {self.chosenWeapon.name}")
        else:
            self.terminal.descriptionAdd("He is dead")

    def talk(self,speaker,words):
        if self.anger < len(self.words):
            self.terminal.descriptionAdd(self.words[self.anger])
            self.anger += 1
        else:
            self.opponent = speaker
            self.fight()

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

        self.hp = 1
        self.alive = True
        self.speed = 30
        self.anger = 0
        self.perception = 10
        self.currentRoom = None
        
        self.control = control
        self.terminal = terminal
        control.eternalObjects.append(self)

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
                elif self.state == "DISTURBED":
                    if self.activityTimer < 0:
                        self.move()
                        self.activityTimer = self.activityTimerMax
        return self.currentRoom
        
            
    def talk(self,speaker,words):
        speech = "Hi"
        self.terminal.descriptionAdd(f"{self.name} says {speech}")
        self.state = "TALKING"
