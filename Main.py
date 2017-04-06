import pygame
import sys
from Camera import Camera
from Sprite import *

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_WIDTH = 1700
BACKGROUND_HEIGHT = 640

# Start setting up PyGame
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Maelstrom")


def main():
    # variables
    left = right = up = down = False
    floor = 1
    Sprites = pygame.sprite.Group()
    platforms = []
    timer = pygame.time.Clock()
    background = Sprite("sprite/Background.png", 0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, 0)

    x = y = 0
    level = [
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                                           ",
        "                             P          P  ",
        "                             P          P  ",
        "                             P          P  ",      #house is aligned
        "                             P           P ",
        "                             P           P ",
        "                                         P ",
        "            P                            P ",
        "                             P           P ",
        "                             P           P ",
        "                             P           P ",
        "                             P           P ",
        "                                           "]


    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                Sprites.add(p)
            x += 32
        y += 32
        x = 0

    # create the camera with a complex camera (will autofit to the boundaries of the screen
    camera = Camera(complex_camera, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)

    # create the player
    player = Sprite("sprite/DisasterPlayer.png", 415, (len(level)*25.5) - 35*2 - 10, 32, 40, 1)
    Sprites.add(player)
    #ladderIndicator = Sprite("sprite/Indicator.png", 1240, (len(level)*25.5) - 35*2 - 5, 45, 45, 0)
    #Sprites.add(ladderIndicator)

    # game time
    while True:
        # read input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    left = True
                if event.key == pygame.K_d:
                    right = True
                if event.key == pygame.K_w:
                    up = True
                if event.key == pygame.K_s:
                    down = True
                if event.key == pygame.K_a and event.key == pygame.K_w:
                    left = True
                    up = False
                if event.key == pygame.K_a and event.key == pygame.K_s:
                    left = True
                    down = False
                if event.key == pygame.K_d and event.key == pygame.K_w:
                    right = True
                    up = False
                if event.key == pygame.K_d and event.key == pygame.K_s:
                    right = True
                    down = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_s:
                    down = False

        spritesToModify = Sprites.sprites()  # get list of sprites
        for sprite in spritesToModify:
            # player manipulations
            if sprite.identity == 1:
                # get list of obj's colliding with current sprite
                hitList = pygame.sprite.spritecollide(sprite, Sprites, False)

                # update positions (using pixel-perfect movement)
                if sprite.rect.bottom <= BACKGROUND_HEIGHT and sprite.rect.top >= 0 and sprite.rect.right <= BACKGROUND_WIDTH \
                   and sprite.rect.left >= 0:
                    # movement
                    if sprite.identity == 1:
                        speedX = 0
                        speedY = 0
                        if left:
                            speedX += -5
                        if right:
                            speedX += 5
                        # movement up the ladders
                        if up:
                            # going upstairs
                            if floor == 1 and sprite.rect.centerx > 985 and sprite.rect.centerx < 1015:
                                sprite.rect.centery -= 140
                                floor = 2
                            # going to first floor
                            if floor == 0 and sprite.rect.centerx > 1245 and sprite.rect.centerx < 1275:
                                sprite.rect.centery -= 140
                                floor = 1
                        # movement down the ladders
                        if down:
                            # going to basement
                            if floor == 1 and sprite.rect.centerx > 1245 and sprite.rect.centerx < 1275:
                                sprite.rect.centery += 140
                                floor = 0
                            # going to the first floor
                            if floor == 2 and sprite.rect.centerx > 985 and sprite.rect.centerx < 1015:
                                sprite.rect.centery += 140
                                floor = 1

                        # moves the player
                        sprite.rect.centerx += speedX

                        # moves the background along with the player
                        background.rect.x -= speedX

                        # collision handling for player
                        for hit in hitList:
                            if hit.identity == 0:  # a barrier was hit
                                if speedX > 0:  # was moving right
                                    while pygame.sprite.collide_rect(player, hit):  # correction
                                        player.rect.centerx -= 1
                                        background.rect.x += 1
                                if speedX < 0:  # was moving left
                                    while pygame.sprite.collide_rect(player, hit):  # correction
                                        player.rect.centerx += 1
                                        background.rect.x -= 1
                                if speedY > 0: #down
                                    while pygame.sprite.collide_rect(player, hit):
                                        player.rect.centery -= 1
                                #        background.rect.y -= 1
                                if speedY < 0: #up
                                    while pygame.sprite.collide_rect(player, hit):
                                        player.rect.centery += 1
                                #        background.rect.y += 1

                # position adjustments
                while sprite.rect.bottom > BACKGROUND_HEIGHT:
                    if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
                        Sprites.remove(sprite)
                    # sprite.rect.y -= 1
                while sprite.rect.top < 0:
                    if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
                        Sprites.remove(sprite)
                    # sprite.rect.y += 1
                while sprite.rect.right > BACKGROUND_WIDTH:
                    if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
                        Sprites.remove(sprite)
                    sprite.rect.x -= 1
                while sprite.rect.left < 0:
                    if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
                        Sprites.remove(sprite)
                    sprite.rect.x += 1

        # draw stuff
        screen.fill((0, 0, 0))
        screen.blit(background.image, background.rect)
        camera.update(player)  # camera will follow the player

        # draw everything using blit over the .draw() function (more control with camera)
        for sprite in Sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        screen.blit(player.image, camera.apply(player))

        pygame.display.flip()
        timer.tick(60)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h  # center player

    l = min(0, l)  # stop scrolling at the left edge
    l = max(-(camera.width - WIN_WIDTH), l)  # stop scrolling at the right edge
    t = max(-(camera.height - WIN_HEIGHT), t)  # stop scrolling at the bottom
    t = min(0, t)  # stop scrolling at the top

    return pygame.Rect(l, t, w, h)


class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, "sprite/Blank.png", x, y, 32, 32)

    def update(self):
        pass

if __name__ == "__main__":
    main()
