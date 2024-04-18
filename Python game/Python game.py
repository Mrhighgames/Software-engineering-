import pygame
import button

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'
DESC = 'DESC'
font = pygame.font.Font('vcr_osd_mono_pixel.ttf', 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')
desc = ("You are a degerate gambler, and times have been tough..... luckily there is a small crypt you heard about,"
        "tales of jewels and riches fill your senses, you must enter. "
        "Welcome to the curse of the crypt")

north = button.Button(150, 400, 'Go North')
south = button.Button(450, 400, 'Go South')
east = button.Button(150, 550, 'Go East')
west = button.Button(450, 550, 'Go West')
leave = button.Button(300, 700, 'Quit')
counter = 0


def draw_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines(' ')]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
            for word in lines:
                word_surface = font.render(word, True, color)
                word_width , word_height = word_surface.get_size()
                if x + word_width >= SCREEN_WIDTH:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height


run = True
while run:
    screen.fill(button.bg)
    draw_text(screen, desc, (20,50), font, (255, 255, 255))

    if north.draw_button(screen, font):
        print('north')
    if south.draw_button(screen, font):
        print('south')
    if east.draw_button(screen, font):
        print('east')
    if west.draw_button(screen, font):
        print('west')
    if leave.draw_button(screen, font):
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

worldRooms = {
    'test': {
        NORTH: '',
        SOUTH: '',
        EAST: '',
        WEST: '',

    }
}
