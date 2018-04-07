import pygame

class Selections:

    hovered = False
    def __init__(self, text,location):
        self.text = text
        self.location = location
        self.set_rect()
        self.draw()

    def draw_box(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.location

    def get_color(self):
        return (255, 255, 255) if self.hovered else (100, 100, 100)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.location

pygame.init()
screen = pygame.display.set_mode((480, 320))
menu_font = pygame.font.Font(None, 40)
options = [Selections("NEW GAME", (140, 105)), Selections("LOAD GAME", (135, 155)),
           Selections("OPTIONS", (145, 205))]
while True:
    pygame.event.pump()
    event = pygame.event.get()
    screen.fill((57, 82, 54)) #colored background
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            for events in event:
                if events.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print pos
        option.draw()
    pygame.display.update()


