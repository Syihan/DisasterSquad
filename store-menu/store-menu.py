import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (186, 0, 0)
YELLOW = (234, 150, 0)
GREEN = (0, 104, 56)
BLUE = (0, 89, 219)
HOVER_ITEM_COLOR = (240, 240, 240)

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HEADER_HEIGHT = int(WIN_HEIGHT / 6)
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

#constants representing different items
EXTINGUISHER = 0;
BOOTS = 1;
AID = 2;

CANCEL = 3;
CHECKOUT = 4;

selectedCheckout = pygame.image.load('../images/selected_checkout.png')
selectedClose = pygame.image.load('../images/selected_close.png')

allItems = {
    EXTINGUISHER: pygame.image.load('../images/extinguisher.png'),
    BOOTS: pygame.image.load('../images/extinguisher.png'),
    AID: pygame.image.load('../images/extinguisher.png'),

    CANCEL: pygame.image.load('../images/close_button.png'),
    CHECKOUT: pygame.image.load('../images/checkout.png'),
}

info = {
    EXTINGUISHER: "Fire Extinguisher ($30): Used to put out any fire.",
    BOOTS: "Boots ($90): Help prevent electrocution.",
    AID: "First Aid ($40): Restores some health to the player.",
}

prices = {
    EXTINGUISHER: 30,
    BOOTS: 90,
    AID: 40
}
storeMoney = 160
cartTotal = 0
yourMoney = 100
position = -1
width, height = 6, 2
layout = []

layout.append([EXTINGUISHER, BOOTS, AID, -1, -1, -1]) #left three spaces for store, right 3 for inventory
layout.append([CANCEL, CANCEL, CANCEL, CHECKOUT, CHECKOUT, CHECKOUT])


def display_item_info(screen, itemNr):
    infoFont = pygame.font.Font(None, 20)
    infoText = infoFont.render(info[itemNr], 1, WHITE)
    pygame.draw.rect(screen, BLACK, [2, WIN_HEIGHT-60, 363, 60])
    screen.blit(infoText, (10, WIN_HEIGHT-40))


def draw_table_structure(screen):
    # top parts
    pygame.draw.rect(screen, WHITE, [2, 2, HALF_WIDTH - 4, HEADER_HEIGHT])
    pygame.draw.rect(screen, WHITE, [HALF_WIDTH, 2, HALF_WIDTH - 2, HEADER_HEIGHT])

    # green parts
    pygame.draw.rect(screen, GREEN, [HALF_WIDTH/4, 2*HEADER_HEIGHT/3+3, HALF_WIDTH/2, HEADER_HEIGHT/3])
    pygame.draw.rect(screen, GREEN, [HALF_WIDTH + HALF_WIDTH/4, 2*HEADER_HEIGHT/3+3, HALF_WIDTH/2, HEADER_HEIGHT/3])

    # main parts
    storeRect = pygame.draw.rect(screen, WHITE, [2, HEADER_HEIGHT+4, HALF_WIDTH-4, WIN_HEIGHT-HEADER_HEIGHT-6])
    pygame.draw.rect(screen, WHITE, [HALF_WIDTH, HEADER_HEIGHT+4, HALF_WIDTH-2, WIN_HEIGHT-HEADER_HEIGHT-6])

    #close button
    screen.blit(allItems[CANCEL], (HALF_WIDTH-35, WIN_HEIGHT-72))

    #checkout button
    screen.blit(allItems[CHECKOUT], (WIN_WIDTH - 147, WIN_HEIGHT - 82))

def draw_store_items(screen, selected_item):
    itemNumber = 0
    leftShift = 0

    for y in range(0, 6):
        if layout[0][y] != -1:
            itemNumber = layout[0][y]
            if y>2:
                leftShift = 14
            if selected_item == allItems[itemNumber]:
                pygame.draw.rect(screen, HOVER_ITEM_COLOR, [8+y*128+leftShift, HEADER_HEIGHT + 48, 130, 130])
            screen.blit(allItems[itemNumber], (18+128*y+leftShift, HEADER_HEIGHT+52))


