""" Base class for item, items should be able to read themselves in from config files """
import pygame
import os
class Item(pygame.sprite.Sprite):
    """ this will be the holder class for items """
    def __init__(self, name, image, special):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image_name = image 
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.special = special
        self.rect = self.image.get_rect()
        self.desc = None
        self.effects = dict()
        self.equiped = False
        self.slot = None
        
    def re_init_images(self):
        # this has to be done to reload the sprite after loading a game
        self.image = pygame.image.load(os.path.join('images', self.image_name))
        self.rect = self.image.get_rect()
       
    def __str__(self):
        """ return the name as the string representation """
        return self.name
        