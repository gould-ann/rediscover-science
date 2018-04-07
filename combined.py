import pygame
import sys
import time
import pygame.freetype


class Option:
    hovered = False
    #creates initial box
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
    
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (77, 77, 77)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

pygame.init()
size = width, height = 512, 512
screen = pygame.display.set_mode(size)
count = 1
menu_font = pygame.font.Font(None, 40)
title = [Option("Rediscover Science", (width/20, height/15))]
options = [Option("Play game!", (width/20, height/4)),
           Option("Save another person", (width/20, height/4+50)),
           Option("Save Devin Uner", (width/20, height/4+100))]

myfont = pygame.font.SysFont("monospace", 15)

pygame.display.set_mode(size, pygame.DOUBLEBUF)
black = 50, 50, 50





# draws the game grid
grid = None
def draw_grid():
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "s":
                image = pygame.image.load("brick.png")
                rect = image.get_rect()
                rect.x = r*32
                rect.y = c*32
                screen.blit(image, rect)
            if grid[r][c] == "p":
                image = pygame.image.load("player.png")
                rect = image.get_rect()
                rect.x = r*32
                rect.y = c*32
                screen.blit(image, rect)
            if grid[r][c] == "r":
                image = pygame.image.load("REAPER.png")
                rect = image.get_rect()
                rect.x = r*32
                rect.y = c*32
                screen.blit(image, rect)
            if grid[r][c] == "g":
                if level == 1:
                    image = pygame.image.load("lovelace.png")
                if level == 2:
                    image = pygame.image.load("atanasoff.png")
                if level == 3:
                    image = pygame.image.load("turing.png")
                if level == 4:
                    image = pygame.image.load("johnson.png")
                if level == 5:
                    image = pygame.image.load("hopper.png")
                rect = image.get_rect()
                rect.x = r*32
                rect.y = c*32
                screen.blit(image, rect)


# stuff for player movement
last_moved = 0
currently_moving = False
player_direction = "r"
player_location = [0, 0]


player_health = 10
winning_text = ""

level = 1

# stuff for REAPERS
last_enemy_move = 0
def get_next_reaper_position(current_reaper_pos):
    # make a list of the current spreading spots
    a_star_grid = [[" " for i in range(width / 32)] for j in range(height / 32)]
    spreading_spots = [current_reaper_pos]
    a_star_grid[current_reaper_pos[0]][current_reaper_pos[1]] = "X"
    while (player_location[0], player_location[1]) not in spreading_spots:
        # print spreading_spots
        # print player_location
        new_spreading_spots = []
        for spot in spreading_spots:

            if spot[0] + 1 < len(a_star_grid) and a_star_grid[spot[0] + 1][spot[1] + 0] == " " and grid[spot[0] + 1][spot[1]] != "s" and grid[spot[0] + 1][spot[1]] != "g":
                new_spreading_spots += [(spot[0] + 1, spot[1] + 0)]
                a_star_grid[spot[0] + 1][spot[1] + 0] = "u"

            if spot[0] - 1 >= 0 and a_star_grid[spot[0] - 1][spot[1] + 0] == " " and grid[spot[0] - 1][spot[1]] != "s" and grid[spot[0] - 1][spot[1]] != "g":
                new_spreading_spots += [(spot[0] - 1, spot[1] + 0)]
                a_star_grid[spot[0] - 1][spot[1] + 0] = "d"

            if spot[1] + 1 < len(a_star_grid) and a_star_grid[spot[0] + 0][spot[1] + 1] == " " and grid[spot[0]][spot[1] + 1] != "s" and grid[spot[0]][spot[1] + 1] != "g":
                new_spreading_spots += [(spot[0] + 0, spot[1] + 1)]
                a_star_grid[spot[0] + 0][spot[1] + 1] = "r"

            if spot[1] - 1 >= 0 and a_star_grid[spot[0] + 0][spot[1] - 1] == " " and grid[spot[0]][spot[1] - 1] != "s" and grid[spot[0]][spot[1] - 1] != "g":
                new_spreading_spots += [(spot[0] + 0, spot[1] - 1)]
                a_star_grid[spot[0] + 0][spot[1] - 1] = "l"
        spreading_spots = new_spreading_spots

    current_point = [player_location[0], player_location[1]]
    old_point = [player_location[0], player_location[1]]
    while a_star_grid[current_point[0]][current_point[1]] != "X":
        old_point = [current_point[0], current_point[1]]
        if a_star_grid[current_point[0]][current_point[1]] == "r":
            current_point[1] -= 1
        elif a_star_grid[current_point[0]][current_point[1]] == "l":
            current_point[1] += 1
        elif a_star_grid[current_point[0]][current_point[1]] == "u":
            current_point[0] -= 1
        elif a_star_grid[current_point[0]][current_point[1]] == "d":
            current_point[0] += 1
        a_star_grid[old_point[0]][old_point[1]] = "*"
    a_star_grid[old_point[0]][old_point[1]] = "0"
    # print "--------------"
    # for i in a_star_grid:
    #     for c in i:
    #         print c,
    #     print ""
    return old_point

