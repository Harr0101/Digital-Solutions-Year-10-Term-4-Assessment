# main.py

from turtle import back
from room import Room
from character import Character, Friend, Enemy
from item import Item

#create rooms
cavern = Room("Cavern")
cavern.description = "A room so big that the light of your torch doesn't reach the walls."

armoury = Room("Armoury")
armoury.description = "The walls are lined with racks that once held weapons and armour."

lab = Room("Laboratory")
lab.description = "A strange odour hangs in a room filled with unknowable contraptions."

torture_chamber = Room("Torture chamber")
torture_chamber.description = "Dried blood coats the floor and instruments of torture line the walls."

# Link rooms together
cavern.link_rooms(armoury,"south")
armoury.link_rooms(cavern,"north")
armoury.link_rooms(lab,"east")
armoury.link_rooms(torture_chamber,"west")
torture_chamber.link_rooms(armoury, "east")
lab.link_rooms(armoury,"west")

# create characters
ugine = Enemy("Ugine")
ugine.description = "a huge troll with rotting teeth."
ugine.weakness = "cheese"

nigel = Friend("Nigel")
nigel.description = "a burly dward with golden beads woven through his beard."
nigel.conversation = "Well youngman, what are you doing here?"

monster = Enemy("Usame")
monster.description = "a mostrous being covered in too many tentacles to count."
monster.conversation = "GET OUT OF MY CAVERN."
monster.weakness = "acid"

# add characters to rooms
armoury.character = ugine
lab.character = nigel
cavern.character = monster

# Create items
cheese = Item("Cheese")
cheese.description = "super smelly"

chair = Item("chair")
chair.description = "designed to be sat on"

elmo = Item("elmo")
elmo.description = "wanting to be tickled"

acid = Item("acid")
acid.description = "very strong"

sword = Item("sword")
sword.descrition = "It was your father's/"

# add items to room
cavern.item = chair
armoury.item = elmo
lab.item = cheese
torture_chamber.item = acid

# initialisng variables
current_room = cavern
running = True
backpack = [sword]

# ---- MAIN LOOP ----
while running:
    current_room.describe()

    command = input("> ").lower()

    # Move
    if command in ["north","south","east","west"]:
        current_room = current_room.move(command)
    
    # Talk
    elif command == "talk":
        if current_room.character is not None:
            current_room.character.talk()
        else:
            print("There is no one here to talk to.")

    # Hug
    elif command == "hug":
        if current_room.character is not None:
            current_room.character.hug()
        else:
            print("There is no one here to hug.")

    # Fight
    elif command == "fight":
        if current_room.character is not None:
            weapon = input("What will you fight with? > ").lower()
            available_weapons = []
            for item in backpack:
                available_weapons.append(item.name)
            if weapon in available_weapons:
                if current_room.character.fight(weapon):
                    current_room.character = None
                    if Enemy.get_num_of_enemy() == 0:
                        print("You have slain all the enemies. You are victorious.")
                        running = False
                else:
                    running = False
            else:
                print(f"You don't have {weapon}")
                print(f"{current_room.character.name} strikes you down.")
                running = False
        else:
            print("There is no one here to fight.")

    # Take
    elif command == "take":
        if current_room.item is not None:
            backpack.append(current_room.item)
            print(f"You put {current_room.item.name} into your backpack.")
            current_room.item = None
        else:
            print("There is nothing here to take.")
    
    # Backpack
    elif command == "backpack":
        if backpack == []:
            print("It's empty")
        else:
            print("You have:")
            for item in backpack:
                print(f"    {item.name.capitalize()}")
    
    # Help
    elif command == 'help':
        print("Type which direction you wish to move,")
        print("or use one of these commands:")
        print("-  Talk")
        print("-  Fight")
        print("-  Hug")
        print("-  Take")
        print("-  Backpack")
    
    # Quit
    elif command == "quit":
        running = False
    
    # Incorrect command
    else:
        print("Enter 'help' for list of commands")

    input("\nPress <Enter> to continue")

print("Thank you for playing Deepest Dungeon")

