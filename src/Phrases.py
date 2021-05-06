import pygame
import time

class TimedDrawing(object):
    pass

class Phrase(TimedDrawing):

    UPDATE_TEXT_EVENT = pygame.USEREVENT + 5

    def __init__(self, text, on, x, y, colour, size):
        self.text = text
        self.on = on
        self.X = x
        self.Y = y
        self.colour = colour
        self.size = size
        self.current_state = 0
        self.currently_displaying = []
        self.my_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", self.size)

    def write_simple(self, screen, x, y):
        my_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 10)
        item = my_font.render(self.text, 1, (0, 0, 0))
        screen.blit(item, (x + 200, y + 200))

    def write(self, screen):

        my_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", self.size)

        for index, letter in enumerate(self.text):
            label = my_font.render(letter, 1, self.colour)
            screen.blit(label, (self.X + (index*20), self.Y))
            time.sleep(.5)
            pygame.display.update()

    def write_phrase_slowly(self, delay_ms=100):
        self.currently_displaying.clear()
        pygame.time.set_timer(self.UPDATE_TEXT_EVENT, delay_ms)

    def stop_writing(self):
        pygame.time.set_timer(self.UPDATE_TEXT_EVENT, 0)


    def draw_frame(self, screen):
        for index, letter in enumerate(self.text):
            if index == self.current_state:
                self.currently_displaying.append(letter)


        if self.current_state != len(self.text) - 1:
            self.current_state += 1
            return True
        else:
            self.current_state = 0
            return False

    def write_current_phrase(self, screen):
        for letter in range(len(self.currently_displaying)):
            label = self.my_font.render(self.currently_displaying[letter], True, self.colour)
            screen.blit(label, (self.X + (letter * 20), self.Y))