def display_health():
    label = myfont.render(str(player_health), 1, (0,255,255))
    screen.blit(label, (15, 480))

mobs = []
def read_level(file_name):
    global mobs
    global player_location
    global grid
    global winning_text
    mobs = []
    f = open(file_name, "r")
    grid = []
    for line in f:
        if "TEXT: " in line:
            winning_text = line.replace("TEXT: ", "")
        else:
            grid += [line.split(",")]
    print len(grid), len(grid[0])
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == "r":
                mobs += [{"type": "REAPER", "position": [r, c], "health": 3}]
            if grid[r][c] == "p":
                player_location = [r, c]

read_level("level_1.txt")
projectiles = []

def display_text(text):
    screen.fill(black)
    count = 1
    for l in text.split("\\n"):
        label = myfont.render(l, 1, (0,255,255))
        screen.blit(label, (20, count*20 + 20))
        count += 1
    if "Lovelace" in text:
        print "adding a pic of lovelace"
        image = pygame.image.load("big_lovelace.png")
        rect = image.get_rect()
        rect.x = 200
        rect.y = 350
        screen.blit(image, rect)
    if "Atanasoff" in text:
        print "adding a pic of atanasoff"
        image = pygame.image.load("big_atanasoff.png")
        rect = image.get_rect()
        rect.x = 200
        rect.y = 350
        screen.blit(image, rect)
    if "turing" in text:
        print "adding a pic of turing"
        image = pygame.image.load("big_turing.png")
        rect = image.get_rect()
        rect.x = 200
        rect.y = 350
        screen.blit(image, rect)
    if "johnson" in text:
        print "adding a pic of johnson"
        image = pygame.image.load("big_johnson.png")
        rect = image.get_rect()
        rect.x = 200
        rect.y = 350
        screen.blit(image, rect)
    pygame.display.update()
    time.sleep(10)

playing_game = False

