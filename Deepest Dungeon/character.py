#character.py

class Character():
    def __init__(self,name):
        # initialises the character object
        self.name = name
        self.description = None
        self.conversation = None

    def describe(self):
        # sends a description of the character to the screen
        print(f"{self.name} is here, {self.description}")

    def hug(self):
        # the character responds to a hug
        print(f"{self.name} doesn't want to hug you.")

    def fight(self,item):
        # the character responds to a threat
        print(f"{self.name} doesn't want to fight you")

    def talk(self):
        # send the conversation to the screen
        if self.conversation is not None:
            print(f"{self.name}: {self.conversation}")
        else:
            print(f"{self.name} doesn't want to talk to you.")


class Friend(Character):
    def __init__(self,name):
        #initialise the friend object by call the character initalise
        super().__init__(name)

    def hug(self):
        # The friend responds to a hug
        print(f"{self.name} hugs you back.")


class Enemy(Character):
    num_of_enemy = 0

    def __init__(self,name):
        #initialise the enemy object by calling the character initilaise
        super().__init__(name)
        self.weakness = None
        Enemy.num_of_enemy += 1

    def fight(self,item):
        # fights the enemy with provided item and returns if player survives
        if item == self.weakness:
            print(f"You strike {self.name} down with {item}.")
            Enemy.num_of_enemy -= 1
            return True
        else:
            print(f"{self.name} crushes you. Puny adventurer")
            return False
    
    def get_num_of_enemy():
        # returns the number of enemies present in the dungeon
        return Enemy.num_of_enemy