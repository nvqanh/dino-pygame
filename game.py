import pygame as pg
from sys import exit

def display_score():
    global score
    global font
    global start_time
    score_sf = font.render(f"{score:05d}", False, "gray75")
    score_rect = score_sf.get_rect(midtop = (900, 50))
    screen.blit(score_sf, score_rect)

def display_high_score():
    global high_score
    global font
    global start_time
    high_score_sf = font.render(f"HI {high_score:05d}", False, "gray60")
    high_score_rect = high_score_sf.get_rect(midtop = (720, 50))
    screen.blit(high_score_sf, high_score_rect)

pg.init()
screen = pg.display.set_mode((1000, 600))
icon = pg.image.load("icon.png").convert()
pg.display.set_icon(icon)
pg.display.set_caption("Dino Run")
clock = pg.time.Clock()

bg_sf = pg.image.load("background.png").convert_alpha()

font = pg.font.Font("fonts/ari-w9500-condensed-display.ttf", 35)

idle_img = pg.image.load("player/dino-idle.png").convert_alpha() # Loads an image and convert it to pygame
dino_sf = pg.transform.scale_by(idle_img, 5) # Makes a surface, aka image on screen, with that image
dino_rect = dino_sf.get_rect(midbottom = (100, 430)) # Makes a rectangle (box) with that image

c1_img = pg.image.load("obstacles/cactus1.png").convert_alpha()
cactus_sf = pg.transform.scale_by(c1_img, 2)
cactus_rect = cactus_sf.get_rect(midbottom = (1500, 430))

player_speed_y = 0
cactus_speed_x = 8

cooldown = 20

ingame = True

start_time = pg.time.get_ticks()
score = 0
high_score = 0

while True:
    for event in pg.event.get():
        # Check if you want to exit
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if not ingame and ((event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_UP)) or event.type == pg.MOUSEBUTTONDOWN):
            dino_rect.midbottom = (100, 430)
            cactus_rect.midbottom = (1500, 430)

            player_speed_y = 0
            cactus_speed_x = 8

            ingame = True
            cooldown = 20

            start_time = pg.time.get_ticks()
            continue

    if ingame:
        score = int((pg.time.get_ticks() - start_time) / 100)

        screen.blit(bg_sf, (0, 0))

        screen.blit(dino_sf, dino_rect)
        
        screen.blit(cactus_sf, cactus_rect)
        cactus_rect.x -= cactus_speed_x
        if cactus_speed_x <= 25: cactus_speed_x += .001
        if cactus_rect.right <= 0:
            cactus_rect.left = 1000

        keys = pg.key.get_pressed()
        if (keys[pg.K_SPACE] or keys[pg.K_UP] or pg.mouse.get_pressed()[0]) and cooldown == 0:
            if dino_rect.bottom == 430:
                player_speed_y = -20
        
        if cooldown > 0:
            cooldown -= 1

        player_speed_y += 1
        dino_rect.y += player_speed_y
        if dino_rect.bottom >= 430:
            dino_rect.bottom = 430
            player_speed_y = 0

        # Game over
        if dino_rect.inflate(-80, -50).colliderect(cactus_rect.inflate(-30, -10)):
            ingame = False
            if score > high_score:
                high_score = score

        display_score()
        display_high_score()

    # 60 FPS
    pg.display.update()
    clock.tick(60)
