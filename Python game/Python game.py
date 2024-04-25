#! python3
# global variables
import cmd
import sys
import textwrap

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
WEST = 'west'
EAST = 'east'
SCREEN_WIDTH = 80

print("--------------------------------------------------------")
print(
    "You are a degerate gambler, and times have been tough..... luckily there is a small crypt you heard about,\ntales of jewels and riches fill your senses, you must enter")
print("Welcome to the curse of the crypt \n ---------------------------------------------------------")

# todo: Player can move into directions where they shouldn't, causing error.
cryptRooms = {
    'Main Room': {
        DESC: 'This room is cold and murky, you see three doors in front of you, a Pharoh symbol is on the ground',
        NORTH: 'Puzzle Room',
        WEST: 'Doctors room',
        EAST: 'Professors Room',
        SOUTH: 'locked door.. ',
    },
    'Doctors room': {
        DESC: 'The room has sticky notes strewn along the walls, it smells of sulpher and pungent male cologne',
        EAST: 'Main Room',
        WEST: 'A wall...',
        NORTH: 'Another wall, you can hear the macherniny cranking and jolting',
        SOUTH: 'Its a wall!, you see deep scratches and impressions into the sandstone',
        'NPC': {
            'Description': 'Short and stubby man, who has the facial hair of a preteen',
            'Start phrase': 'Well who do you think you are? Interupting my work! you annoy me'

        },
        'Professors room': {
            DESC: 'The room is tidy, a nice auroma of lemons, wow even a couch is in here too!',
            NORTH: 'A wall bordering the puzzle room, you hear a small screeching, mixed with the harmony of engine noises',
            WEST: 'Main Room',
            EAST: 'A wall, you dont know what it borders but their is a picture of a small egyptian cat. Cute!',
            SOUTH: 'A wall, it borders the way out, and has a made  ',
            'NPC': {
                'name': 'Professor Dan',
                'Description': 'Tall and lanky, smells of incense and rosemary, wears his pants above his waist'
            }

        },
        'Puzzle room': {
            DESC: 'The room has tall ceilings, a machine is present in front of you with four squares _ _ _ _',
            NORTH: 'You are facing the puzzle the closest you can get',
            WEST: 'You see Egyption symbols and hieroglyphs, a large man domineering over seemingly a sea of people',
            EAST: 'Hieroglyphs cover the east side of the room, it displays a people rushing into the crypts and leaving with jeweles',
            SOUTH: 'Main Room'
        },
        'Final room': {
            # figure out how to lock this thing
        }

    }
}

location = 'Main Room'  # where the start is; I want to have a start menu
# the global data variables

inventory = ['readme note', 'map']
# show where to go
showFullExits = True
desc = 'the room is murky and hot, you see three doors. A million thoughts are going through your head what do you do?'

for line in textwrap.wrap(desc, 80):
    print(line)


def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""

    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(cryptRooms[loc][DESC], SCREEN_WIDTH)))

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST,):
        if direction in cryptRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST,):
            if direction in cryptRooms[location]:
                print('%s: %s' % (direction.title(), cryptRooms[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in cryptRooms[location]:
        print('You move to the %s.' % direction)
        location = cryptRooms[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')


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

    def help_combat(self):
        print('Combat is not implemented in this program.')

    def do_north(self, arg):
        moveDirection('north')

    def do_south(self, arg):
        moveDirection('south')

    def do_east(self, arg):
        moveDirection('east')

    def do_west(self, arg):
        moveDirection('west')
        self.dialogue_w_doc()

    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west

    def do_exits(self, arg):
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing the description of the exit')
        else:
            print('Showing a smaller description incase ur lazy')


if __name__ == '__main__':
    print('Welcome to the Pharaohs tomb')
    print('____________________________')
    print()
    print('(Type help to get a list of potential commands por favor)')
    print()
    TextAdventureCmd().cmdloop()
    displayLocation(location)
    print('Lets hope you like this project!')
