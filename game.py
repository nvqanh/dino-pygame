# TODO:
# - Animations for dino
# - Different cactus types
# - Multiple cactus rects <implementing>
# - Pterodactyls
# - Moon and stars

import pygame as pg
import random
from sys import exit

def display_score():
    global score
    global font1
    global start_time
    score_sf = font1.render(f"{score:05d}", False, "gray75")
    score_rect = score_sf.get_rect(midtop = (900, 50))
    screen.blit(score_sf, score_rect)

def display_high_score():
    global high_score
    global font1
    global start_time
    high_score_sf = font1.render(f"HI {high_score:05d}", False, "gray60")
    high_score_rect = high_score_sf.get_rect(midtop = (720, 50))
    screen.blit(high_score_sf, high_score_rect)

pg.init()
screen = pg.display.set_mode((1000, 600))
icon = pg.image.load("icon.png").convert()
pg.display.set_icon(icon)
pg.display.set_caption("Dino Run")
clock = pg.time.Clock()

# NOTE: width 1000 height 600

bg_sf = pg.image.load("background.png").convert_alpha()
ground_sf = pg.image.load("ground.png").convert_alpha()
ground_rect1 = ground_sf.get_rect(bottomleft = (0, 600))
ground_rect2 = ground_sf.get_rect(bottomleft = (1000, 600))

font1 = pg.font.Font("fonts/ari-w9500-display.ttf", 35)
font2 = pg.font.Font("fonts/ari-w9500-display.ttf", 50)
font3 = pg.font.Font("fonts/ari-w9500-bold.ttf", 35)

idle_img = pg.image.load("player/dino-idle.png").convert_alpha() # Loads an image and convert it to pygame
dino_sf = pg.transform.scale_by(idle_img, 5.2) # Makes a surface, aka image on screen, with that image
dino_rect = dino_sf.get_rect(midbottom = (100, 430)) # Makes a rectangle (box) with that image

c1_img = pg.image.load("obstacles/cactus1.png").convert_alpha()
cactus_sf = pg.transform.scale_by(c1_img, 2.3)
cactus_rect1 = cactus_sf.get_rect(midbottom = (1500, 430))
cactus_rect2 = cactus_sf.get_rect(midbottom = (2500, 430))

game_over_sf = font2.render("GAME OVER", False, "gray75")
game_over_rect = game_over_sf.get_rect(midtop = (500, 200))
restart_txt_sf = font3.render("Space or Click to restart", False, "gray60")
restart_txt_rect = restart_txt_sf.get_rect(midtop = (500, 275))

player_speed_y = 0
speed_x = 8

cooldown = 20

ingame = True

start_time = pg.time.get_ticks()
score = 0

# Loads high score from highscore.txt
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0

while True:
    # Event loop
    for event in pg.event.get():
        # Check if you want to exit
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if not ingame and ((event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_UP)) or event.type == pg.MOUSEBUTTONDOWN):
            dino_rect.midbottom = (100, 430)
            cactus_rect1.midbottom = (1500, 430)
            cactus_rect2.midbottom = (2500, 430)

            ground_rect1.left = 0
            ground_rect2.left = 1000

            player_speed_y = 0
            speed_x = 8

            ingame = True
            cooldown = 20

            start_time = pg.time.get_ticks()
            continue

    if ingame:
        score = int((pg.time.get_ticks() - start_time) / 100)

        screen.blit(bg_sf, (0, 0))
        # screen.fill((32, 33, 36))

        screen.blit(ground_sf, ground_rect1)
        screen.blit(ground_sf, ground_rect2)

        # When a ground rect goes out of the screen, move it to exactly the right of the other

        ground_rect1.x -= speed_x
        ground_rect2.x -= speed_x
        if ground_rect1.right <= 0:
            ground_rect1.left = ground_rect2.right
        elif ground_rect2.right <= 0:
            ground_rect2.left = ground_rect1.right
 
        screen.blit(dino_sf, dino_rect)
        
        screen.blit(cactus_sf, cactus_rect1)
        screen.blit(cactus_sf, cactus_rect2)
        cactus_rect1.x -= speed_x
        cactus_rect2.x -= speed_x

        #Spawns cacti
        if speed_x <= 25: speed_x += .001
        if cactus_rect1.right <= 0:
            if cactus_rect2.right < 1000:
                #Try to spawn from the right but if the two cacti are too close then keep a distance of 300-500
                cactus_rect1.left = max(random.randint(1000, 2000), cactus_rect2.right + random.randint(300, 500))
            else:
                cactus_rect1.left = cactus_rect2.right + random.randint(300, 1500)
        if cactus_rect2.right <= 0:
            if cactus_rect1.right < 1000:
                cactus_rect2.left = max(random.randint(1000, 2000), cactus_rect1.right + random.randint(300, 500))
                cactus_rect2.left = cactus_rect1.right + random.randint(300, 1500)

        keys = pg.key.get_pressed()
        if (keys[pg.K_SPACE] or keys[pg.K_UP] or pg.mouse.get_pressed()[0]) and cooldown == 0:
            if dino_rect.bottom == 430:
                player_speed_y = -22
        
        if cooldown > 0:
            cooldown -= 1

        if keys[pg.K_DOWN]:
            player_speed_y += 3
        else: player_speed_y += 1

        dino_rect.y += player_speed_y
        if dino_rect.bottom >= 430:
            dino_rect.bottom = 430
            player_speed_y = 0

        # Game over
        if dino_rect.inflate(-80, -50).colliderect(cactus_rect1.inflate(-30, -10)) or dino_rect.inflate(-80, -50).colliderect(cactus_rect2.inflate(-30, -10)):
            ingame = False
            if score > high_score:
                high_score = score

                # with open() is recommended
                with open("highscore.txt", "w") as file:
                    file.write(str(high_score))

        display_score()
        display_high_score()
    else:
        screen.blit(game_over_sf, game_over_rect)
        screen.blit(restart_txt_sf, restart_txt_rect)

    # 60 FPS
    pg.display.update()
    clock.tick(60)
