import pygame
import sys
from Camera import Camera
from Sprite import *
from SpriteSheet import SpriteSheet
import StoreMenu
import Inventory

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
pygame.display.set_caption("R.A.N.D.I.")

# Global variables
Sprites = pygame.sprite.Group()   # sprites manager
playerHealth = 5

EXTINGUISHER = 0;
BOOTS = 1;
AID = 2;


#todo implementations for these
def equip_extinguisher():
    ()

def equip_boots():
    ()

def use_aid():
    global playerHealth
    playerHealth += 1
    HeartDisplay(playerHealth)

def main():
    global playerHealth
    # variables
    running = True                    # indicates whether or not the game is running
    left = right = up = down = False  # movement variables
    floor = 1                         # floor indicator
    platforms = []                    # platform manager
    timer = pygame.time.Clock()       # framerate manager

    background = Sprite("images/background.png", 0, 0, 0, 0, 0)  # background image
    background.image = pygame.transform.smoothscale(background.image, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    startscreen = Sprite("images/startscreen.png", 0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, 0)
    health_indicator = Sprite("sprite/Indicator.png", 0, WIN_HEIGHT, 0, 0, 3)
    Sprites.add(health_indicator)
    equippedItem = -1;

    # PHASE 1 VARIABLES
    phase_one = False
    fridge_disconnected = False
    has_healthkit = False

    # Sound bytes
    weather_sounds = pygame.mixer.Channel(2)
    radio_sounds = pygame.mixer.Channel(3)
    thunder = pygame.mixer.Sound("audio/heavy_rain_with_thunder.wav")
    phase1_warning = pygame.mixer.Sound("audio/phase1_warning.wav")
    zap = pygame.mixer.Sound("audio/zap_damage.wav")
    cha_ching = pygame.mixer.Sound("audio/cha_ching.wav")

    # Object sprites
    water = Sprite("sprite/water.png", 0, WIN_HEIGHT, 1700, 0, 3)
    fridge = Sprite("sprite/fridge_on.png", 1100, 545, 0, 0, 3)
    fridge_on = pygame.image.load("sprite/fridge_on.png")
    fridge_on = pygame.transform.smoothscale(fridge_on, (80, 45))
    fridge_off = pygame.image.load("sprite/fridge_off.png")
    fridge_off = pygame.transform.smoothscale(fridge_off, (80, 45))
    fridge.image = pygame.transform.smoothscale(fridge.image, (80, 45))
    Sprites.add(water)
    Sprites.add(fridge)

    # Cloud sprites
    cloud0 = Sprite("sprite/cloud0.png", -300, 0, 0, 0, 3)
    cloud1 = Sprite("sprite/cloud1.png", -300, 0, 0, 0, 3)
    cloud2 = Sprite("sprite/cloud2.png", 2000, 0, 0, 0, 3)
    cloud3 = Sprite("sprite/cloud0.png", -300, 0, 0, 0, 3)
    cloud4 = Sprite("sprite/cloud1.png", -300, 0, 0, 0, 3)
    cloud5 = Sprite("sprite/cloud2.png", 2000, 0, 0, 0, 3)
    cloud0.image = pygame.transform.smoothscale(cloud0.image, (300, 200))  # 300 x 200
    cloud1.image = pygame.transform.smoothscale(cloud1.image, (300, 200))
    cloud2.image = pygame.transform.smoothscale(cloud2.image, (300, 200))
    cloud3.image = pygame.transform.smoothscale(cloud0.image, (300, 200))
    cloud4.image = pygame.transform.smoothscale(cloud1.image, (300, 200))
    cloud5.image = pygame.transform.smoothscale(cloud2.image, (300, 200))
    Sprites.add(cloud0)
    Sprites.add(cloud1)
    Sprites.add(cloud2)
    Sprites.add(cloud3)
    Sprites.add(cloud4)
    Sprites.add(cloud5)

    # Rain sprites
    rain1 = Sprite("sprite/rain1.png", 0, -WIN_HEIGHT, 0, 0)
    rain2 = Sprite("sprite/rain1.png", 0, - (2 * WIN_HEIGHT), 0, 0)
    rain1.image = pygame.transform.smoothscale(rain1.image, (BACKGROUND_WIDTH, WIN_HEIGHT))
    rain2.image = pygame.transform.smoothscale(rain2.image, (BACKGROUND_WIDTH, WIN_HEIGHT))
    Sprites.add(rain1)
    Sprites.add(rain2)

    # Timer variables
    phase1_wait_now = phase1_wait_then = pygame.time.get_ticks()
    water_wait_now = water_wait_then = pygame.time.get_ticks()
    warning_wait_now = warning_wait_then = pygame.time.get_ticks()
    zap_wait_now = zap_wait_then = pygame.time.get_ticks()
    warning_over = False
    flood_over = False
    interact_on = False

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
        "                              PP        PPPP",
        "                              P          PPP",
        "                              P          PPP",      # house is aligned
        "                              P          PPP",
        "             PPPPPPPPPPPPPPPPPPP        PPPP",
        "             P                           PPP",
        "             P                           PPP",
        "                             PPP         PPP",
        "                             P           PPP",
        "                             P           PPP",
        "                             P           PPP",
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


    end_it = False
    while(end_it == False):
        screen.fill((0,0,0))
        screen.blit(startscreen.image, startscreen.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            # detecting button presses
            if event.type == pygame.KEYDOWN:
                # enter key
                if event.key == pygame.K_RETURN:
                    end_it = True
        pygame.display.flip()

    # game time
    while running:
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
                if event.key == pygame.K_SPACE:
                    interact_on = True
                if event.key == pygame.K_b:
                    Inventory.addItems(StoreMenu.openMenu())
                if event.key == pygame.K_i:
                    #returns number key in itemDict if an item equipped, or -1 if cancelled before equipping
                    left = False
                    right = False
                    down = False
                    up = False
                    pygame.image.save(screen, "images/savedForInv.png")
                    pic = pygame.image.load("images/savedForInv.png")

                    equippedItem = Inventory.openInventory(pic)
                    if equippedItem == AID:
                        use_aid()
                    elif equippedItem == EXTINGUISHER:
                        equip_extinguisher()
                    elif equippedItem == BOOTS:
                        equip_boots()

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
                            playerSkin.image = playerSheet.get_image(round(222 / 3)+3, 0, round(222 / 3), 123)
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
                        # unplugs the freezer
                        if interact_on:
                            if 1100 < sprite.rect.centerx < 1180 and 450 < sprite.rect.centery < 640:
                                if not fridge_disconnected:
                                    fridge.image = fridge_off
                                    fridge_disconnected = True
                                    cha_ching.play()
                                    StoreMenu.giveMoney(40)
                                else:
                                    fridge.image = fridge_on
                                    fridge_disconnected = False
                                    cha_ching.play()
                                    StoreMenu.giveMoney(-40)
                                interact_on = False
                            else:
                                interact_on = False

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

        # Executes Phase 1 if triggered
        if phase_one:
            water_wait_now = zap_wait_now = pygame.time.get_ticks()

            # Plays the thunder with rain sound effect
            if not weather_sounds.get_busy() and not flood_over:
                    weather_sounds.play(thunder)

            # Plays the radio warning
            if not radio_sounds.get_busy() and not warning_over and not flood_over:
                warning_wait_then = pygame.time.get_ticks()
                radio_sounds.play(phase1_warning)

            warning_wait_now = pygame.time.get_ticks()

            # Animates rain drops and clouds; also waits for audio to finish
            if warning_wait_now - warning_wait_then >= 200 and not flood_over:
                warning_over = True
                if cloud0.rect.x < 800:
                    cloud0.rect.x += 5
                else:
                    if rain1.rect.y < WIN_HEIGHT:
                        rain1.rect.y += 10
                        rain2.rect.y += 10
                    if rain1.rect.y == WIN_HEIGHT:
                        rain1.rect.y = - WIN_HEIGHT
                        rain2.rect.y += 10
                    if rain2.rect.y == WIN_HEIGHT:
                        rain1.rect.y += 10
                        rain2.rect.y = - WIN_HEIGHT

                if cloud1.rect.x < 1000:
                    cloud1.rect.x += 6
                if cloud2.rect.x > 1200:
                    cloud2.rect.x -= 5
                if cloud3.rect.x < 800:
                    cloud3.rect.x += 6
                if cloud4.rect.x < 600:
                    cloud4.rect.x += 5
                if cloud5.rect.x > 1400:
                    cloud5.rect.x -= 5

            # Stops the rain and removes the clouds
            if flood_over:
                if rain1.rect.y < WIN_HEIGHT:
                    rain1.rect.y += 10
                if rain2.rect.y < WIN_HEIGHT:
                    rain2.rect.y += 10
                if cloud0.rect.x > 0:
                    cloud0.rect.x -= 5
                if cloud1.rect.x > -300:
                    cloud1.rect.x -= 5
                if cloud2.rect.x < BACKGROUND_WIDTH:
                    cloud2.rect.x += 5
                if cloud3.rect.x > -300:
                    cloud3.rect.x -= 5
                if cloud4.rect.x > -300:
                    cloud4.rect.x -= 5
                if cloud5.rect.x < BACKGROUND_WIDTH:
                    cloud5.rect.x += 5

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
                health_indicator.rect.y = 0  # adds the red screen
                health_indicator.image = pygame.transform.scale(health_indicator.image,
                                                                (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
                if zap_wait_now - zap_wait_then > 1000:
                    zap.play()
                    zap_wait_then = zap_wait_now
                    if playerHealth > 0:
                        playerHealth -= 1

                    if playerHealth == 0:
                        zap.stop()
                        Sprites.empty()

            else:
                health_indicator.rect.y = WIN_HEIGHT  # removes the red screen

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
    #gameover = Sprite("images/gameover.png", 0, 0, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
    if (playerHP == 0):
        #screen.fill((0, 0, 0))
        screen.blit(pygame.image.load("images/gameover.png"), (0,0))
        pygame.mixer.music.stop()
        pygame.mixer.Channel(1).stop()
        pygame.mixer.Channel(2).stop()
        pygame.mixer.Channel(3).stop()
        #Sprites.empty()
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