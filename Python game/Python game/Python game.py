#! python3
import cmd
import textwrap

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
START = 'start'
LEFT = 'left'
RIGHT = 'right'
started = False
SCREEN_WIDTH = 70
inventory = ['readme note']
showFullExits = True
location = 'The Pharaohs Tomb'
puz = ''
main = ''
current_char = 0
left_view = ['v', 'b', 'k', 'd']
current_view = ['a', 'z', 'r', 'y']
right_view = ['w', 'o', 'c', 'm']

npc_Data = {
    'Doctor Peter': {
        'His Name':'Doctor Peter',
        'His Description ':'Short and stubby man, who has the facial hair of a preteen',
        'His Greetings ':'Well who do you think you are? Interupting my work! you annoy me'
    },
    'Professor Dan': {
        'His Name':'Professor Dan',
        'His Description':'all and lanky, smells of incense and rosemary, wears his pants above his waist',
        'His Greetings':'Hey man.. Got any gum? I smell your breath and its minty'
    }
}


cryptRooms = {
    'The Pharaohs Tomb': {
        DESC: "---------------------------------------------------------------------- "
              'You are a degenerate gambler, and times have been tough..... '
              'luckily there is a small crypt you heard about, '
              'tales of jewels and riches fill your senses, you must enter. '
              'Welcome to The Pharaohs Tomb.                                       '
              "---------------------------------------------------------------------- "
              'Type "help" to view available commands, or type "start" to begin!. ',
        START: 'Main Room',
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
        'NPC': {
            'Description': 'Short and stubby man, who has the facial hair of a preteen',
            'Start phrase': 'Well who do you think you are? Interrupting my work! you annoy me'
        }

    },
    'Professors Room': {
        DESC: 'The room is tidy, a nice aroma of lemons, wow even a couch is in here too!',
        WEST: 'Main Room',
        'NPC': {
            'name': 'Professor Dan',
            'Description': 'Tall and lanky, smells of incense and rosemary, wears his pants above his waist'
        }

    },
    'Puzzle Room': {
        DESC: 'The room has tall ceilings, a machine is present in front of you with four squares _ _ _ _',
        SOUTH: 'Main Room',
    },
}


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""

    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(cryptRooms[loc][DESC], SCREEN_WIDTH)))

    if loc == 'Puzzle Room':
        puzzle('center', 0)

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in cryptRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        # Prints a full descriptions of the exits with direction and location
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in cryptRooms[location]:
                print('%s: %s' % (direction.title(), cryptRooms[location][direction]))
    else:
        # Shows the brief direction of the exits without showing the connected rooms.
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location
    global started

    if direction in cryptRooms[location]:
        if direction == START:
            print('Starting Game...')
            started = True
        else:
            print('You move to the %s.' % direction)
        location = cryptRooms[location][direction]
        displayLocation(location)
    else:
        if direction == START:
            print('Game already started..')

        else:
            if location == 'The Pharaohs Tomb':
                print('Game not started')
                return
            else:
                print('You cannot move in that direction')


def puzzle(rotation, selection):
    print()
    global current_view
    global left_view
    global right_view
    global current_char
    word = 'word'
    temp = [None] * 5
    current_char = selection

    temp[0] = current_view[current_char]
    if rotation == RIGHT:
        current_view[current_char] = left_view[current_char]  # replaces current_view with left_view (replace k with y)
        temp[1] = right_view[current_char]  # stores right_view (storing c)
        right_view[current_char] = temp[0]  # replaces right view with old current_view (replace c with k)
        left_view[current_char] = temp[1]  # replace left_view with temp two (replace blank with c)
    if rotation == LEFT:
        current_view[current_char] = right_view[current_char]
        temp[1] = left_view[current_char]
        left_view[current_char] = temp[0]
        right_view[current_char] = temp[1]
    string = ''.join(str(x) for x in current_view)
    if word == string:
        print('WIN')
    print(string)
    return


