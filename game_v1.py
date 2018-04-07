import pygame
import sys

pygame.init()


size = width, height = 512, 512
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

    def collision(self, entity):
        for brick in self.bricks:
            if pygame.sprite.collide_rect(entity, brick):
                return True
        return False
        

all_items = []

player = Player(400,400)
walley = Wall(100, 100,300,300)
bulley = Bullet(10, 10, [9, 9])

all_items += [walley]

def collision_to_point(position):
    thing = pygame.sprite.Sprite()
    thing.rect = pygame.Rect(position[0], position[1], position[0]+1, position[1]+1)
    for item in all_items:
        if item.collision(thing):
            return True
    return False


class REAPER(object):
    """docstring for REAPER"""
    def __init__(self, x, y):
        super(REAPER, self).__init__()
        self.image = pygame.image.load("REAPER.png")
        self.rect = self.image.get_rect()
        self.speed = [x, y]
        self.rect.x = x
        self.rect.y = y
        self.calculated = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, target):
        self.update_speed([target.rect[0], target.rect[1]])
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        print self.speed


    def update_speed(self, target):
        self.calculated = 10
        # OK so i guess we are doing A* here... haha thisll be fun...
        # Ok so first step i guess is to make an array thats all 0s
        a_star_grid = [[" " for i in range(width / 32)] for j in range(height / 32)]
        # Ok so we also need a list of current positions
        current = [(self.rect.x / 32, self.rect.y / 32)]
        a_star_grid[self.rect.x / 32][self.rect.y / 32] = "X"
        target_pos = (target[0] / 32, target[1] / 32)

        # Ok so now we need to iterate until we find the target
        iteration = 0
        while target_pos not in current and iteration < 100:
            iteration += 1
            new_current = []
            for cur in current:
                if cur[0] + 1 < len(a_star_grid) and a_star_grid[cur[0] + 1][cur[1] + 0] == " " and not collision_to_point((cur[0]*32, cur[1]*32)):
                    new_current += [(cur[0] + 1, cur[1] + 0)]
                    a_star_grid[cur[0] + 1][cur[1] + 0] = "U"

                if cur[0] - 1 >= 0 and a_star_grid[cur[0] - 1][cur[1] + 0] == " " and not collision_to_point((cur[0]*32, cur[1]*32)):
                    new_current += [(cur[0] - 1, cur[1] + 0)]
                    a_star_grid[cur[0] - 1][cur[1] + 0] = "D"

                if cur[1] + 1 < len(a_star_grid) and a_star_grid[cur[0] + 0][cur[1] + 1] == " " and not collision_to_point((cur[0]*32, cur[1]*32)):
                    new_current += [(cur[0] + 0, cur[1] + 1)]
                    a_star_grid[cur[0] + 0][cur[1] + 1] = "R"

                if cur[1] - 1 >= 0 and a_star_grid[cur[0] + 0][cur[1] - 1] == " " and not collision_to_point((cur[0]*32, cur[1]*32)):
                    new_current += [(cur[0] + 0, cur[1] - 1)]
                    a_star_grid[cur[0] + 0][cur[1] - 1] = "L"

                current = new_current

        current_point = [target_pos[0], target_pos[1]]
        old_point = [target_pos[0], target_pos[1]]
        iteration = 0
        while a_star_grid[current_point[0]][current_point[1]] != "X"  and iteration < 100:
            iteration += 1
            old_point = [current_point[0], current_point[1]]
            if a_star_grid[current_point[0]][current_point[1]] == "R":
                current_point[1] -= 1
            elif a_star_grid[current_point[0]][current_point[1]] == "L":
                current_point[1] += 1
            elif a_star_grid[current_point[0]][current_point[1]] == "U":
                current_point[0] -= 1
            elif a_star_grid[current_point[0]][current_point[1]] == "D":
                current_point[0] += 1
            a_star_grid[old_point[0]][old_point[1]] = "*"
        a_star_grid[old_point[0]][old_point[1]] = "0"

        print "--------------"
        for i in a_star_grid:
            for c in i:
                print c,
            print ""

        self.speed[0] = 2 if old_point[0] > self.rect.x / 32 else -2 if old_point[0] < self.rect.x / 32 else 0
        self.speed[1] = 2 if old_point[1] > self.rect.y / 32 else -2 if old_point[1] < self.rect.y / 32 else 0
        # return (old_point[0]*32, old_point[1]*32)



dave = REAPER(10, 10)
dave2 = REAPER(100, 10)
dave3 = REAPER(10, 110)
dave.update_speed((player.rect[0], player.rect[1]))

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
    dave.move(player)
    dave2.move(player)
    dave3.move(player)


    #line for detecting collisions? <3
    #this was brilliant thank you <3
    if walley.collision(player):
        player.speed[1] = -1*player.speed[1]
        player.speed[0] = -1*player.speed[0]
        player.move()
        player.speed = [0, 0]
    if walley.collision(dave):
        dave.speed[1] = -1*dave.speed[1]
        dave.speed[0] = -1*dave.speed[0]
        dave.rect.x += dave.speed[0]
        dave.rect.y += dave.speed[1]
    if walley.collision(dave2):
        dave2.speed[1] = -1*dave2.speed[1]
        dave2.speed[0] = -1*dave2.speed[0]
        dave2.rect.x += dave2.speed[0]
        dave2.rect.y += dave2.speed[1]
    if walley.collision(dave3):
        dave3.speed[1] = -1*dave3.speed[1]
        dave3.speed[0] = -1*dave3.speed[0]
        dave3.rect.x += dave3.speed[0]
        dave3.rect.y += dave3.speed[1]
    
    screen.fill(black)

    # draw stuff
    player.draw()
    walley.draw()
    bulley.draw()
    dave.draw()
    dave2.draw()
    dave3.draw()

    pygame.display.flip()

