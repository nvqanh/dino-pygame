import pygame as pg
from sys import exit

pg.init()
screen = pg.display.set_mode((1000, 600))
icon = pg.image.load("icon.png").convert()
pg.display.set_icon(icon)
pg.display.set_caption("Dino Run")
clock = pg.time.Clock()

bg_sf = pg.image.load("background.png").convert_alpha()

font = pg.font.Font("fonts/ari-w9500-condensed-display.ttf", 40)
score_sf = font.render("00000", False, "gray75")
score_rect = score_sf.get_rect(midtop = (900, 50))

idle_img = pg.image.load("player/dino-idle.png").convert_alpha() #Loads an image and convert it to pygame
dino_sf = pg.transform.scale_by(idle_img, 5) #Makes a surface, aka image on screen, with that image
dino_rect = dino_sf.get_rect(midbottom = (100, 430)) #Makes a rectangle (box) with that image

c1_img = pg.image.load("obstacles/cactus1.png").convert_alpha()
cactus_sf = pg.transform.scale_by(c1_img, 2)
cactus_rect = cactus_sf.get_rect(midbottom = (1000, 430))

speed_y = 0

while True:
    for event in pg.event.get():
        #Check if you want to exit
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        #Mouse 1
        # if event.type == pg.MOUSEMOTION: #if move mouse
            #  if player_rect.collidepoint(event.pos):
            #     print("collide with mouse")
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     print("mouse down")

        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_w:
        #         if dino_rect.bottom == 430:
        #             speed_x = -20

    screen.blit(bg_sf, (0, 0))

    screen.blit(dino_sf, dino_rect)
    
    screen.blit(cactus_sf, cactus_rect)
    cactus_rect.x -= 10
    if cactus_rect.right <= 0:
        cactus_rect.left = 1000

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
        if dino_rect.bottom == 430:
            speed_y = -20

    speed_y += 1
    dino_rect.top += speed_y
    if dino_rect.bottom >= 430:
        dino_rect.bottom = 430
        speed_y = 0

    screen.blit(score_sf, score_rect)

    #Collision between two rects
    if dino_rect.inflate(-80, -50).colliderect(cactus_rect.inflate(-30, -10)):
        print("GAME OVER")
        pg.quit()
        exit()
        #collided = True
    #elif not dino_rect.colliderect(cactus_rect):
        #collided = False

    #Collision with mouse 2
    # mouse_pos = pg.mouse.get_pos()
    # if dino_rect.collidepoint(mouse_pos):
    #     #print("touching mouse")
    #     #Check mouse press
    #     print(pg.mouse.get_pressed()) #-> tuple. First item is left click, second is scroll, third is right click

    #pg.draw.line(screen, "Blue", (500, 300), pg.mouse.get_pos(), 10)
    #pg.draw.ellipse(screen, "#9e3eca", pg.Rect(200, 100, 50, 50))

    #60 FPS
    pg.display.update()
    clock.tick(60)
