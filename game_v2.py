import pygame
import sys
import time

pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
size = width, height = 512, 512
pygame.display.set_mode(size, pygame.DOUBLEBUF)
black = 50, 50, 50
screen = pygame.display.set_mode(size)

grid = [["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "s", "", "", "", "", "", "", "", ""],
        ["", "", "r", "", "", "", "", "s", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "g", "s", "", "", "", "", "", "", "", ""],
        ["", "", "", "s", "s", "s", "s", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "s", "s", "s", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "", "", "", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "", "", "", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "", "", "", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "s", "", "s", "", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "s", "s", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]


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
                image = pygame.image.load("pirate.png")
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
                image = pygame.image.load("objective.png")
                rect = image.get_rect()
                rect.x = r*32
                rect.y = c*32
                screen.blit(image, rect)


# stuff for player movement
last_moved = 0
currently_moving = False
player_direction = "r"
player_location = [0, 0]
grid[player_location[0]][player_location[1]] = "p"
player_health = 10


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

            if spot[0] + 1 < len(a_star_grid) and a_star_grid[spot[0] + 1][spot[1] + 0] == " " and grid[spot[0] + 1][spot[1]] != "s":
                new_spreading_spots += [(spot[0] + 1, spot[1] + 0)]
                a_star_grid[spot[0] + 1][spot[1] + 0] = "u"

            if spot[0] - 1 >= 0 and a_star_grid[spot[0] - 1][spot[1] + 0] == " " and grid[spot[0] - 1][spot[1]] != "s":
                new_spreading_spots += [(spot[0] - 1, spot[1] + 0)]
                a_star_grid[spot[0] - 1][spot[1] + 0] = "d"

            if spot[1] + 1 < len(a_star_grid) and a_star_grid[spot[0] + 0][spot[1] + 1] == " " and grid[spot[0]][spot[1] + 1] != "s":
                new_spreading_spots += [(spot[0] + 0, spot[1] + 1)]
                a_star_grid[spot[0] + 0][spot[1] + 1] = "r"

            if spot[1] - 1 >= 0 and a_star_grid[spot[0] + 0][spot[1] - 1] == " " and grid[spot[0]][spot[1] - 1] != "s":
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
    f = open(file_name)
    grid = []
    for line in f:
        grid += line.split(",")
    for r in range(len(grid)):
        for c in range(len(grid)):
            if grid[r][c] == "r":
                mobs += [{"type": "REAPER", "position": [r, c]}]
            if grid[r][c] == "p":
                player_location = [r, c]
projectiles = []

def display_text(text):
    screen.fill(black)
    count = 1
    for l in text.split("\n"):
        label = myfont.render(l, 1, (0,255,255))
        screen.blit(label, (50, count*20 + 100))
        pygame.display.update()
        count += 1
    time.sleep(len(text) / 10)

while 1:
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
        grid[player_location[0]][player_location[1]] = ""
        if player_direction == "d" and player_location[1] + 1 < len(grid) and grid[player_location[0]][player_location[1] + 1] == ""  or grid[player_location[0]][player_location[1] + 1] == "g":
            player_location[1] += 1
        if player_direction == "u" and player_location[1] - 1 >= 0 and grid[player_location[0]][player_location[1] - 1] == "" or grid[player_location[0]][player_location[1] - 1] == "g":
            player_location[1] -= 1
        if player_direction == "r" and (player_location[0] + 1 < len(grid)) and grid[player_location[0] + 1][player_location[1]] == "" or grid[player_location[0] + 1][player_location[1]] == "g":
            player_location[0] += 1
        if player_direction == "l"  and player_location[0] - 1 >= 0 and grid[player_location[0] - 1][player_location[1]] == "" or grid[player_location[0] - 1][player_location[1]] == "g":
            player_location[0] -= 1
        if grid[player_location[0]][player_location[1]] == "g":
            display_text("""hey you found some sort of object!\nthats probably good!""")
        grid[player_location[0]][player_location[1]] = "p"

    if time.time() - last_enemy_move > 0.4:
        last_enemy_move = time.time()
        for mob in mobs:
            grid[mob["position"][0]][mob["position"][1]] = ""
            if mob["type"] == "REAPER":
                next_position = get_next_reaper_position(mob["position"])
                if next_position[0] == player_location[0] and next_position[1] == player_location[1]:
                    player_health -= 1
                    if player_health == 0:
                        display_text("GAME OVER!!!")
                else:
                    mob["position"] = next_position
                grid[mob["position"][0]][mob["position"][1]] = "r" 
    screen.fill(black)
    for i in range(len(projectiles)):
        if projectiles[i]["name"] == "bullet":
                image = pygame.image.load("bullet.png")
                rect = image.get_rect()
                rect.x = projectiles[i]["position"][0]
                rect.y = projectiles[i]["position"][1]
                screen.blit(image, rect)
                projectiles[i]["position"][0] += projectiles[i]["speed"][0]
                projectiles[i]["position"][1] += projectiles[i]["speed"][1]

                # ok so now we need a switch for the different things that could be at the bullets location
                if (projectiles[i]["position"][0] / 32) < 16 and (projectiles[i]["position"][0]/32) <16 and (projectiles[i]["position"][0]/32) > 0 and (projectiles[0]["position"][0]/32) > 0:
                    bullet_grid_location = [int(projectiles[i]["position"][0] / 32), int(projectiles[i]["position"][0]/32)]
            
                
                if grid[bullet_grid_location[0]][bullet_grid_location[1]] == "r":
                    # it hit a reaper
                    print "hit a reaper"


    
    draw_grid()
    display_health()
    pygame.display.update()
