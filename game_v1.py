import pygame
import sys

pygame.init()


size = width, height = 800, 800
pygame.display.set_mode(size, pygame.DOUBLEBUF)
black = 0, 0, 0
screen = pygame.display.set_mode(size)

class Bullet(object):
    """docstring for Bullet"""
    def __init__(self, x, y, speed):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)        
        
    def draw(self):
        screen.blit(self.image, self.rect)




class Player(pygame.sprite.Sprite):
    """docstring for Player"""
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load("pirate.png")
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect = self.rect.move(self.speed)

    def draw(self):
        screen.blit(self.image, self.rect)





class Brick(pygame.sprite.Sprite):
    """docstring for wall"""
    def __init__(self, x, y):
        super(Brick, self).__init__()
        self.image = pygame.image.load("brick.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)

class Wall():
    """docstring for Wall"""
    def __init__(self, start_x, start_y, end_x, end_y):
        self.bricks = [Brick(x, y) for x in range(start_x, end_x, 32) for y in range(start_y, end_y, 32)]
        self.group = pygame.sprite.Group()

    def draw(self):
        for brick in self.bricks:
            brick.draw()

    def collision(self, player):
        for brick in self.bricks:
            if pygame.sprite.collide_rect(player, brick):
                return True
        return False
        


player = Player(400,400)
walley = Wall(100, 100,300,300)
bulley = Bullet(10, 10, [9, 9]) 


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed[0] = -4
            if event.key == pygame.K_RIGHT:
                player.speed[0] = 4
            if event.key == pygame.K_DOWN:
                player.speed[1] = 4
            if event.key == pygame.K_UP:
                player.speed[1] = -4

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed[0] = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player.speed[1] = 0



    # move everything
    player.move()
    bulley.move()


    #line for detecting collisions? <3
    #this was brilliant thank you <3
    if walley.collision(player):
        player.speed[1] = -1*player.speed[1]
        player.speed[0] = -1*player.speed[0]
        player.move()
        player.speed = [0, 0]

    
    screen.fill(black)

    # draw stuff
    player.draw()
    walley.draw()
    bulley.draw()

    pygame.display.flip()

