import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (186, 0, 0)
YELLOW = (234, 150, 0)
GREEN = (0, 104, 56)
BLUE = (0, 89, 219)
HOVER_ITEM_COLOR = (240, 240, 240)

INV_WIDTH = 800
INV_HEIGHT = 150
WIN_WIDTH = 800
WIN_HEIGHT = 640

#constants representing different items
EXTINGUISHER = 0;
BOOTS = 1;
AID = 2;
CANCEL = 3;

selectedClose = pygame.image.load('images/selected_close.png')

allItems = {
    CANCEL: pygame.image.load('images/close_button.png')
}
layout = [CANCEL]
position = 0

selectedItemNr = CANCEL

def addItems(items):
    for key in items:
        allItems[key] = items[key]
        layout.append(key)

def openInventory(background_img):
    global done
    global allItems
    global layout
    done = False

    def draw_inventory(screen, selected_item):
        # background
        s = pygame.Surface((INV_WIDTH, INV_HEIGHT), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 80))  # notice the alpha value in the color
        screen.blit(s, (0, WIN_HEIGHT-INV_HEIGHT))
        # pygame.draw.rect(screen, WHITE, [0, WIN_HEIGHT-INV_HEIGHT, INV_WIDTH, INV_HEIGHT])

        #close button
        screen.blit(allItems[CANCEL], (5, WIN_HEIGHT - 3*INV_HEIGHT//4))

        counter = 0
        for key in allItems:
            if key != CANCEL:
                if selected_item == key:
                    pygame.draw.rect(screen, HOVER_ITEM_COLOR, [83+counter*128, WIN_HEIGHT - 140, 130, 135])

                screen.blit(allItems[key], (93 + 128 * counter, WIN_HEIGHT-130))
                counter+=1

    def navigate_menu(key):
        global done
        global selectedItemNr
        global allItems
        global position

         # Find the chosen item
        if key == pygame.K_a:
            if position-1>=0:
                position = position-1
            else:
                position = len(layout)-1

            selectedItemNr = layout[position]
        elif key == pygame.K_d:
            if position + 1 >= len(layout):
                selectedItemNr = CANCEL
                position = 0
            else:
                position = position + 1
                selectedItemNr = layout[position]

        elif key == pygame.K_RETURN:
            done = True
            if position == 0:
                return -1
            else:
                temp = layout[position]
                del allItems[temp]
                del layout[position]
                return temp

    pygame.init()
    size = (WIN_WIDTH, WIN_HEIGHT)
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if event.type == pygame.KEYDOWN:
            item = navigate_menu(event.key)
            if done:
                return item

        if not done:
            screen.blit(background_img, (0,0))

            draw_inventory(screen, selectedItemNr)
            if selectedItemNr == CANCEL:
                screen.blit(selectedClose, (5, WIN_HEIGHT - 3*INV_HEIGHT//4))

            pygame.display.flip()

            clock.tick(12)