def view_map():
    global puz
    global main

    puz = "           +----------+" \
          "\n           |          |" \
          "\n           |          |" \
          "\n           |   Puz.   |" \
          "\n           |          |" \
          "\n           |          |"
    main = "+----------+----OO----+----------+" \
           "\n|          |          |          |" \
           "\n|   Doc.   |   Main   |   Prof.  |" \
           "\n|          O          O          |" \
           "\n|          |          |          |" \
           "\n|          |          |          |" \
           "\n+----------+----------+----------+"

    if location == 'Puzzle Room':
        puz = "           +----------+" \
              "\n           |          |" \
              "\n           |          |" \
              "\n           |   Puz.   |" \
              "\n           |    ¶     |" \
              "\n           |          |"

    if location == 'Main Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O          |" \
               "\n|          |    ¶     |          |" \
               "\n|          |          |          |" \
               "\n+----------+----------+----------+"

    if location == 'Doctors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O          |" \
               "\n|      ¶   |          |          |" \
               "\n|          |          |          |" \
               "\n+----------+----------+----------+"

    if location == 'Professors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O          |" \
               "\n|          |          |  ¶       |" \
               "\n|          |          |          |" \
               "\n+----------+----------+----------+"
    print(puz)
    print(main)
    print()
    print("\tKey "
          "\n---------------"
          "\nDoor = 0"
          "\nWall = -,+,|"
          "\nPuz. = Puzzle Room"
          "\nDoc. = Doctors Room"
          "\nProf. = Professors Room"
          "\n¶. = Player (You)")


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # I added this for the npc dialogue
    def __init__(self):
        super().__init__()
        self.location = 'Main Room'
        self.inventory = ['readme note', 'map']
        self.showFullExits = True

    def do_dialogue(self):
        if self.location in cryptRooms['Doctors Room']:
            self.dialogue_w_doc()
        elif self.location in cryptRooms['Professors Room']:
            self.dialogue_w_prf()
        else:
            print("Didnt work")

    def dialogue_w_doc(self):
        room_info = cryptRooms.get(self.location)
        if room_info:
            print("NPC info")
            print(npc_Data['Doctor Peter'])

        else:
            print("room info not found")
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
                print(" Bad first impression", attitude, "The Doc disliked that")
                break
            elif user_input == '2' or user_input.startswith('Who'):
                attitude = like_counter + 1

                print("You reason with him", attitude, "The Doc accepts that")
                print(
                    "Yeah dont you think I know that?, but yeah.. I guess I will help, I have some outdated textbooks here")
                break
            elif user_input == '3' or user_input.startswith('Well'):
                attitude = like_counter + 2

                print("You challenged his agression", attitude, "+ reputation with Doc")
                print("I see you take no shit, but do you even know why I am upset? that idiot professor")
                break
            elif user_input == '4' or user_input.startswith("exit"):
                TextAdventureCmd().cmdloop
                break
            else:
                print("Doctor Peter: Yeah I have no idea what you just said")
    # The default() method is called when none of the other do_*() command methods match.

    def dialogue_w_prf(self):
        room_info = cryptRooms.get(self.location)

        if room_info:

            print("NPC info")
            print(npc_Data['Professor Dan'])

        else:
            print("Ur gay")
        like_counter = 0
        while True:
            print("What would you like to respond with?")
            print("1: Uhhh no gum.. do you know how to get out of here?")
            print("2: Hey, how did you get locked in here??")
            print("3: Listen, not sure if you are sane or not, are you going to help or what?")
            print("4:Exit conversation")

            user_input = input("> ").strip().lower()

            if user_input == '1' or user_input.startswith('uhh'):
                attitude = like_counter + 1
                print("Prof Dan:No gum?... lame...")
                print("Prof Dan: well from what I've deduced.. we are trapped", "+", attitude)

                break
            elif user_input == '2' or user_input.startswith("Hey"):
                attitude = like_counter + 1

                print(
                    "Prof Dan: Well yes, I wanted to expand my professional career and uh the other guy? he wants money",
                    "+", attitude)
                print("Prof Dan: Anyway, we will be trapped in here forever if we dont work together")

                break

            elif user_input == '3' or user_input.startswith("Listen"):
                attitude = like_counter - 1

                print(
                    "Prof Dan: Not sure if I am sane? well what about you?? Youre the idiot who got stuck in here recently ",
                    "-", attitude)
                print("Prof Dan: Even so, I need your help just like you need mine. Better not betray me")

                break

            elif user_input == '4' or user_input.startswith("exit"):
                TextAdventureCmd.cmdloop()
                break
            else:
                print("lol didnt work")

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
        self.dialogue_w_prf()

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
        if not started:
            print('Game not started')
            return

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

        if not started:
            print('Game not started')
            return
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing the description of the exit')
        else:
            print('Showing a brief description of the exits')

    def do_map(self, arg):
        """View the in-game map (shows all the room connections)"""
        if not started:
            print('Game not started')
        else:
            view_map()

    def do_left(self, arg):
        """Brings a character in the word puzzle from right to left with position input"""
        str_pos = input('Select what character position: \n')
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        if current_char < 0 or current_char > 3:
            print('Cannot go any further left')
            return
        pos = int(str_pos)
        puzzle('left', pos)

    def do_right(self, arg):
        """Brings a character in the word puzzle from left to right with position input"""
        str_pos = input('Select what character position: \n')
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        if current_char < 0 or current_char > 3:
            print('Cannot go any further right')
            return
        pos = int(str_pos)
        puzzle('right', pos)

    def do_location(self, arg):
        """View Information about the current location incase it is lost"""
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
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()
    print('Thank you for playing!')
