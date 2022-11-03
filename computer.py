import random
import string

from item import Item,Healing
from weapon import Weapon

class Computer(Item):
    def __init__(self,room,terminal, control):
        super().__init__("computer","Attached to the local intranet",False,room,terminal,control)
        self.keywords = []
        self.state = "Logged Out"
        self.items = {"sword":(lambda :Weapon("Sword","Cuts",4,room,terminal,control)),"blaster":(lambda: Weapon("Blaster","Shoots stuff with pure energy",2,room,terminal,control)),"nanobots":(lambda: Healing(room,terminal,control))}

        self.homeScreenIcons = ["file explorer","word processor", "manufacturing control"]
        manufacturingHints = ["Go to manufacturing application", "Choose what is made", "Visit relevant muanufacturing room ro pick up item."]
        masterPlan = ["We will kill half the world population, and remove power facilities.","This will be started in 1 day."]
        self.fileExplorerFiles = {"master plan":masterPlan,"manufacturing":manufacturingHints}

        self.words = ""
        self.password = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    
    def getPassword(self):
        return self.password
    
    def describe(self):
        self.terminal.descriptionAdd(self.description)

    def run(self):
        if self.state != "Logged Out":
            if self.state == "Home Screen":
                self.description = "You are on the home screen, the options are: " + ', '.join(self.homeScreenIcons)
                self.keywords = self.homeScreenIcons.copy()
                self.keywords.append("logout")

            elif self.state == "file explorer":
                self.description = "The File explorer is open, the files are: " + ', '.join(self.fileExplorerFiles.keys())
                self.keywords = list(self.fileExplorerFiles.keys())
                self.keywords.append("exit")

            elif self.state in self.fileExplorerFiles.keys():
                for line in self.fileExplorerFiles[self.state]:
                    self.terminal.descriptionAdd(line)
                self.state = "file explorer"

            elif self.state == "word processor":
                self.description = "The file says " + self.words + ". You can write or clear."
                self.keywords = ["write","exit","clear"]

            elif self.state == "manufacturing control":
                self.description = "Welcome to manufacturing, you can make: " + ', '.join(self.items.keys())
                self.keywords = list(self.items.keys())
                self.keywords.append("exit")
        else:
            self.description = "The login screen"
            self.keywords = ["enter password"]

    def do(self,keyword):
        if self.state != "Logged Out":
            if self.state == "Home Screen":
                if keyword in self.homeScreenIcons:
                    self.state = keyword
                elif keyword == "logout":
                    self.state = "Logged Out"
                
            elif self.state == "file explorer":
                if keyword in self.fileExplorerFiles:
                    self.state = keyword
                elif keyword == "exit":
                    self.state = "Home Screen"

            elif self.state == "word processor":
                if keyword[:5] == "write":
                    self.words += keyword[5:]
                elif keyword == "exit":
                    self.state = "Home Screen"
                elif keyword == "clear":
                    self.words = ""

            elif self.state == "manufacturing control":
                if keyword in self.items.keys():
                    newItem = (self.items[keyword])()
                    self.control.currentRoom.items.append(newItem)
                    self.control.currentRoom.objects.append(newItem)
                elif keyword == "exit":
                    self.state = "Home Screen"

        else:
            if keyword.startswith("enter password"):
                password = keyword[15:]
                if password == self.password:
                    self.state = "Home Screen"