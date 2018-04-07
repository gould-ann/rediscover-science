import pygame
import sys

pygame.init()


size = width, height = 800, 800
pygame.display.set_mode(size, pygame.DOUBLEBUF)
black = 0, 0, 0
screen = pygame.display.set_mode(size)

class Bullet(pygame.sprite.Sprite):
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

    def shoot(self, dir, location_x, location_y):
        self.rect.x = location_x
        self.rect.y = location_y
        if dir == "l":
            self.speed = [-8,0]
        if dir == "u":
            self.speed = [0,-8]
        if dir == "d":
            self.speed = [0,8]
        if dir == "r":
            self.speed = [8,0]


class Player(pygame.sprite.Sprite):
    """docstring for Player"""
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image = pygame.image.load("pirate.png")
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.rect.x = x
        self.rect.y = y
        self.dir = "r"

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

bullets = pygame.sprite.Group();
# bulley = Bullet(-10, -10, [0, 0])

while 1:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #x to shoot bullet
            if event.key == pygame.K_x:
                new_bullet = Bullet(0, 0, [0, 0])
                new_bullet.rect.x = player.rect.x
                new_bullet.rect.y = player.rect.y
                new_bullet.shoot(player.dir, player.rect.x, player.rect.y)
                bullets.add(new_bullet)
                print player.rect.x , player.rect.y
            if event.key == pygame.K_LEFT:
                player.speed[0] = -4
                player.dir = "l"
            if event.key == pygame.K_RIGHT:
                player.dir = "r"
                player.speed[0] = 4
            if event.key == pygame.K_DOWN:
                player.speed[1] = 4
                player.dir = "d"
            if event.key == pygame.K_UP:
                player.speed[1] = -4
                player.dir = "u"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed[0] = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player.speed[1] = 0



    # move everything
    player.move()

    #loops to draw bullets shot (from group) 
    for individual in bullets:
        individual.move()

    if walley.collision(player):
        player.speed[1] = -1*player.speed[1]
        player.speed[0] = -1*player.speed[0]
        player.move()
        player.speed = [0, 0]

    
    screen.fill(black)

    # draw stuff
    player.draw()
    walley.draw()
    for individual in bullets:
        individual.draw()

    pygame.display.flip()