while 1:
    if playing_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    projectiles += [{"name": "bullet", "position": [player_location[0]*32 + 16, player_location[1]*32 + 16], "speed": [0, 8] if player_direction == "d" else [0, -8] if player_direction == "u" else [8, 0] if player_direction == "r" else [-8, 0]}]
                if event.key == pygame.K_LEFT :
                    player_direction = "l"
                    currently_moving = True
                if event.key == pygame.K_RIGHT :
                    player_direction = "r"
                    currently_moving = True
                if event.key == pygame.K_DOWN :
                    player_direction = "d"
                    currently_moving = True
                if event.key == pygame.K_UP :
                    player_direction = "u"
                    currently_moving = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    currently_moving = False

        # print currently_moving
        if currently_moving and time.time() - last_moved > 0.1:
            last_moved = time.time()
            grid[player_location[0]][player_location[1]] = " "
            if player_direction == "d" and player_location[1] + 1 < len(grid) and (grid[player_location[0]][player_location[1] + 1] == " "  or grid[player_location[0]][player_location[1] + 1] == "g"):
                player_location[1] += 1
            if player_direction == "u" and player_location[1] - 1 >= 0 and grid[player_location[0]][player_location[1] - 1] == " " or grid[player_location[0]][player_location[1] - 1] == "g":
                player_location[1] -= 1
            if player_direction == "r" and (player_location[0] + 1 < len(grid)) and (grid[player_location[0] + 1][player_location[1]] == " " or grid[player_location[0] + 1][player_location[1]] == "g"):
                player_location[0] += 1
            if player_direction == "l"  and player_location[0] - 1 >= 0 and grid[player_location[0] - 1][player_location[1]] == " " or grid[player_location[0] - 1][player_location[1]] == "g":
                player_location[0] -= 1
            if grid[player_location[0]][player_location[1]] == "g":
                level += 1
                display_text(winning_text)
                read_level("level_" + str(level) + ".txt")
            grid[player_location[0]][player_location[1]] = "p"

        if time.time() - last_enemy_move > 0.4:
            last_enemy_move = time.time()
            for mob in mobs:
                grid[mob["position"][0]][mob["position"][1]] = " "
                if mob["type"] == "REAPER":
                    next_position = get_next_reaper_position(mob["position"])
                    if next_position[0] == player_location[0] and next_position[1] == player_location[1]:
                        player_health -= 1
                        if player_health == 0:
                            display_text("GAME OVER!!!")
                            read_level("level_" + str(level) + ".txt")
                    else:
                        mob["position"] = next_position
                    grid[mob["position"][0]][mob["position"][1]] = "r" 
        screen.fill(black)
        for i in range(len(projectiles)):
            if projectiles[i] != None and projectiles[i]["name"] == "bullet":
                    image = pygame.image.load("bullet.png")
                    rect = image.get_rect()
                    rect.x = projectiles[i]["position"][0]
                    rect.y = projectiles[i]["position"][1]
                    screen.blit(image, rect)
                    projectiles[i]["position"][0] += projectiles[i]["speed"][0]
                    projectiles[i]["position"][1] += projectiles[i]["speed"][1]

                    # ok so now we need a switch for the different things that could be at the bullets location
                    # if (projectiles[i]["position"][0] / 32) < 16 and (projectiles[i]["position"][0]/32) <16 and (projectiles[i]["position"][0]/32) > 0 and (projectiles[i]["position"][0]/32) > 0:
                    bullet_grid_location = [int(projectiles[i]["position"][0] / 32), int(projectiles[i]["position"][1]/32)]
                
                    print bullet_grid_location, projectiles[i]["position"], int(projectiles[i]["position"][1] / 32)

                    if not (bullet_grid_location[0] < 16 and bullet_grid_location[0] >= 0 and bullet_grid_location[1] >= 0 and bullet_grid_location[1] < 16):
                        projectiles[i] = None
                    elif grid[bullet_grid_location[0]][bullet_grid_location[1]] == "r":
                        # it hit a reaper
                        print "hit a reaper"
                        print mobs
                        projectiles[i] = None
                        for i in range(len(mobs)):
                            if mobs[i]["position"][0] == bullet_grid_location[0] and mobs[i]["position"][1] == bullet_grid_location[1]:
                                print "hit"
                                mobs[i]["health"] -= 1
                                if mobs[i]["health"] < 1:
                                    mobs[i] = None
                                    grid[bullet_grid_location[0]][bullet_grid_location[1]] = " "
                        while None in mobs:
                            mobs.remove(None)
                    elif grid[bullet_grid_location[0]][bullet_grid_location[1]] == "s":
                        # it hit a stone
                        print "hit a stone"
                        projectiles[i] = None
        while None in projectiles:
            projectiles.remove(None)

        
        draw_grid()
        display_health()
    else:
        pygame.event.pump()
        event = pygame.event.get()
        for my_event in event:
            if my_event.type == pygame.QUIT:
                sys.exit()

        screen.fill((204,153,255)) #colored background
        for t in title:
            menu_font = pygame.font.Font(None, 60)
            pygame.font.Font.set_underline(menu_font, True)
            t.draw()
        
        for option in options:
            menu_font = pygame.font.Font(None, 40)
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for my_event in event:
                    if my_event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        print option.text
                        if option.text == "Play game!":
                            playing_game = True
            else:
                option.hovered = False
            option.draw()
    pygame.display.update()
