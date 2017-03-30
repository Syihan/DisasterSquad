import pygame

class Sprite(pygame.sprite.Sprite):
    destructable = False
    identity = 0 #0 = barrier of some kind, 1 = player

    def __init__(self, sprite, startx, starty, width, height, identity = 0):
        super().__init__()

        self.identity = identity # 0 = barrier, 1 = player

        self.width = width
        self.height = height

        #set the image
        self.image = pygame.image.load(sprite)

        #Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        #set the starting location
        self.rect.topleft = [startx, starty]

        #scale the image down to a manageable size
        self.image = pygame.transform.smoothscale(self.image, (width, height))

        #scale hitbox to new size
        self.rect = self.rect.clip(pygame.Rect(startx, starty, width, height))