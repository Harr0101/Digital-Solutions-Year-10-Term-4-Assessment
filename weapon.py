from item import Item
from player import Player

class Weapon(Item):
    def __init__(self,name,description,damage,terminal,control):
        self.damage = damage
        super().__init__(name,description,True, None, terminal,control)

    def use(self,target,user):
        target.hp -= self.damage
        self.terminal.descriptionAdd(f"{user.name} hurt {target.name} for {self.damage} damage with a {self.name}.")
        target.anger = 5
        target.opponent = user
        if target.hp <= 0:
            if isinstance(target,Player):
                self.terminal.descriptionAdd(f"You died.")
                self.terminal.stopCommands()
            else:
                self.terminal.descriptionAdd(f"You killed {target.name}")
                target.alive = False
                self.control.completedCheck.enemies -= 1



    def take(self):
        self.terminal.descriptionAdd(f"You equipped {self.name}. It does {self.damage} damage.")
        return True