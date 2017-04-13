import pygame

class SpriteSheet(object): #pygame has no default sprite sheet class, so use object
    def __init__(self, sheet):
        #load the sprite sheet.
        self.spriteSheet = pygame.image.load(sheet)

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        #Create a blank image
        image = pygame.Surface([width, height]).convert()

        #Copy the sprite from the large sheet onto the smaller image
        image.blit(self.spriteSheet, (0, 0), (x, y, width, height))

        #The image will have a black background, this sets it to being transparent
        image.set_colorkey((0, 0, 0))

        #Return the image
        return image