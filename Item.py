""" Base class for item, items should be able to read themselves in from config files """
import pygame
import os
class Item(pygame.sprite.Sprite):
    """ this will be the holder class for items """
    def __init__(self, name, image, special):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load(os.path.join('images', image))
        self.special = special
        self.rect = self.image.get_rect()
        
    def __repr__(self):
        """ return the name as the representation """
        return self.name
        