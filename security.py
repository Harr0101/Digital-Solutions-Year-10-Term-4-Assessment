import random

from weapon import Weapon
from character import Character

class SecurityBot(Character):
    def __init__(self,name,room,terminal,control):
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
        
        self.terminal = terminal
        self.control = control
        control.eternalObjects.append(self)
        control.completedCheck.enemies += 1

        self.moveTimer = 150
        self.attackTimer = 90
        self.activityTimer = self.moveTimer

    def run(self):
        if self.alive:
            self.activityTimer -= 1
            if self.currentRoom == self.control.currentRoom:
                if self.activityTimer < 0:
                    self.fight()
                    self.activityTimer = self.attackTimer
                    self.state = "Eliminating threat"
            else:
                if self.activityTimer < 0:
                    self.move()
                    self.activityTimer = self.moveTimer
                    self.state = "Searching for threat"
        return self.currentRoom

    def describe(self):
        self.terminal.descriptionAdd(self.description)
        if self.alive:
            self.terminal.descriptionAdd(f"{self.name.capitalize()} has a {self.chosenWeapon.name}")
        else:
            self.terminal.descriptionAdd("It is destroyed")

    def talk(self,speaker,words):
        self.terminal.descriptionAdd(f"{self} is {self.state}")
        
    def fight(self):
        self.chosenWeapon.use(self.control.player, self)