def navigate_menu(key):
    global selectedItemNr
    global allItems
    global layout
    global position

     #TODO: selectedItemNr or position?
    # if position == -1:
    #     position = selectedItemNr%3
    # x = position
    x = selectedItemNr%3
    y = selectedItemNr//3

     # Find the chosen item
    #TODO: moving right on something already moved to the right actually selects item that USED to be on its right
    if key == pygame.K_a:
        if y == 1:
            selectedItemNr = CANCEL
        if x - 1 < 0:
            x = 6
        while (layout[0][x-1] == -1):
            if x-2 < 0:
                x = 5
            else:
                x -= 1
        selectedItemNr = layout[0][x-1]
        position = x-1

    elif key == pygame.K_d:
        if y == 1:
            selectedItemNr = CHECKOUT
        if x + 1 > 5:
            x = -1
        while (layout[0][x+1] == -1):
            if x+2 > 5:
                x = 0
            else:
                x += 1
        selectedItemNr = layout[0][x+1]
        position = x+1

    elif key == pygame.K_RETURN:
        switch_side(selectedItemNr)

    elif key == pygame.K_s:
        if x<3:
            selectedItemNr = CANCEL
        elif x<CANCEL:
            selectedItemNr = CHECKOUT

    elif key == pygame.K_w:
        selectedItemNr = 0

def switch_side(selectedItemNr):
    global position
    global storeMoney
    global cartTotal
    layout[0][position]=-1
    i=0

    if position < 3:
        i=3

    while (layout[0][i] != -1):
        i+=1

    for y in range(0, 6):
        if layout[0][y] == selectedItemNr:
            layout[0][y] = -1

    layout[0][i] = selectedItemNr
    position = i
    if i>2:
        storeMoney = storeMoney - prices[selectedItemNr]
        cartTotal = cartTotal + prices[selectedItemNr]
    else:
        storeMoney = storeMoney + prices[selectedItemNr]
        cartTotal = cartTotal - prices[selectedItemNr]

    storeMoneyText = moneyFont.render("$" + str(storeMoney), 1, WHITE)
    yourMoneyText = moneyFont.render("$" + str(cartTotal), 1, WHITE)




pygame.init()
pygame.font.init()
size = (WIN_WIDTH, WIN_HEIGHT)
screen = pygame.display.set_mode(size)

items = []

headerFont = pygame.font.Font(None, 68)
moneyFont = pygame.font.Font(None, 42)
storeItemsText = headerFont.render("Store Items", 1, YELLOW)
yourItemsText = headerFont.render("Items to Buy", 1, BLUE)

clock = pygame.time.Clock()

started = False
done = False

selectedItemNr = EXTINGUISHER

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if event.type == pygame.KEYDOWN:
        navigate_menu(event.key)


    screen.fill(BLACK)

    draw_table_structure(screen)
    draw_store_items(screen, allItems[selectedItemNr])
    display_item_info(screen, selectedItemNr)
    screen.blit(storeItemsText, (HALF_WIDTH/6+5, HEADER_HEIGHT/6))
    screen.blit(yourItemsText, (HALF_WIDTH+HALF_WIDTH/6 -5, HEADER_HEIGHT/6))

    storeMoneyText = moneyFont.render("$" + str(storeMoney), 1, WHITE)
    cartMoneyText = moneyFont.render("$" + str(cartTotal), 1, WHITE)
    yourMoneyText = moneyFont.render("Have: $" + str(yourMoney), 1, YELLOW)
    screen.blit(storeMoneyText, (HALF_WIDTH/2 - 30, 2*HEADER_HEIGHT/3+6))
    screen.blit(cartMoneyText, (HALF_WIDTH + HALF_WIDTH/2 - 25, 2*HEADER_HEIGHT/3 + 6))
    screen.blit(yourMoneyText, (HALF_WIDTH + 65, WIN_HEIGHT-55))

    pygame.display.flip()

    clock.tick(12)

pygame.quit()