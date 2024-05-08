#! python3
import cmd
import sys
import textwrap

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
START = 'start'
LEFT = 'left'
RIGHT = 'right'
DIFF = 'diff'
location = 'The Pharaohs Tomb'
dial = ''
puz = ''
main = ''
dark = ''
locked_door = ''
word = 'berm'
string = ''
SCREEN_WIDTH = 70
current_char = 0
rep_doctor = 0
rep_professor = 0
inventory = []
left_view = ['b', 'a', 'r', 'd']
current_view = ['f', 'e', 'l', 'k']
right_view = ['w', 'o', 'c', 'm']
started = False
solved = False
locked = True
showFullExits = True
doc_visited = False
pros_visited = False

npc_Data = {
    'Doctor Peter': {
        'His Name': 'Doctor Peter',
        'His Description ': 'Short and stubby man, who has the facial hair of a preteen',
        'His Greetings ': 'Well who do you think you are? Interrupting my work! you annoy me'
    },
    'Professor Dan': {
        'His Name': 'Professor Dan',
        'His Description': 'all and lanky, smells of incense and rosemary, wears his pants above his waist',
        'His Greetings': 'Hey man.. Got any gum? I smell your breath and its minty'
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
        DESC: 'This room is cold and murky, you see three doors to the north, east, west, '
              'a stone door to the south, and a Pharaoh symbol is on the ground',
        DIFF: 'This room is cold and murky, you see three doors to the north, east, west, '
              'and a Pharaoh symbol is on the ground',
        NORTH: 'Puzzle Room',
        WEST: 'Doctors Room',
        EAST: 'Professors Room',
        SOUTH: 'Dark Room',
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
        DESC: 'The room has tall ceilings, four large stone dials are presented in front of you {_} {_} {_} {_}',
        DIFF: 'The room has tall ceilings, the dials lay in the ground unable to be used',
        SOUTH: 'Main Room',
    },
    'Dark Room': {
        DESC: 'You enter the dark room but a small glimmer of light is in front of you, hope of escape is there',
        NORTH: 'Main Room',
    },
}

items = {
    'treasure': {
        DESC: 'this is treasure.',
    },
    'tablet': {
        DESC: 'A stone tablet, similar to the design to the door in the main room.',
    },
}


def view_map():
    global puz
    global dial
    global main
    global dark
    global locked_door

    dial = "           +----------+" \
           "\n           |          |"

    puz = "           |          |" \
          "\n           |   Puz.   |" \
          "\n           |          |" \
          "\n           |          |"
    main = "+----------+----OO----+----------+" \
           "\n|          |          |          |" \
           "\n|   Doc.   |   Main   |   Prof.  |" \
           "\n|          O          O          |" \
           "\n|          |          |          |" \
           "\n|          |          |          |"
    locked_door = "+----------+----XX----+----------+"
    dark = "           |          |" \
           "\n           |          |" \
           "\n           |   Dark   |" \
           "\n           |          |" \
           "\n           |          |" \
           "\n           +----------+" \

    if location == 'Puzzle Room':
        if not solved:
            dial = "           +----------+" \
                   "\n           | ֍ ֍  ֍ ֍ |"
        puz = "           |          |" \
              "\n           |   Puz.   |" \
              "\n           |    ¶     |" \
              "\n           |          |"

    if not locked:
        locked_door = "\n+----------+----00----+----------+"

    if location == 'Main Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O    ¶     O          |" \
               "\n|          |    ╔╣    |          |" \
               "\n|          |          |          |"

    if location == 'Doctors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O          |" \
               "\n| ₭    ¶   |          |          |" \
               "\n|          |          |          |"

    if location == 'Professors Room':
        main = "+----------+----OO----+----------+" \
               "\n|          |          |          |" \
               "\n|   Doc.   |   Main   |   Prof.  |" \
               "\n|          O          O      ₭   |" \
               "\n|          |          |  ¶       |" \
               "\n|          |          |          |"
    print(dial)
    print(puz)
    print(main)
    print(locked_door)
    print(dark)
    print()
    print("\tKey "
          "\n---------------"
          "\nUnlocked Doors = 0"
          "\nLocked Doors = X"
          "\nWall = -,+,|"
          "\nPuz. = Puzzle Room"
          "\nDoc. = Doctors Room"
          "\nProf. = Professors Room"
          "\n¶. = Player (You)"
          "\n֍ = Stone Dial"
          "\n₭ = Character"
          "\n╔╣ = Pharaoh Symbol")


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""

    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    if (location == 'Puzzle Room' and solved) or (location == 'Main Room' and not locked):
        print('\n'.join(textwrap.wrap(cryptRooms[loc][DIFF], SCREEN_WIDTH)))
    else:
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


