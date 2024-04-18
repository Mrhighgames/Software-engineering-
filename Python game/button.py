import pygame
from pygame.locals import *

pygame.init()

# define colours

# define global variable
clicked = False

bg = (0, 133, 177)
black = (0, 0, 0)
white = (255, 255, 255)

class Button:
    # colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 180
    height = 70

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text


    def draw_button(self, surface, font):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(surface, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(surface, self.hover_col, button_rect)
        else:
            pygame.draw.rect(surface, self.button_col, button_rect)

        # add shading to button
        # pygame.draw.line(surface, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        # pygame.draw.line(surface, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        # pygame.draw.line(surface, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        # pygame.draw.line(surface, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        surface.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action



