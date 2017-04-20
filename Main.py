import pygame
import sys
from Camera import Camera
from Sprite import *
from SpriteSheet import SpriteSheet

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_WIDTH = 1700
BACKGROUND_HEIGHT = 640

# Sprite Constants
WATER_LINE = 400

# PyGame setup
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Maelstrom")

# Global variables
Sprites = pygame.sprite.Group()   # sprites manager

def main():
    # variables
    left = right = up = down = False  # movement variables
    floor = 1                         # floor indicator
    platforms = []                    # platform manager
    timer = pygame.time.Clock()       # framerate manager
    background = Sprite("images/full background.png", 0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, 0)  # background image
    health_indicator = Sprite("sprite/Indicator.png", 0, WIN_HEIGHT, 0, 0, 3)
    Sprites.add(health_indicator)

    # phase 1 variables
    phase_one = False
    weather_sounds = pygame.mixer.Channel(2)
    radio_sounds = pygame.mixer.Channel(3)
    thunder = pygame.mixer.Sound("audio/heavy_rain_with_thunder.wav")
    phase1_warning = pygame.mixer.Sound("audio/phase1_warning.wav")
    stillwater = pygame.mixer.Sound("audio/flood.wav")
    zap = pygame.mixer.Sound("audio/zap_damage.wav")
    water = Sprite("sprite/water.png", 0, WIN_HEIGHT, 1700, 0, 3)
    Sprites.add(water)
    phase1_wait_now = phase1_wait_then = pygame.time.get_ticks()
    water_wait_now = water_wait_then = pygame.time.get_ticks()
    warning_wait_now = warning_wait_then = pygame.time.get_ticks()
    zap_wait_now = zap_wait_then = pygame.time.get_ticks()
    warning_over = False
    flood_over = False

    # load and play the music
    pygame.mixer.pre_init(44100, 16, 2, 4096) # frequency, size, channels, buffersize
    pygame.mixer.music.load("audio/background_music.mp3")
    pygame.mixer.music.play(-1)

    # build the level
    x = y = 0
    level = [
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                              PP        PP  ",
        "                              P          P  ",
        "                              P          P  ",      # house is aligned
        "                              P          P  ",
        "             PPPPPPPPPPPPPPPPPPP  PPPPPPPPP ",
        "             P                           PP ",
        "             P                           PP ",
        "                             PPPPPPPPP   PP ",
        "                             P           PP ",
        "                             P           PP ",
        "                             P           PP ",
        "                                            "]

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
    playerSheet = SpriteSheet("sprite/randi_sheet.png")
    playerSkin = Sprite("sprite/Blank.png", 0, 0, 0, 0, 2)
    player = Sprite("sprite/Blank.png", 445, (len(level)*25.5) - 35*2 - 10, 32, 40, 1)
    Sprites.add(player)
    Sprites.add(playerSkin)
    playerHealth = 5

    #ladderIndicator = Sprite("sprite/Indicator.png", 1240, (len(level)*25.5) - 35*2 - 5, 45, 45, 0)
    #Sprites.add(ladderIndicator)

    # game time
    while True:
        # read input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            #detecting button presses
            if event.type == pygame.KEYDOWN:
                # left movement
                if event.key == pygame.K_a:
                    left = True
                # right movement
                if event.key == pygame.K_d:
                    right = True
                # up movement
                if event.key == pygame.K_w:
                    up = True
                # down movement
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
                # Phase 1 is triggered
                if event.key == pygame.K_1:
                    phase_one = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_s:
                    down = False

        # get list of sprites
        spritesToModify = Sprites.sprites()

        for sprite in spritesToModify:
            # player manipulations
            if sprite.identity == 1:
                # get list of obj's colliding with current sprite
                hitList = pygame.sprite.spritecollide(sprite, Sprites, False)

                playerSkin.image = playerSheet.get_image(0, 0, round(222 / 3), 123)
                playerSkin.image = pygame.transform.smoothscale(playerSkin.image, (round(float(player.rect.width * 1.3)), player.rect.height))
                playerSkin.rect = playerSkin.image.get_rect()

                # update positions (using pixel-perfect movement)
                if sprite.rect.bottom <= BACKGROUND_HEIGHT and sprite.rect.top >= 0 and sprite.rect.right <= BACKGROUND_WIDTH \
                   and sprite.rect.left >= 0:
                    # movement
                    if sprite.identity == 1:
                        speedX = 0
                        # moving left
                        if left:
                            playerSkin.image = playerSheet.get_image(round(222 / 3)*2, 0, round(222 / 3), 123)
                            playerSkin.image = pygame.transform.smoothscale(playerSkin.image, (round(float(player.rect.width * 1.3)), player.rect.height))
                            speedX += -5
                        # moving right
                        if right:
                            playerSkin.image = playerSheet.get_image(round(222 / 3), 0, round(222 / 3), 123)
                            playerSkin.image = pygame.transform.smoothscale(playerSkin.image, (round(float(player.rect.width * 1.3)), player.rect.height))
                            speedX += 5
                        # movement up the ladders
                        if up:
                            # going upstairs
                            if floor == 1 and 1010 < sprite.rect.centerx < 1040:
                                sprite.rect.centery = 310
                                floor = 2
                            # going to first floor
                            if floor == 0 and 1275 < sprite.rect.centerx < 1305:
                                sprite.rect.centery = 450
                                floor = 1
                        # movement down the ladders
                        if down:
                            # going to basement
                            if floor == 1 and 1275 < sprite.rect.centerx < 1305:
                                sprite.rect.centery = 590
                                floor = 0
                            # going to the first floor
                            if floor == 2 and 1010 < sprite.rect.centerx < 1040:
                                sprite.rect.centery = 450
                                floor = 1

                        # moves the player
                        sprite.rect.centerx += speedX
                        playerSkin.rect.centerx = sprite.rect.centerx
                        playerSkin.rect.centery = sprite.rect.centery

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

            # if sprite.identity == 3:
            #     # get list of obj's colliding with current sprite
            #     hitList = pygame.sprite.spritecollide(sprite, Sprites, False)
            #     # collision handling for object
            #     for hit in hitList:
            #         if hit.identity == 1 or hit.identity == 2:  # the player was hit
            #             # TODO: Figure out how to diminish player health
            #             hit.rect.centery -= 1
            #
            #     # position adjustments
            #     while sprite.rect.bottom > BACKGROUND_HEIGHT:
            #         if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
            #             Sprites.remove(sprite)
            #         # sprite.rect.y -= 1
            #     while sprite.rect.top < 0:
            #         if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
            #             Sprites.remove(sprite)
            #         # sprite.rect.y += 1
            #     while sprite.rect.right > BACKGROUND_WIDTH:
            #         if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
            #             Sprites.remove(sprite)
            #         sprite.rect.x -= 1
            #     while sprite.rect.left < 0:
            #         if sprite.destructable:  # if the obj is destructible and it hits a wall, get rid of it
            #             Sprites.remove(sprite)
            #         sprite.rect.x += 1

        # Executes Phase 1 if triggered
        if phase_one:
            water_wait_now = zap_wait_now = pygame.time.get_ticks()

            # Plays the thunder with rain sound effect
            if not weather_sounds.get_busy() and not flood_over:
                    weather_sounds.play(thunder)

            # Plays the radio warning
            if not radio_sounds.get_busy() and not warning_over and not flood_over:
                warning_wait_then = pygame.time.get_ticks()
                # radio_sounds.play(phase1_warning)

            warning_wait_now = pygame.time.get_ticks()

            # Waits for the audio to finish
            if warning_wait_now - warning_wait_then >= 00:
                warning_over = True

            # As soon as the radio is finished, begin the flood
            if not radio_sounds.get_busy() and warning_over and not flood_over:
                # Moves the waterline progressively upward
                if water.rect.y > WATER_LINE:
                    if water_wait_now - water_wait_then > 100:
                        water.rect.y -= 1
                        water.height += 1
                        water.image = pygame.transform.scale(water.image, (1700, water.height))
                        water.rect = water.rect.clip(pygame.Rect(0, 0, 1700, water.height))
                        water_wait_then = water_wait_now
                else:
                    weather_sounds.fadeout(3000)
                    phase1_wait_then = pygame.time.get_ticks()
                    flood_over = True

            # If the player reaches below the waterline, he will become damaged
            if water.rect.y < player.rect.bottom < WIN_HEIGHT:
                health_indicator.rect.y = 0
                health_indicator.image = pygame.transform.scale(health_indicator.image,
                                                                (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
                if zap_wait_now - zap_wait_then > 1000:
                    zap.play()
                    zap_wait_then = zap_wait_now
                    playerHealth -= 1
            else:
                health_indicator.rect.y = WIN_HEIGHT

            # Wait for 10 seconds, then wait for the water to recede
            if phase1_wait_now - phase1_wait_then > 10000 and flood_over:
                if water.rect.y < 640:
                    if water_wait_now - water_wait_then > 100:
                        water.rect.y += 1
                        water.height -= 1
                        water_wait_then = water_wait_now
                else:
                    phase_one = False

            phase1_wait_now = pygame.time.get_ticks()

        # draw stuff
        screen.fill((0, 0, 0))
        screen.blit(background.image, background.rect)  # fills screen with background
        camera.update(player)  # camera will follow the player

        # draw everything using blit over the .draw() function (more control with camera)
        for sprite in Sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        #hp display
        HeartDisplay(playerHealth)

        screen.blit(player.image, camera.apply(player))

        pygame.display.flip()
        timer.tick(60)

def HeartDisplay(playerHP):
    # Health Display If Chain
    # heart 1
    if (playerHP > 0):
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_red.png"), (32, 32)),
                    (32, 10, 32, 32))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_black.png"), (32, 32)),
                    (32, 10, 32, 32))

    # heart 2
    if (playerHP > 1):
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_red.png"), (32, 32)),
                    (32 * 2 + 5, 10, 32, 32))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_black.png"), (32, 32)),
                    (32 * 2 + 5, 10, 32, 32))

    # heart 3
    if (playerHP > 2):
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_red.png"), (32, 32)),
                    (32 * 3 + 10, 10, 32, 32))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_black.png"), (32, 32)),
                    (32 * 3 + 10, 10, 32, 32))

    # heart 4
    if (playerHP > 3):
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_red.png"), (32, 32)),
                    (32 * 4 + 15, 10, 32, 32))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_black.png"), (32, 32)),
                    (32 * 4 + 15, 10, 32, 32))

    # heart 5
    if (playerHP > 4):
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_red.png"), (32, 32)),
                    (32 * 5 + 20, 10, 32, 32))
    else:
        screen.blit(pygame.transform.scale(pygame.image.load("images/heart_black.png"), (32, 32)),
                    (32 * 5 + 20, 10, 32, 32))

def phase1():
    phase1 = True
    thunder = pygame.mixer.Sound("audio/heavy_rain_with_thunder.wav")
    thunder.play()
    cloudX = 0
    waterY = 300
    #cloud0 = Sprite("sprite/cloud0.png", cloudX, 20, 1000, 200, 0)
    #cloud1 = Sprite("sprite/cloud1.png", BACKGROUND_WIDTH-cloudX, 30, 1000, 200, 0)
    #cloud2 = Sprite("sprite/cloud2.png", cloudX, 40, 1000, 200, 0)
    water = Sprite("sprite/water2.png", 0, 0, 300, 300)
    #Sprites.add(cloud0)
    #Sprites.add(cloud1)
    #Sprites.add(cloud2)
    Sprites.add(water)

    while phase1:
        if water.rect.centery < WIN_HEIGHT/2:
            water.rect.centery -= 10
        else:
            phase1 = False


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