def submit_puzzle():
    global solved
    if word == string:
        print('the stone dials sink into the floor, opening the door revealing the door. the treasure is yours.')
        inventory.append('treasure')
        solved = True
    else:
        print('Pressing the button, nothing happens with the dials.')


def puzzle(rotation, selection):
    print()
    global current_view
    global left_view
    global right_view
    global current_char
    global string
    global word
    temp = [None] * 5
    current_char = selection

    temp[0] = current_view[current_char]
    if not solved:
        if rotation == RIGHT:
            current_view[current_char] = left_view[current_char]
            temp[1] = right_view[current_char]
            right_view[current_char] = temp[0]
            left_view[current_char] = temp[1]
        if rotation == LEFT:
            current_view[current_char] = right_view[current_char]
            temp[1] = left_view[current_char]
            left_view[current_char] = temp[0]
            right_view[current_char] = temp[1]
        string = '} {'.join(str(x) for x in current_view)
        print("{" + string + '}')
        string = string.replace('} {', '')
        return
    else:
        print('The dials are locked into place, unable to be used again.')


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # I added this for the npc dialogue
    def __init__(self):
        super().__init__()
        self.location = 'Main Room'
        self.inventory = []
        self.showFullExits = True

    def dialogue_w_doc(self):
        global rep_doctor
        global doc_visited
        like_counter = 0

        while True:
            # First Meeting Professor
            if rep_doctor == 0:
                print("Neutral Question")
                print("1: ")
                print("2: ")
                print("3: ")
                print("4: exit ")

                doc_visited = True
                user_input = input("> ").strip().lower()
                if user_input == '1':  # Main response 1
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    print("l Question")
                    print("1: 1")
                    print("2: 2")
                    print("3: exit")

                    user_input = input("> ").strip().lower()
                    if user_input == '1':  # Side response 1-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')
                        print("l Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 1-2
                        like_counter = like_counter - 2
                        rep_doctor = rep_doctor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '2':  # Main response 2
                    like_counter = like_counter - 2
                    rep_doctor = rep_doctor + like_counter
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    print("l Question")
                    print("1: 11")
                    print("2: 22")
                    print("3: exit")

                    user_input = input("> ").strip().lower()
                    if user_input == '1':  # Side Response 2-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print("ok Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 2-2
                        like_counter = like_counter - 2
                        rep_doctor = rep_doctor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '3':  # Main response 3
                    like_counter = like_counter + 2
                    rep_doctor = rep_doctor + like_counter
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    if user_input == '1':  # Side Response 3-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print("ok Question")
                        print("1: 111")
                        print("2: 222")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 3-2
                        like_counter = like_counter - 2
                        rep_doctor = rep_doctor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 111")
                        print("2: 222")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_doctor = rep_doctor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '4':  # Main response 4
                    break
                else:
                    print('Not a valid response\n')

            elif rep_professor <= -4:
                print("Im not talking anymore")
                break

            elif rep_professor >= 4:
                print("hey do you want a hint")
                break

    # The default() method is called when none of the other do_*() command methods match.

    def dialogue_w_prf(self):
        global rep_professor
        global pros_visited
        like_counter = 0

        while True:
            # First Meeting Professor
            if rep_professor == 0:
                print("Neutral Question")
                print("1: ")
                print("2: ")
                print("3: ")
                print("4: exit ")

                pros_visited = True
                user_input = input("> ").strip().lower()
                if user_input == '1':  # Main response 1
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    print("l Question")
                    print("1: 1")
                    print("2: 2")
                    print("3: exit")

                    user_input = input("> ").strip().lower()
                    if user_input == '1':  # Side response 1-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')
                        print("l Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 1-2
                        like_counter = like_counter - 2
                        rep_professor = rep_professor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '2':  # Main response 2
                    like_counter = like_counter - 2
                    rep_professor = rep_professor + like_counter
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    print("l Question")
                    print("1: 11")
                    print("2: 22")
                    print("3: exit")

                    user_input = input("> ").strip().lower()
                    if user_input == '1':  # Side Response 2-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print("ok Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 2-2
                        like_counter = like_counter - 2
                        rep_professor = rep_professor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 11")
                        print("2: 22")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")
                            break

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '3':  # Main response 3
                    like_counter = like_counter + 2
                    rep_professor = rep_professor + like_counter
                    print('ok response [Reputation: ' + str(like_counter) + ']')

                    if user_input == '1':  # Side Response 3-1
                        print('ok response [Reputation: ' + str(like_counter) + ']')

                        print("ok Question")
                        print("1: 111")
                        print("2: 222")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '2':  # Side Response 3-2
                        like_counter = like_counter - 2
                        rep_professor = rep_professor + like_counter
                        print('bad response [Reputation: ' + str(like_counter) + ']')

                        print("bad Question")
                        print("1: 111")
                        print("2: 222")
                        print("3: exit")

                        user_input = input("> ").strip().lower()
                        if user_input == '1':
                            print('ok response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '2':
                            like_counter = like_counter - 2
                            rep_professor = rep_professor + like_counter
                            print('bad response [Reputation: ' + str(like_counter) + ']')
                            print("end")

                        elif user_input == '3':
                            break
                        else:
                            print('Not a valid response\n')
                    elif user_input == '3':
                        break
                    else:
                        print('Not a valid response\n')
                elif user_input == '4':  # Main response 4
                    break
                else:
                    print('Not a valid response\n')

            elif rep_professor <= -4:
                print("Im not talking anymore")
                break

            elif rep_professor >= 4:
                print("hey do you want a hint")
                break


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
        if location == 'Main Room' and locked:
            print('The door wont budge')
        else:
            moveDirection('south')

    def do_east(self, arg):
        """Moves the character east if able."""
        moveDirection('east')
        if location == 'Professors Room':
            self.dialogue_w_prf()

    # dialogue being tied to direction maybe isn't a good idea lol, player can get dialogue trigger in wrong room.
    # probably aware already just thought I'd mention.
    def do_west(self, arg):
        """Moves the character west if able."""
        moveDirection('west')
        if location == 'Doctors Room':
            self.dialogue_w_doc()

    def do_start(self, arg):
        """Starts the game"""
        moveDirection('start')

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
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        else:
            while True:
                try:
                    pos = int(input('Select what character position: \n'))
                    break
                except:
                    print('Input a number!')
            pos = pos - 1
            puzzle('left', pos)
            if pos < 0 or pos > 3:
                print('Not a valid character position!')
                return

    def do_right(self, arg):
        """Brings a character in the word puzzle from left to right with position input"""
        if location != 'Puzzle Room':
            print('You are not in the puzzle Room')
            return
        else:
            while True:
                try:
                    pos = int(input('Select what character position: \n'))
                    break
                except:
                    print('Input a number!')
            pos = pos - 1
            puzzle('right', pos)
            if pos < 0 or pos > 3:
                print('Not a valid character position!')
                return

    def do_location(self, arg):
        """View Information about the current location incase it is lost"""
        displayLocation(location)

    def do_submit(self, arg):
        """Submit your guess for the puzzle"""
        if not started:
            print('Game not started')
        elif location == 'Puzzle Room':
            submit_puzzle()
        else:
            print('You are not in the Puzzle Room')

    def do_inventory(self, arg):
        """Access the players inventory"""
        if not started:
            print('Game not started')
            return

        elif len(inventory) == 0:
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

    def do_view_item(self, arg):
        """View an item in your inventory"""
        if not started:
            print('Game not started')
            return
        elif not inventory:
            print('Inventory contains no items')
            return
        else:
            item = input('What item do you want to view: \n')
            if item in inventory:
                print('\n' + item + ": " + "".join(textwrap.wrap(items[item][DESC], SCREEN_WIDTH)))
            else:
                print('You do not have this item.')

    def do_escape(self, arg):
        """Escape if you can"""
        if not started:
            print('Game not started')
            return
        elif location != 'Dark Room':
            print('You are not in the dark room.')
            return
        else:
            while True:
                confirm = input("Are you sure you want to escape (Yes or no): \n")
                confirm = confirm.lower()
                if confirm == 'yes' or 'y' or confirm == 'no' or 'n':
                    break
                else:
                    print('Please enter Yes or No')

            if confirm == 'yes' or confirm == 'y':
                if 'treasure' in inventory:
                    print('You escape with the treasure')
                    sys.exit()
                else:
                    print('You escape without the treasure.')
            else:
                return

    def do_unlock(self, arg):
        """Attempt to unlock the locked door"""
        global locked
        if not started:
            print('Game not started')
            return
        elif 'tablet' in inventory and location == 'Main Room':
            print('You insert the tablet into the door, as it disappears, the door opens in front of you')
            locked = False
            inventory.remove('tablet')
            return
        elif 'tablet' not in inventory and location == 'Main Room':
            print('You attempt to open the door, but you do not have the item to do so.')
            return
        else:
            print('There is no door to unlock here')

    def do_reputation(self, arg):
        """View reputation with a character you have visited"""
        if not started:
            print('Game not started')
        if pros_visited:
            print('[Total Professor Reputation: ' + str(rep_professor) + ']')
        if doc_visited:
            print('[Total Doctor Reputation: ' + str(rep_doctor) + ']')
        else:
            print('You have not visited anyone')
    do_inv = do_inventory
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_loc = do_location
    do_view = do_view_item
    do_rep = do_reputation


# Commented out the welcome, I moved alot of it to the "start menu",
# I didn't delete chance, so you can get a chance to look and see how it compares.
if __name__ == '__main__':
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()
    print('Thank you for playing!')
