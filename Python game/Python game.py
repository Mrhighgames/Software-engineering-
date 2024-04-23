import textwrap
import Rooms
import Player
import Commands
import cmd
import Rooms
showFullExits = True
import textwrap
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'
DESC = 'DESC'
currentRoom = 'Main Room'
SCREEN_WIDTH = 80


worldRooms = {
    'Main Room': {
        DESC: 'test',
        NORTH: 'Puzzle Room',
        SOUTH: 'Exit Room',
        EAST: 'Side Room 1',
        WEST: 'Side Room 2',

    },
    'Side Room 1': {
        DESC: 'test',
        WEST: 'Main Room',

    },
    'Side Room 2': {
        DESC: 'test',
        EAST: 'Main Room',

    },
    'Puzzle Room': {
        DESC: 'test',
        SOUTH: 'Main Room',

    },
    'Exit Room': {
        DESC: 'test',
        NORTH: 'Main Room',

    },
}


def displayRooms(room):
    print(room)
    print('=' * len(room))

    print('\n'.join(textwrap.wrap(worldRooms[room][DESC], SCREEN_WIDTH)))

    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST):
        if direction in worldRooms[room].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST):
            if direction in worldRooms[room]:
                print('%s: %s' % (direction.title(), worldRooms[currentRoom][direction]))
            else:
                print('Exits: %s' % ' '.join(exits))


class TextPuzzleCmd(cmd.Cmd):
    prompt = '\n> '

    def __init__(self):
        super().__init__()
        self.start_enabled = False

    def default(self, arg):
        print('Command not found, Type "help" for the list of commands')

    def do_quit(self, arg):
        """Quit the game"""
        return True

    def do_north(self, arg):
        """Change to the room that is north if possible."""
        if self.start_enabled:
            movePlayer('north')
        else:
            print('Game off')

    def do_south(self, arg):
        """Change to the room that is south if possible."""
        if self.start_enabled:
            movePlayer('south')
        else:
            print('Game off')

    def do_east(self, arg):
        """Change to the room that is east if possible."""
        if self.start_enabled:
            movePlayer('east')
        else:
            print('Game off')

    def do_west(self, arg):
        """Change to the room that is west if possible."""
        if self.start_enabled:
            movePlayer('west')
        else:
            print('Game off')

    def do_start(self, arg):
        """Start the game"""
        self.start_enabled = True
        print('Starting game...')


def movePlayer(direction):
    global currentRoom

    if direction in worldRooms[currentRoom]:
        print('Moving to the %s' % direction)
        currentRoom = worldRooms[currentRoom][direction]
        displayRooms(currentRoom)
    else:
        print('Cannot move in this direction')


if __name__ == '__main__':
    print(textwrap.fill('You are a degerate gambler, and times have been tough..... '
                        'luckily there is a small crypt you heard about, '
                        'tales of jewels and riches fill your senses, you must enter. '
                        'Welcome to the curse of the crypt', SCREEN_WIDTH))
    print(textwrap.fill('----------------------------------------'
                        '----------------------------------------', SCREEN_WIDTH))
    print()
    print('Type "start" to begin the game')
    displayRooms(currentRoom)
    TextPuzzleCmd().cmdloop()
    print('Thank you for playing the game.')
