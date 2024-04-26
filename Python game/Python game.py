#! python3
# global variables
import cmd
# import sys
import textwrap

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
START = 'start'
SCREEN_WIDTH = 70
inventory = ['readme note', 'map']
showFullExits = True
location = 'The Pharaohs Tomb'  # where the start is; I want to have a start menu

# todo: commented out rooms that have dead ends that currently break when player goes in that direction.
cryptRooms = {
    'The Pharaohs Tomb': {
        DESC: "---------------------------------------------------------------------- "
              'You are a degenerate gambler, and times have been tough..... '
              'luckily there is a small crypt you heard about, '
              'tales of jewels and riches fill your senses, you must enter. '
              'Welcome to The Pharaohs Tomb.                                       '
              "---------------------------------------------------------------------- "
              'Type "help" to view available commands, or type "start" to begin!. ',
        START: 'Main Room'
    },
    'Main Room': {
        DESC: 'This room is cold and murky, you see three doors in front of you, a Pharaoh symbol is on the ground',
        NORTH: 'Puzzle Room',
        WEST: 'Doctors Room',
        EAST: 'Professors Room',
        SOUTH: 'locked door.. ',
    },
    'Doctors Room': {
        DESC: 'The room has sticky notes strewn along the walls, it smells of sulphur and pungent male cologne',
        EAST: 'Main Room',
        # WEST: 'A wall...',
        # NORTH: 'Another wall, you can hear the machinery cranking and jolting',
        # SOUTH: 'Its a wall!, you see deep scratches and impressions into the sandstone',
        'NPC': {
            'Description': 'Short and stubby man, who has the facial hair of a preteen',
            'Start phrase': 'Well who do you think you are? Interrupting my work! you annoy me'
        }

    },
    'Professors Room': {
        DESC: 'The room is tidy, a nice aroma of lemons, wow even a couch is in here too!',
        # NORTH: 'A wall bordering the puzzle room, you hear a small screeching, mixed with the harmony of engine noises',
        WEST: 'Main Room',
        # EAST: 'A wall, you don't know what it borders but there is a picture of a small egyptian cat. Cute!',
        # SOUTH: 'A wall, it borders the way out, and has a made  ',
        'NPC': {
            'name': 'Professor Dan',
            'Description': 'Tall and lanky, smells of incense and rosemary, wears his pants above his waist'
        }

    },
    'Puzzle Room': {
        DESC: 'The room has tall ceilings, a machine is present in front of you with four squares _ _ _ _',
        # NORTH: 'You are facing the puzzle the closest you can get',
        # WEST: 'You see Egyptian symbols and hieroglyphs, a large man domineering over seemingly a sea of people',
        # EAST: 'Hieroglyphs cover the east side of the room, it displays a people rushing into the crypts and leaving with jewels',
        SOUTH: 'Main Room'
    },
    'Final Room': {
        # figure out how to lock this thing
    }

}


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""

    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(cryptRooms[loc][DESC], SCREEN_WIDTH)))

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in cryptRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in cryptRooms[location]:
                print('%s: %s' % (direction.title(), cryptRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location
    started = False

    if direction in cryptRooms[location]:
        if direction == START:
            print('Starting Game...')
        else:
            print('You move to the %s.' % direction)
        location = cryptRooms[location][direction]
        displayLocation(location)
    else:
        if direction == START:
            print('Game already started..')

        else:
            if not started:
                print('Game not started')
            else:
                print('You cannot move in that direction')


def view_map():
    # todo: maybe tie this map with the map item?
    print("           +----------+")
    print("           |          |")
    print("           |          |")
    print("           |   Puz.   |")
    print("           |          |")
    print("           |          |")
    print("+----------+----OO----+----------+")
    print("|          |          |          |")
    print("|   Doc.   |   Main   |   Prof.  |")
    print("|          O          O          |")
    print("|          |          |          |")
    print("|          |          |          |")
    print("+----------+----------+----------+")
    print()
    print("\tKey "
          "\n---------------"
          "\nDoor = 0"
          "\nWall = -,+,|"
          "\nPuz. = Puzzle Room"
          "\nDoc. = Doctors Room"
          "\nProf. = Professors Room")


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # I added this for the npc dialogue
    def __init__(self):
        super().__init__()
        self.location = 'Main Room'
        self.inventory = ['readme note', 'map']
        self.showFullExits = True

    def do_dialogue(self):
        if self.location == 'Doctors room':
            self.dialogue_w_doc()
        else:
            print('there is no one here, sad and depressing')

    def dialogue_w_doc(self):
        if self.location in cryptRooms and 'NPC' in cryptRooms[self.location]:
            npc_data = cryptRooms[self.location]['NPC']
            npc_name = 'NPC'
            print(npc_data['Description'])
            print(npc_data['Greetings'])
        else:
            print("No one is here lol")

        like_counter = 0

        while True:
            print("What do you want to say in response?")
            print("1: Who are you to talk to me like that? Where even is your PHD?")
            print("2: Listen, we are stuck here together. Help me help us escape")
            print("3: Well you annoy me too but am I crying about it? Lets work together")
            print("4: you exit the conversation")

            user_input = input("> ").strip().lower()

            if user_input == '1' or user_input.startswith('What'):
                print("You question his legitimacy")
                print("Doc Peter: WHERE IS YOUR DAMN DEGREE?? I WORKED FOR 8 YEARS..(he rambles for 2 minutes)")
                attitude = like_counter - 1
                print(" Bad first impression", attitude)
                break
            elif user_input == '2' or user_input.startswith('Who'):
                print("You reason with him")
                print("Yeah dont you think I know that?, but yeah I guess I will help I have outdated textbooks here")
                break
            elif user_input == '3' or user_input.startswith('Well'):
                print("You challenged his aggression")
                print("I see you take no shit, but do you even know why I am upset? that idiot professor")
                break
            elif user_input == '4' or user_input.startswith("exit"):
                break
            else:
                print("Doctor Peter: Yeah I have no idea what you just said")

    # The default() method is called when none of the other do_*() command methods match.

    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True  # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    def do_north(self, arg):
        """Moves the character north if able."""
        moveDirection('north')

    def do_south(self, arg):
        """Moves the character south if able."""
        moveDirection('south')

    def do_east(self, arg):
        """Moves the character east if able."""
        moveDirection('east')

    # dialogue being tied to direction maybe isn't a good idea lol, player can get dialogue trigger in wrong room.
    # probably aware already just thought I'd mention.
    def do_west(self, arg):
        """Moves the character west if able."""
        moveDirection('west')
        self.dialogue_w_doc()

    def do_start(self, arg):
        """Starts the game"""
        moveDirection('start')

    def do_inventory(self, arg):
        """Access the players inventory"""
        if len(inventory) == 0:
            print('Inventory:\n (Contains no Items)')
            return
        item_count = {}
        # If there is an item in inventory, add to item count, otherwise set item count to one.
        for item in inventory:
            if item in inventory:
                if item in item_count.keys():
                    item_count[item] += 1
                else:
                    item_count[item] = 1
        print('Inventory:')
        for item in set(inventory):
            if item_count[item] > 1:
                print(' %s %s' % (item, item_count[item]))
            else:
                print('  ' + item)

    def do_exits(self, arg):
        """Shows full descriptions of where exits lead too vs all available exits."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing the description of the exit')
        else:
            print('Showing a smaller description incase ur lazy')

    def do_map(self, arg):
        """View the in-game map (shows all the room connections)"""
        view_map()

    def do_location(self, arg):
        """View Information about the current location (incase it is lost)"""
        displayLocation(location)

    do_inv = do_inventory
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_loc = do_location


# Commented out the welcome, I moved alot of it to the "start menu",
# I didn't delete chance, so you can get a chance to look and see how it compares.
if __name__ == '__main__':
    # print('Welcome to the Pharaohs tomb')
    # print('____________________________')
    # print()
    # print('(Type help to get a list of potential commands por favor)')
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()
    print('Lets hope you like this project!')
