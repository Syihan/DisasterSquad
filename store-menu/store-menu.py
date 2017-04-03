import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (186, 0, 0)
YELLOW = (234, 150, 0)
GREEN = (0, 104, 56)
BLUE = (0, 89, 219)

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HEADER_HEIGHT = int(WIN_HEIGHT / 6)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

def draw_table_structure(screen):
    # top parts
    pygame.draw.rect(screen, WHITE, [2, 2, HALF_WIDTH - 4, HEADER_HEIGHT])
    pygame.draw.rect(screen, WHITE, [HALF_WIDTH, 2, HALF_WIDTH - 2, HEADER_HEIGHT])

    # # main parts
    pygame.draw.rect(screen, WHITE, [2, HEADER_HEIGHT+4, HALF_WIDTH-4, WIN_HEIGHT-HEADER_HEIGHT-6])
    pygame.draw.rect(screen, WHITE, [HALF_WIDTH, HEADER_HEIGHT+4, HALF_WIDTH-2, WIN_HEIGHT-HEADER_HEIGHT-6])




pygame.init()
pygame.font.init()
size = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(size)

headerFont = pygame.font.Font(None, 68)
storeItemsText = headerFont.render("Store Items", 1, YELLOW)
yourItemsText = headerFont.render("Your Items", 1, BLUE)

clock = pygame.time.Clock()

started = False
done = False

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            left = True
        elif event.key == pygame.K_d:
            right = True
        elif event.key == pygame.K_w:
            up = True
        elif event.key == pygame.K_s:
            down = True

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_d:
            right = False
        if event.key == pygame.K_a:
            left = False
        if event.key == pygame.K_w:
            up = False
        if event.key == pygame.K_s:
            down = False


    screen.fill(BLACK)

    draw_table_structure(screen)
    screen.blit(storeItemsText, (HALF_WIDTH/6, HEADER_HEIGHT/3))
    screen.blit(yourItemsText, (HALF_WIDTH+HALF_WIDTH/6 + 10, HEADER_HEIGHT/3))

    pygame.display.flip()

    clock.tick(30)

# pygame.time.wait(5000)
pygame.quit()